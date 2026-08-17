# 原則候補

```yaml
- id: p01
  title: ローカルリポジトリを作業基点にする
  type: principle
  source_chapter: Why use Codex CLI
  source_quote: |
    "Work against your local repository: Let Codex inspect files, make edits, and run the tools already installed on your machine."
  summary: |
    Codex CLIは、抽象的な会話だけでなく、対象リポジトリのファイルと既存ツールを
    同じ作業文脈として扱う。調査、編集、実行をリポジトリ内で閉じた反復へまとめる。
  tags: [principle, local-repository, workflow]

- id: p02
  title: タスクに合わせて制御条件を選ぶ
  type: principle
  source_chapter: Why use Codex CLI
  source_quote: |
    "Stay in control: Choose the model, reasoning effort, permissions, and commands that fit the task."
  summary: |
    モデル、推論量、権限、実行コマンドを一律に固定せず、タスクの難しさと危険度に
    合わせて選ぶ。能力だけでなく実行境界も作業設計の一部にする。
  tags: [principle, control, permissions, model-selection]

- id: p03
  title: 反復作業はcodex execへ移す
  type: principle
  source_chapter: Why use Codex CLI
  source_quote: |
    "Compose with scripts and CI: Use Codex interactively or call codex exec from repeatable workflows and pipelines."
  summary: |
    探索的な作業は対話的に行い、入力と判定が定まった反復作業は `codex exec` を
    スクリプトやCIから呼ぶ。対話と自動化を目的で使い分ける。
  tags: [principle, codex-exec, automation, ci]

- id: p04
  title: 初回は焦点を絞ったタスクから始める
  type: principle
  source_chapter: Getting started · Start your first task
  source_quote: |
    "Describe what you want to accomplish. For example, ask Codex to explain the project, make a focused change, or help debug an issue."
  summary: |
    最初から広範な自動化を任せず、プロジェクト説明、限定的変更、デバッグなど、
    成否を観察しやすい一つの目的を伝える。
  tags: [principle, prompting, focused-task, onboarding]

- id: p05
  title: 作業前後にGitチェックポイントを作る
  type: principle
  source_chapter: Getting started · Start your first task
  source_quote: |
    "Create Git checkpoints before and after a task so you can revert changes."
  summary: |
    Codexへ変更を任せる前後でGitの復元点を確保し、差分比較と取り消しを可能にする。
    回復可能性をエージェント作業の前提条件として扱う。
  tags: [principle, git, checkpoint, recovery]

- id: p06
  title: 同じセッションで作業ループを継続する
  type: principle
  source_chapter: See what Codex CLI can do · Keep the coding loop in your terminal
  source_quote: |
    "Steer the active turn, inspect commands and diffs as they appear, and keep follow-up work in the same session."
  summary: |
    実行中のターンを誘導し、表示されるコマンドと差分を確認し、追加作業を同じ
    セッションへ積み重ねる。途中経過を観察できる連続的な開発ループを保つ。
  tags: [principle, interactive-loop, steering, diff-review]

- id: p07
  title: 反復指示はskillとして再利用する
  type: principle
  source_chapter: See what Codex CLI can do · Use skills and plugins
  source_quote: |
    "Package repeatable instructions as skills, then add plugins to connect Codex to your team's tools and data without leaving the CLI."
  summary: |
    毎回貼り直す手順はskillへまとめ、チームのツールやデータへの接続はpluginで
    補う。再利用する指示と外部接続を別の役割として扱う。
  tags: [principle, skills, plugins, reuse]

- id: p08
  title: 出荷前レビューは作業ツリーを変更せず行う
  type: principle
  source_chapter: See what Codex CLI can do · Review changes before they ship
  source_quote: |
    "Codex reports prioritized findings without modifying your working tree, so you can address risks before you commit or open a pull request."
  summary: |
    未コミット差分、コミット、基準ブランチに対するレビューでは、修正と検査を分離し、
    作業ツリーを変えずに優先順位付きの問題を得る。
  tags: [principle, code-review, read-only, risk]

- id: p09
  title: 実行前に権限境界を確認する
  type: principle
  source_chapter: Build a terminal workflow around Codex · Set the boundaries for each run
  source_quote: |
    "Choose when Codex can edit files or run commands without asking, and inspect the active sandbox and writable roots before you continue."
  summary: |
    ファイル編集やコマンド実行を無確認で許す条件を選び、処理を続ける前に有効な
    sandboxと書き込み可能なルートを確認する。
  tags: [principle, permissions, sandbox, writable-roots]
```
