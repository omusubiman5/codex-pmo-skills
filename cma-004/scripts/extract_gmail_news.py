#!/usr/bin/env python3
"""Extract article candidates from Gmail connector/API message JSON."""

from __future__ import annotations

import argparse
import base64
import html
import json
import re
import sys
from datetime import datetime, timezone
from email.utils import parseaddr, parsedate_to_datetime
from html.parser import HTMLParser
from pathlib import Path
from typing import Any
from urllib.parse import parse_qsl, unquote, urlencode, urlsplit, urlunsplit


URL_RE = re.compile(r"https?://[^\s<>\]\[\)\(\"']+", re.IGNORECASE)
TRACKING_KEYS = {"gclid", "fbclid", "mc_cid", "mc_eid"}
BLOCKED_TERMS = {
    "unsubscribe",
    "preferences",
    "privacy",
    "terms",
    "manage-subscription",
    "manage_preferences",
    "view-in-browser",
    "facebook.com",
    "instagram.com",
    "linkedin.com",
    "youtube.com",
    "twitter.com",
    "x.com/intent",
}
GENERIC_TITLES = {
    "read more",
    "learn more",
    "click here",
    "view online",
    "open in browser",
    "続きを読む",
    "詳細はこちら",
}
SENDER_SYSTEMS = {
    "dan@tldrnewsletter.com": "TLDR",
    "news@daily.therundown.ai": "The Rundown AI",
    "hi@robotics.therundown.ai": "The Rundown Robotics",
    "bensbites@substack.com": "Ben's Bites",
    "agentai@mail.beehiiv.com": "simple.ai",
}
SPONSOR_TERMS = {"sponsor", "sponsored", "together with", "advertisement", "partner message"}
BEN_ALLOWED_SECTIONS = {"headlines", "my feed"}


class ExtractError(ValueError):
    """Raised when Gmail JSON cannot be safely interpreted."""


class BlockLinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.blocks: list[dict[str, object]] = []
        self.text: list[str] = []
        self._block_tag: str | None = None
        self._block_text: list[str] = []
        self._block_links: list[tuple[str, str]] = []
        self._href: str | None = None
        self._anchor_text: list[str] = []
        self._ignored_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        lowered = tag.lower()
        if lowered in {"script", "style"}:
            self._ignored_depth += 1
        if lowered in {"h1", "h2", "h3", "h4", "h5", "h6", "p", "li"} and self._ignored_depth == 0 and self._block_tag is None:
            self._block_tag = lowered
            self._block_text = []
            self._block_links = []
        if lowered == "a" and self._ignored_depth == 0:
            self._href = dict(attrs).get("href")
            self._anchor_text = []

    def handle_endtag(self, tag: str) -> None:
        lowered = tag.lower()
        if lowered == "a" and self._href:
            title = clean_text(" ".join(self._anchor_text))
            if self._block_tag is not None:
                self._block_links.append((title, html.unescape(self._href)))
            self._href = None
            self._anchor_text = []
        if lowered == self._block_tag:
            text = clean_text(" ".join(self._block_text))
            if text or self._block_links:
                self.blocks.append({"tag": self._block_tag, "text": text, "links": list(self._block_links)})
            self._block_tag = None
            self._block_text = []
            self._block_links = []
        if lowered in {"script", "style"} and self._ignored_depth:
            self._ignored_depth -= 1

    def handle_data(self, data: str) -> None:
        if self._ignored_depth:
            return
        self.text.append(data)
        if self._block_tag is not None:
            self._block_text.append(data)
        if self._href is not None:
            self._anchor_text.append(data)


def clean_text(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def unwrap_tracking_url(value: str) -> str:
    value = html.unescape(value.strip())
    parsed = urlsplit(value)
    if parsed.netloc.lower() == "tracking.tldrnewsletter.com":
        match = re.match(r"^/CL0/([^/]+)/\d+/", parsed.path, re.IGNORECASE)
        if match:
            decoded = unquote(match.group(1))
            if decoded.lower().startswith(("http://", "https://")):
                return decoded
    return value


def canonical_url(value: str) -> str:
    parsed = urlsplit(unwrap_tracking_url(value).strip().rstrip(".,;:"))
    if parsed.scheme.lower() not in {"http", "https"} or not parsed.netloc:
        raise ExtractError("article URL must be absolute http(s)")
    query = sorted(
        (key, val)
        for key, val in parse_qsl(parsed.query, keep_blank_values=True)
        if not key.lower().startswith("utm_") and key.lower() not in TRACKING_KEYS
    )
    return urlunsplit((parsed.scheme.lower(), parsed.netloc.lower(), parsed.path or "/", urlencode(query), ""))


def is_article_link(title: str, url: str) -> bool:
    lowered = f"{title} {url}".lower()
    if any(term in lowered for term in BLOCKED_TERMS):
        return False
    if urlsplit(url).path.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".pdf")):
        return False
    normalized_title = clean_text(title).lower()
    if normalized_title in GENERIC_TITLES:
        return False
    return bool(normalized_title and len(normalized_title) >= 4)


