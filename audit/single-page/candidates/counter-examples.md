# Counter-example candidates — Codex CLI

## Extraction audit

- **Stage**: 1 (counter-example extraction only)
- **Extractor contract**: `extractors/counter-example-extractor.md`
- **Corpus**: `https://learn.chatgpt.com/docs/codex/cli.md`
- **Corpus boundary**: Only the Markdown body returned by the URL above was examined. Linked pages were not opened or treated as source text.
- **Result**: One qualifying warning candidate was found.
- **Exclusion rule**: Capability descriptions were not inverted into warnings. In particular, the descriptions of `codex --search`, `/permissions`, code review, `codex exec`, cloud, subagents, and MCP do not state a failure outcome on this page, so no counter-example was inferred from them.

```yaml
- id: ce01
  title: Gitチェックポイントを作らずにタスクを進める
  type: counter-example
  source_chapter: Getting started · 3. Start your first task
  source_quote: |
    "Create Git checkpoints before and after a task so you can revert changes."
  failure_mode: |
    タスクの前後にGitチェックポイントを作らず、変更をチェックポイントへ
    戻せる状態を用意しないまま作業を進める。
  mechanism: |
    本文は、タスク前後のGitチェックポイントを変更のrevertに使うものとしている。
    チェックポイントを設けない進め方では、この回復手段をあらかじめ確保できない。
  warning_signs:
    - タスク開始前のGitチェックポイントがない
    - タスク完了後のGitチェックポイントがない
  bound_to:
    - "Codex CLIで最初のタスクを実行する"
    - "リポジトリ中心の対話型開発ループを運用する"
    - "Codexによる変更を回復可能に保つ"
  tags: [counter-example, git, checkpoint, revert]
```
