#!/usr/bin/env python3
"""Write AI NEWS JSON as one Markdown file per item."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit


TRACKING_KEYS = {"gclid", "fbclid", "mc_cid", "mc_eid"}
REQUIRED = ("title", "url", "retrieved_at", "source_text")
FORBIDDEN_ACTION_TERMS = {
    "記事にする", "記事化", "記事候補", "記事下書き", "下書きする",
    "Pith に追加", "Pith 記事", "claude-skills に追加", "skill を新設",
    "MEMORY.md に記録", "MEMORY.md にメモ", "cma-002 題材",
    "AI News Pipeline の題材", "エピソード題材", "daily-post に登録",
    "reference に残す", "reference にメモ", "video-gen 題材",
    "検討する", "注視", "整理する", "モニタリング", "モニター", "フォロー", "ウォッチ",
}
JAPANESE_RE = re.compile(r"[\u3040-\u30ff\u3400-\u9fff]")
CONCRETE_ACTION_RE = re.compile(r"\d|本日|今日|今週|今月|まで|以内|毎日|毎週")


class InputError(ValueError):
    """Raised when input cannot safely produce a note."""


def yaml_string(value: object) -> str:
    return json.dumps("" if value is None else str(value), ensure_ascii=False)


def canonical_url(value: str) -> str:
    parsed = urlsplit(value.strip())
    if parsed.scheme.lower() not in {"http", "https"} or not parsed.netloc:
        raise InputError("url must be an absolute http(s) URL")
    query = sorted(
        (key, val)
        for key, val in parse_qsl(parsed.query, keep_blank_values=True)
        if not key.lower().startswith("utm_") and key.lower() not in TRACKING_KEYS
    )
    path = parsed.path or "/"
    return urlunsplit((parsed.scheme.lower(), parsed.netloc.lower(), path, urlencode(query), ""))


def iso_date(value: str, field: str) -> str:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (TypeError, ValueError) as exc:
        raise InputError(f"{field} must be ISO 8601") from exc
    return parsed.date().isoformat()


def normalized_item(raw: object, index: int, allow_live_data: bool = False) -> dict[str, object]:
    if not isinstance(raw, dict):
        raise InputError(f"item {index} must be an object")
    missing = [field for field in REQUIRED if not isinstance(raw.get(field), str) or not raw[field].strip()]
    if missing:
        raise InputError(f"item {index} missing string fields: {', '.join(missing)}")
    sample_data = raw.get("sample_data") is True
    if not sample_data and not allow_live_data:
        raise InputError(f"item {index} must set sample_data=true unless --allow-live-data is explicit")
    key_points = raw.get("key_points")
    if key_points is None:
        key_points = [raw.get("kp1", ""), raw.get("kp2", ""), raw.get("kp3", "")]
    if not isinstance(key_points, list) or not all(isinstance(point, str) for point in key_points):
        raise InputError(f"item {index} key_points must be an array of strings")
    key_points = [point.strip() for point in key_points if point.strip()]
    summary = str(raw.get("summary", "")).strip()
    action = str(raw.get("action", "")).strip()
    if not summary.startswith("結論：") or "\n仕組み：" not in summary:
        raise InputError(f"item {index} summary must contain Japanese 結論 and 仕組み sections")
    if len(key_points) != 3 or len(set(key_points)) != 3:
        raise InputError(f"item {index} must contain three distinct key points")
    if not JAPANESE_RE.search(summary) or any(not JAPANESE_RE.search(point) for point in key_points):
        raise InputError(f"item {index} summary and key points must be written in Japanese")
    if not action:
        raise InputError(f"item {index} action must be non-empty")
    if not JAPANESE_RE.search(action) or not CONCRETE_ACTION_RE.search(action):
        raise InputError(f"item {index} action must be Japanese and contain a number or deadline")
    forbidden = next((term for term in FORBIDDEN_ACTION_TERMS if term in action), None)
    if forbidden:
        raise InputError(f"item {index} action contains forbidden term: {forbidden}")
    source_kind = str(raw.get("source_kind", "fixture")).strip().lower()
    if source_kind not in {"gmail", "web", "fixture"}:
        raise InputError(f"item {index} source_kind must be gmail, web, or fixture")

    canonical = canonical_url(str(raw["url"]))
    news_id = hashlib.sha256(canonical.encode("utf-8")).hexdigest()[:12]
    published_at = str(raw.get("published_at", "")).strip()
    retrieved_at = str(raw["retrieved_at"]).strip()
    retrieved_date = iso_date(retrieved_at, "retrieved_at")
    date_value = iso_date(published_at, "published_at") if published_at else retrieved_date
    item = {
        "title": str(raw["title"]).strip(),
        "news_id": news_id,
        "status": str(raw.get("status", "collected")).strip() or "collected",
        "source_url": str(raw["url"]).strip(),
        "canonical_url": canonical,
        "source_kind": source_kind,
        "source_name": str(raw.get("source_name", "")).strip(),
        "category": str(raw.get("category", "")).strip(),
        "published_at": published_at,
        "retrieved_at": retrieved_at,
        "summary": summary,
        "key_points": key_points,
        "action": action,
        "source_text": str(raw["source_text"]),
        "source_ref": str(raw.get("source_ref", "")).strip(),
        "sample_data": sample_data,
        "date": date_value,
    }
    hash_fields = {
        key: value
        for key, value in item.items()
        if key not in {"date", "news_id", "source_url", "retrieved_at"}
    }
    item["content_hash"] = hashlib.sha256(
        json.dumps(hash_fields, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    return item


def resolve_inside(root: Path, candidate: Path, label: str) -> Path:
    resolved_root = root.resolve()
    resolved = (candidate if candidate.is_absolute() else resolved_root / candidate).resolve()
    try:
        resolved.relative_to(resolved_root)
    except ValueError as exc:
        raise InputError(f"{label} must stay inside vault root") from exc
    return resolved


def validate_source_ref(item: dict[str, object], vault_root: Path) -> None:
    ref = str(item["source_ref"])
    if not ref:
        return
    ref_path = Path(ref)
    if ref_path.suffix.lower() != ".md":
        raise InputError("source_ref must point to a Markdown file")
    resolved = resolve_inside(vault_root, ref_path, "source_ref")
    if not resolved.is_file():
        raise InputError(f"source_ref does not exist: {ref}")


def render(item: dict[str, object]) -> str:
    frontmatter = [
        "---",
        f"date: {yaml_string(item['date'])}",
        f"system: {yaml_string(item['source_name'])}",
        f"category: {yaml_string(item['category'])}",
        f"title: {yaml_string(item['title'])}",
        f"url: {yaml_string(item['canonical_url'])}",
        f"news_id: {yaml_string(item['news_id'])}",
        f"status: {yaml_string(item['status'])}",
        f"original_source_url: {yaml_string(item['source_url'])}",
        f"canonical_url: {yaml_string(item['canonical_url'])}",
        f"source_kind: {yaml_string(item['source_kind'])}",
        f"published_at: {yaml_string(item['published_at'])}",
        f"retrieved_at: {yaml_string(item['retrieved_at'])}",
        f"content_hash: {yaml_string(item['content_hash'])}",
        f"sample_data: {'true' if item['sample_data'] else 'false'}",
    ]
    if item["source_ref"]:
        frontmatter.append(f"source_ref: {yaml_string(item['source_ref'])}")
    frontmatter.extend(["---", "", f"# {item['title']}", ""])

    body: list[str] = []
    body.extend(["## CMA001 digest", "", "### F: summary", "", str(item["summary"]), ""])
    for label, point in zip(("G: kp1", "H: kp2", "I: kp3"), item["key_points"]):
        body.extend([f"### {label}", "", str(point), ""])
    body.extend(["### J: action", "", str(item["action"]), ""])

    body.extend(["## Source", ""])
    if item["source_ref"]:
        body.extend([f"[[{item['source_ref']}|source]]", ""])
    body.append(str(item["source_text"]).rstrip())
    body.append("")
    return "\n".join(frontmatter + body)


def existing_hash(path: Path) -> str | None:
    if not path.is_file():
        return None
    match = re.search(r'^content_hash:\s*["\']?([0-9a-f]{64})["\']?\s*$', path.read_text(encoding="utf-8"), re.MULTILINE)
    return match.group(1) if match else "invalid"


def load_items(path: str) -> list[object]:
    if path == "-":
        payload = json.load(sys.stdin)
    else:
        with Path(path).open(encoding="utf-8") as stream:
            payload = json.load(stream)
    if isinstance(payload, dict):
        payload = payload.get("items")
    if not isinstance(payload, list):
        raise InputError("input must be an array or an object with an items array")
    return payload


def run(args: argparse.Namespace) -> int:
    vault_root = Path(args.vault_root).resolve()
    if not vault_root.is_dir():
        raise InputError("vault root does not exist")
    output_root = resolve_inside(vault_root, Path(args.output_root), "output root")

    items = [normalized_item(raw, index, args.allow_live_data) for index, raw in enumerate(load_items(args.input), start=1)]
    planned: dict[Path, dict[str, object]] = {}
    report: dict[str, object] = {"schema": "ai-news-markdown-report-v1", "dry_run": args.dry_run, "created": [], "skipped": [], "conflicts": []}

    for item in items:
        validate_source_ref(item, vault_root)
        target = output_root / f"{item['date']}-news-{item['news_id']}.md"
        if target in planned:
            if planned[target]["content_hash"] == item["content_hash"]:
                report["skipped"].append(str(target.relative_to(vault_root)).replace("\\", "/"))
                continue
            report["conflicts"].append(str(target.relative_to(vault_root)).replace("\\", "/"))
            continue
        current_hash = existing_hash(target)
        if current_hash is None:
            planned[target] = item
        elif current_hash == item["content_hash"]:
            report["skipped"].append(str(target.relative_to(vault_root)).replace("\\", "/"))
        else:
            report["conflicts"].append(str(target.relative_to(vault_root)).replace("\\", "/"))

    if report["conflicts"]:
        report["result"] = "conflict"
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 2

    planned_paths = [str(path.relative_to(vault_root)).replace("\\", "/") for path in planned]
    if args.dry_run:
        report["planned"] = planned_paths
        report["result"] = "ready"
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0

    for target, item in planned.items():
        target.parent.mkdir(parents=True, exist_ok=True)
        try:
            with target.open("x", encoding="utf-8", newline="\n") as stream:
                stream.write(render(item))
        except FileExistsError:
            report["conflicts"].append(str(target.relative_to(vault_root)).replace("\\", "/"))
            report["result"] = "conflict"
            print(json.dumps(report, ensure_ascii=False, indent=2))
            return 2
        report["created"].append(str(target.relative_to(vault_root)).replace("\\", "/"))

    report["result"] = "created" if report["created"] else "no-change"
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", help="JSON file path, or - for stdin")
    parser.add_argument("--vault-root", required=True, help="Explicitly selected Vault or output root directory")
    parser.add_argument("--output-root", required=True, help="Explicitly selected output directory inside --vault-root")
    parser.add_argument("--dry-run", action="store_true", help="Report without writing files")
    parser.add_argument("--allow-live-data", action="store_true", help="Allow sample_data=false for an explicitly selected non-sample output root")
    args = parser.parse_args()
    try:
        raise SystemExit(run(args))
    except (InputError, json.JSONDecodeError, OSError, UnicodeError) as exc:
        print(json.dumps({"schema": "ai-news-markdown-report-v1", "result": "invalid", "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        raise SystemExit(3) from exc


if __name__ == "__main__":
    main()