def is_sponsor(value: str) -> bool:
    lowered = clean_text(value).lower()
    return any(term in lowered for term in SPONSOR_TERMS)


def next_body(blocks: list[dict[str, object]], start: int, title: str) -> str:
    own = clean_text(str(blocks[start].get("text", "")))
    if title and own.lower().startswith(title.lower()):
        own = clean_text(own[len(title):])
    if len(own) >= 40:
        return own
    collected = [own] if own else []
    for block in blocks[start + 1 : start + 4]:
        if str(block.get("tag", "")).startswith("h"):
            break
        text = clean_text(str(block.get("text", "")))
        if text and not is_sponsor(text):
            collected.append(text)
        if len(" ".join(collected)) >= 100:
            break
    return clean_text(" ".join(collected))


def html_candidates(html_content: str, system: str) -> tuple[list[tuple[str, str, str, str]], str]:
    parser = BlockLinkParser()
    parser.feed(html_content)
    category = ""
    candidates: list[tuple[str, str, str, str]] = []
    for index, block in enumerate(parser.blocks):
        tag = str(block.get("tag", ""))
        text = clean_text(str(block.get("text", "")))
        links = block.get("links", [])
        if tag.startswith("h") and text and not is_sponsor(text):
            category = text
        if not isinstance(links, list) or is_sponsor(category) or is_sponsor(text):
            continue
        if system == "Ben's Bites" and category.lower() not in BEN_ALLOWED_SECTIONS:
            continue
        for link in links:
            if not isinstance(link, tuple) or len(link) != 2:
                continue
            title, raw_url = clean_text(str(link[0])), unwrap_tracking_url(str(link[1]))
            try:
                canonical = canonical_url(raw_url)
            except ExtractError:
                continue
            if not is_article_link(title, canonical):
                continue
            body = next_body(parser.blocks, index, title) or title
            candidates.append((title, raw_url, category or "Uncategorized", body))
    return candidates, clean_text(" ".join(parser.text))


def decode_base64url(value: str) -> str:
    padding = "=" * (-len(value) % 4)
    return base64.urlsafe_b64decode(value + padding).decode("utf-8", "replace")


def part_content(part: dict[str, Any]) -> str:
    if isinstance(part.get("content"), str):
        return part["content"]
    if isinstance(part.get("base64_url_content"), str):
        return decode_base64url(part["base64_url_content"])
    body = part.get("body")
    if isinstance(body, dict):
        if isinstance(body.get("content"), str):
            return body["content"]
        if isinstance(body.get("data"), str):
            return decode_base64url(body["data"])
    return ""


def collect_parts(part: object, output: list[tuple[str, str]]) -> None:
    if not isinstance(part, dict):
        return
    mime = str(part.get("mime_type") or part.get("mimeType") or "").lower()
    content = part_content(part)
    if content and mime in {"text/plain", "text/html"}:
        output.append((mime, content))
    for child in part.get("parts") or []:
        collect_parts(child, output)


def header_map(message: dict[str, Any]) -> dict[str, str]:
    headers: dict[str, str] = {}
    payload = message.get("payload")
    raw_headers = payload.get("headers", []) if isinstance(payload, dict) else []
    for entry in raw_headers:
        if isinstance(entry, dict) and entry.get("name"):
            headers[str(entry["name"]).lower()] = str(entry.get("value", ""))
    for key in ("subject", "from", "date"):
        if key not in headers and isinstance(message.get(key), str):
            headers[key] = message[key]
    return headers


