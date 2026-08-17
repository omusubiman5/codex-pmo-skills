# 用語候補

```yaml
- id: g01
  term: Codex CLI
  type: term
  source_chapter: Inspect, edit, and run code from your terminal
  author_definition: |
    "Inspect code, make changes, run commands, and automate repeatable work without leaving your terminal."
  key_distinction: |
    単なるチャット用CLIではない。コード調査、変更、ローカルコマンド実行、反復作業の自動化を同じターミナル面で扱う。
  why_it_matters: |
    後続skillが、Codex CLIを質問応答だけに狭めたり、逆に無制限な自動実行と誤解したりするのを防ぐ。
  tags: [term, codex-cli, terminal]

- id: g02
  term: local repository
  type: term
  source_chapter: Why use Codex CLI
  author_definition: |
    "Let Codex inspect files, make edits, and run the tools already installed on your machine."
  key_distinction: |
    一般的なコード保管場所ではなく、Codexがファイル、差分、既存ツールを扱う作業文脈を指す。
  why_it_matters: |
    対象ディレクトリを誤ると、調査・編集・実行の全境界が誤るため、各workflow skillの前提になる。
  tags: [term, repository, workspace]

- id: g03
  term: permissions
  type: term
  source_chapter: Build a terminal workflow around Codex · Set the boundaries for each run
  author_definition: |
    "Choose when Codex can edit files or run commands without asking, and inspect the active sandbox and writable roots before you continue."
  key_distinction: |
    OSのアカウント権限一般ではなく、Codexが確認なしに編集・実行できる条件と実効sandboxの境界を指す。
  why_it_matters: |
    自動化の速度と変更リスクを調整する中心概念であり、安全運用skillの判断入力になる。
  tags: [term, permissions, sandbox, safety]

- id: g04
  term: interactive loop
  type: term
  source_chapter: See what Codex CLI can do · Keep the coding loop in your terminal
  author_definition: |
    "Steer the active turn, inspect commands and diffs as they appear, and keep follow-up work in the same session."
  key_distinction: |
    一回のプロンプトと応答ではなく、実行を観察しながら誘導・確認・追加依頼を反復する開発サイクル。
  why_it_matters: |
    非対話型 `codex exec` と使い分ける基準になる。
  tags: [term, interactive, steering, session]

- id: g05
  term: codex exec
  type: term
  source_chapter: Why use Codex CLI
  author_definition: |
    "Use Codex interactively or call codex exec from repeatable workflows and pipelines."
  key_distinction: |
    対話型TUIではなく、反復可能なworkflowやpipelineから呼ぶ非対話入口。
  why_it_matters: |
    CI・スクリプト向けの設計を、探索的な対話作業から分離するために必要になる。
  tags: [term, codex-exec, automation, ci]

- id: g06
  term: skills
  type: term
  source_chapter: See what Codex CLI can do · Use skills and plugins
  author_definition: |
    "Package repeatable instructions as skills"
  key_distinction: |
    一回限りのプロンプトではなく、繰り返す指示を再利用可能な形にまとめたもの。
  why_it_matters: |
    手順の再現性を高め、同じ要求を会話ごとに貼り直す必要を減らす。
  tags: [term, skills, reusable-instructions]

- id: g07
  term: plugins
  type: term
  source_chapter: See what Codex CLI can do · Use skills and plugins
  author_definition: |
    "add plugins to connect Codex to your team's tools and data without leaving the CLI."
  key_distinction: |
    指示をまとめるskillsに対し、チームの外部ツールやデータへの接続を追加する。
  why_it_matters: |
    再利用手順の問題と、外部能力・データ接続の問題を混同しないために必要になる。
  tags: [term, plugins, tools, data]

- id: g08
  term: MCP
  type: term
  source_chapter: Build a terminal workflow around Codex · Connect external tools with MCP
  author_definition: |
    "Add local or remote MCP servers, authenticate when needed, and inspect the tools available to the current session before Codex uses them."
  key_distinction: |
    特定サービス名ではなく、ローカルまたはリモートのサーバーを通じてツールを接続・認証・確認する仕組み。
  why_it_matters: |
    Codexが利用できる外部操作の範囲と、その事前確認方法を定義する。
  tags: [term, mcp, external-tools, authentication]

- id: g09
  term: code review
  type: term
  source_chapter: See what Codex CLI can do · Review changes before they ship
  author_definition: |
    "Run a dedicated review against uncommitted changes, a commit, or a base branch."
  key_distinction: |
    コード変更そのものではなく、指定した差分面を検査して優先順位付きの指摘を返す専用処理。
  why_it_matters: |
    実装と検査を分離し、レビュー時に作業ツリーを変えない境界を保つ。
  tags: [term, code-review, diff, read-only]

- id: g10
  term: Codex cloud
  type: term
  source_chapter: Build a terminal workflow around Codex · Move work to Codex cloud
  author_definition: |
    "Browse active and completed chats, submit work to a configured environment, and apply the result to your local repository from the terminal."
  key_distinction: |
    ローカルCLIの代替ではなく、設定済み環境へ作業を提出し、結果をローカルへ適用する委譲先。
  why_it_matters: |
    ローカル対話、非対話実行、クラウド委譲を選び分けるworkflow skillの用語基盤になる。
  tags: [term, codex-cloud, delegation, environment]
```
