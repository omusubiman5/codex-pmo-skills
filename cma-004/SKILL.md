---
name: cma-004
description: "CMA001のGmail・Web取得、ソース別抽出、重複排除、日本語執筆、品質検査を維持し、Google Sheetsへの出力だけを1ニュース1Markdownへ変更する。『CMA004』『CMA001をMarkdown出力』『AI NEWSをMarkdownへ保存』を依頼された時に使用する。動画・音声生成やSNS配信には使用しない。"
---

# CMA004 — CMA001を1ニュース1Markdownで出力する

## データ処理フロー

- 入力: Gmailの対象ニュースレター、ユーザー指定のWebページ・検索条件、または構造化済みニュースJSON
- 出力・保存先: 既定値を持たない。実行ごとに利用者が承認した `--vault-root` と `--output-root` を明示し、そのディレクトリ直下へ `{YYYY-MM-DD}-news-{news_id}.md` を作る。年・月などの追加階層を自動作成しない
- 移動・派生: 入力sourceを移動・上書きせず、source本文とAI生成部分を分離した派生Markdownを新規作成する
- Obsidianリンク: 入力に `source_ref` があれば `[[Vault相対パス|source]]` として保存し、参照先の存在を確認する
- 次工程: 完成したMarkdownを後続Skillが読み取る。公開や外部送信は別タスクとする

## 実行順

1. `references/acquisition.md` と `references/schema.md` を全文読む。
2. ユーザー指定の取得元、検索条件、期間、保存先を棚卸しする。
3. Gmailでは `gmail_search_email_ids` を全ページ処理し、`gmail_batch_read_email` でMIME本文を取得する。WebはWeb閲覧経路で取得する。認証設定や外部状態の変更は開始しない。
4. Gmail応答は `scripts/extract_gmail_news.py` で候補化し、CMA001と同じソース別ルールでA〜E相当（date、system、category、物理title、URL、対応body）を抽出する。URLのない項目は保存候補にしない。
5. CMA001のF〜J定義を維持し、bodyを根拠に全件を日本語で執筆する。summaryは `結論：` と `仕組み：`、重要点は相互に異なる3点、ACTIONは具体的な動詞始まりとし、禁止語を全件検査する。空欄・英文コピー・埋め草が1件でも残る間は保存しない。
6. 入力と既存Markdownを比較し、`new`、`duplicate/derived`、`uncertain`へ分類する。
7. `scripts/write_news_markdown.py` を `--dry-run` で実行し、作成、skip、競合の件数と対象パスを示す。
8. 競合が0件の場合だけ通常実行する。
9. 作成ファイルを再読し、frontmatter、source保持、CMA001のF〜J、日本語、1ニュース1ファイル、重複、リンクを検証する。
10. 取得元別件数、物理抽出数、執筆数、禁止語違反数、作成、skip、競合、外部変更、未解決事項を報告する。

## 実行例

```powershell
python .agents/skills/collect-ai-news-markdown/scripts/write_news_markdown.py news.json --vault-root <明示したroot> --output-root <明示した相対出力先> --dry-run
python .agents/skills/collect-ai-news-markdown/scripts/write_news_markdown.py news.json --vault-root <明示したroot> --output-root <明示した相対出力先>
```

Gmailコネクタ応答から始める場合:

```powershell
python .agents/skills/collect-ai-news-markdown/scripts/extract_gmail_news.py gmail-response.json --retrieved-at 2026-08-15T09:00:00+09:00 --sample-data > gmail-candidates.json
python .agents/skills/collect-ai-news-markdown/scripts/write_news_markdown.py gmail-candidates.json --vault-root <明示したroot> --output-root <明示した相対出力先> --dry-run
python .agents/skills/collect-ai-news-markdown/scripts/write_news_markdown.py gmail-candidates.json --vault-root <明示したroot> --output-root <明示した相対出力先>
```

## 安全契約

- 配布用サンプルVaultへの保存・検証は架空データだけで行う。実在ニュースをサンプル成果物として追加しない。
- ライブ取得結果は、ユーザーが実行を明示した場合に限り、配布用サンプルVaultとは別の専用出力rootへ `--allow-live-data` を付けて保存する。
- GmailとWebは読取取得だけに使う。メールの変更、返信、ラベル操作、Webへの入力・投稿を行わない。
- Google Sheetsの読取・書込、認証設定、外部送信、公開を実行しない。
- ユーザーが指定または承認した出力rootの外へ書き込まない。
- `--vault-root` と `--output-root` の省略を拒否し、Skillやスクリプト側で保存先を固定・推測しない。
- 明示された `--output-root` の下へ日付階層などを勝手に追加しない。
- 既存ファイルを上書き、移動、削除しない。
- source本文を要約で置換しない。AI生成部分は明確に分離する。
- 同一IDで内容が異なる場合は競合として停止し、自動改訂しない。
- Gmail検索、全ページ取得、MIME本文取得、候補抽出、Markdown再読のいずれかを省略した実行を成功扱いしない。