def message_time(message: dict[str, Any], headers: dict[str, str], fallback: str) -> str:
    raw = message.get("internal_date") or message.get("internalDate")
    if raw not in (None, ""):
        try:
            number = float(raw)
            if number > 10_000_000_000:
                number /= 1000
            return datetime.fromtimestamp(number, tz=timezone.utc).isoformat()
        except (TypeError, ValueError, OSError):
            pass
    if headers.get("date"):
        try:
            parsed = parsedate_to_datetime(headers["date"])
            if parsed.tzinfo is None:
                parsed = parsed.replace(tzinfo=timezone.utc)
            return parsed.isoformat()
        except (TypeError, ValueError, OverflowError):
            pass
    try:
        datetime.fromisoformat(fallback.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ExtractError("--retrieved-at must be ISO 8601") from exc
    return fallback


def locate_messages(payload: object) -> list[dict[str, Any]]:
    if isinstance(payload, list):
        messages = [item for item in payload if isinstance(item, dict)]
        if messages:
            return messages
    if isinstance(payload, dict):
        if isinstance(payload.get("payload"), dict):
            return [payload]
        for key in ("messages", "emails", "responses", "result", "data", "structuredContent"):
            if key in payload:
                found = locate_messages(payload[key])
                if found:
                    return found
    return []


def extract_from_message(message: dict[str, Any], retrieved_at: str, sample_data: bool, max_source_chars: int) -> list[dict[str, object]]:
    headers = header_map(message)
    parts: list[tuple[str, str]] = []
    collect_parts(message.get("payload", message), parts)
    if not parts and isinstance(message.get("body"), str):
        parts.append(("text/plain", message["body"]))
    if not parts:
        return []

    html_content = next((content for mime, content in parts if mime == "text/html"), "")
    plain_content = next((content for mime, content in parts if mime == "text/plain"), "")
    parsed_links: list[tuple[str, str, str, str]] = []
    visible_text = clean_text(plain_content)
    sender_name, sender_address = parseaddr(headers.get("from", ""))
    system = SENDER_SYSTEMS.get(sender_address.lower(), clean_text(sender_name) or "Unknown newsletter")
    if html_content:
        parsed_links, html_text = html_candidates(html_content, system)
        if not visible_text:
            visible_text = html_text
    if plain_content and not parsed_links:
        for url in URL_RE.findall(plain_content):
            before = plain_content[: plain_content.find(url)].splitlines()
            title = clean_text(before[-1]) if before else ""
            parsed_links.append((title, unwrap_tracking_url(url), "Uncategorized", title))

    subject = clean_text(headers.get("subject", "Untitled newsletter"))
    timestamp = message_time(message, headers, retrieved_at)
    if system == "simple.ai":
        online = next((entry for entry in parsed_links if "post" in entry[1].lower()), None)
        if online:
            parsed_links = [(subject, online[1], "Essay", visible_text[:max_source_chars] or subject)]
    candidates: list[dict[str, object]] = []
    seen: set[str] = set()
    for title, raw_url, category, body in parsed_links:
        title = clean_text(title)
        try:
            canonical = canonical_url(raw_url)
        except ExtractError:
            continue
        if canonical in seen or not is_article_link(title, canonical):
            continue
        seen.add(canonical)
        candidates.append(
            {
                "title": title,
                "url": raw_url,
                "published_at": timestamp,
                "retrieved_at": retrieved_at,
                "source_kind": "gmail",
                "source_name": system,
                "category": clean_text(category) or "Uncategorized",
                "source_text": clean_text(body)[:max_source_chars] or subject,
                "sample_data": sample_data,
            }
        )
    return candidates


def load_json(path: str) -> object:
    if path == "-":
        return json.load(sys.stdin)
    return json.loads(Path(path).read_text(encoding="utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", help="Gmail connector/API JSON path, or - for stdin")
    parser.add_argument("--retrieved-at", required=True, help="ISO 8601 collection timestamp")
    parser.add_argument("--sample-data", action="store_true", help="Mark fictional test input as sample data")
    parser.add_argument("--max-source-chars", type=int, default=6000)
    args = parser.parse_args()
    try:
        payload = load_json(args.input)
        messages = locate_messages(payload)
        if not messages:
            raise ExtractError("no Gmail messages found in input JSON")
        items: list[dict[str, object]] = []
        seen_urls: set[str] = set()
        window_duplicate_skip = 0
        for message in messages:
            for item in extract_from_message(message, args.retrieved_at, args.sample_data, args.max_source_chars):
                canonical = canonical_url(str(item["url"]))
                if canonical in seen_urls:
                    window_duplicate_skip += 1
                    continue
                seen_urls.add(canonical)
                items.append(item)
        result = {
            "schema": "gmail-news-candidates-v1",
            "items": items,
            "stats": {"messages": len(messages), "candidates": len(items), "window_duplicate_skip": window_duplicate_skip},
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except (ExtractError, json.JSONDecodeError, OSError, UnicodeError) as exc:
        print(json.dumps({"schema": "gmail-news-candidates-v1", "result": "invalid", "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        raise SystemExit(3) from exc


if __name__ == "__main__":
    main()
