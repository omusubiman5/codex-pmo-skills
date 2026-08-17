- id: f01
  title: タスク適合型の実行境界設計
  type: framework
  source_chapter: Why use Codex CLI
  source_quote: |
    "Stay in control: Choose the model, reasoning effort, permissions, and commands that fit the task."
  summary: |
    Codexの自律性を一律に設定せず、取り組むタスクに合わせてモデル、推論量、
    permissions、許可するコマンドを選ぶ。実行能力と操作境界を同時に調整し、
    必要な作業能力を確保しながら利用者の制御を維持するための判断枠組みである。
  tags: [control, permissions, task-fit, decision]

- id: f02
  title: 回復可能な初回タスク導入
  type: framework
  source_chapter: Getting started
  source_quote: |
    "Open a project directory and run `codex`."
    "Describe what you want to accomplish. For example, ask Codex to explain the project, make a focused change, or help debug an issue."
    "Create Git checkpoints before and after a task so you can revert changes."
  summary: |
    プロジェクトディレクトリを作業文脈としてCodexを起動し、説明、限定的変更、
    デバッグのように焦点を定めた依頼から始める。タスクの前後にGitチェックポイントを
    置き、変更を比較可能かつ取り消し可能に保つ導入フローである。
  tags: [getting-started, git, reversibility, scoped-task]

- id: f03
  title: リポジトリ中心の対話型開発ループ
  type: framework
  source_chapter: See what Codex CLI can do
  source_quote: |
    "Start Codex in a repository to explore unfamiliar code, plan a change, edit files, and run your local development tools. Steer the active turn, inspect commands and diffs as they appear, and keep follow-up work in the same session."
  summary: |
    一つのリポジトリとセッションを中心に、未知コードの探索、変更計画、編集、
    ローカルツールによる実行を順に回す。途中で利用者が方向を調整し、表示される
    コマンドと差分を検査してから、追加作業を同じセッションへつなげる反復構造である。
  tags: [interactive-loop, repository, inspect, iteration]

- id: f04
  title: 実行形態の用途別選択
  type: framework
  source_chapter: Use Codex CLI when…
  source_quote: |
    "You work from the terminal: Explore, edit, and run a repository in one focused loop."
    "You need scripting or CI: Run a non-interactive command in a repeatable workflow."
    "You want to hand work to the cloud: Launch a cloud chat and return to the terminal later."
  summary: |
    作業の性質から実行形態を選ぶ。人が継続的に誘導するリポジトリ作業には対話型CLI、
    スクリプトやCIで反復する処理には非対話コマンド、時間を置いて受け取る委譲には
    cloudを使う。入口ではなく、対話性、反復性、委譲性を判断軸にする。
  tags: [execution-mode, interactive, automation, cloud]

- id: f05
  title: 必要文脈に応じた入口選択
  type: framework
  source_chapter: Build a terminal workflow around Codex
  source_quote: |
    "Return to a saved chat — `codex resume`: Reopen a recent chat from the current repository, or search across local chats when you need to return to older work."
    "Bring visual context into the prompt — `codex --image`: Pass an error screenshot, architecture diagram, or design reference with the first prompt, or paste an image into the interactive composer."
    "Search for current context — `codex --search`: Switch a run to live web search when a task depends on current releases, documentation, or external behavior."
  summary: |
    タスクに欠けている文脈の種類を先に判定し、それに対応する入口を選ぶ。過去作業の
    継続にはresume、視覚資料にはimage、現行リリースや外部挙動にはsearchを使う。
    すべての機能を常用するのではなく、情報不足の型と入力手段を対応付ける考え方である。
  tags: [context, resume, image, web-search]

- id: f06
  title: 複雑作業の分割・再統合
  type: framework
  source_chapter: Build a terminal workflow around Codex
  source_quote: |
    "Split up a larger investigation — `subagents`: Ask Codex to delegate focused work to specialized agents, then bring their findings back into the main terminal session."
  summary: |
    大きな調査をそのまま一つの流れで処理せず、焦点を限定した作業へ分割して専門化した
    エージェントへ委譲する。各結果は分散したままにせず、主セッションへ戻して全体判断へ
    再統合する。分解と統合を一組として扱う調査フレームワークである。
  tags: [decomposition, delegation, subagents, synthesis]

- id: f07
  title: 反復手順と外部能力の分離
  type: framework
  source_chapter: See what Codex CLI can do
  source_quote: |
    "Package repeatable instructions as skills, then add plugins to connect Codex to your team's tools and data without leaving the CLI."
  summary: |
    再利用したい作業では、反復可能な指示をskillsとしてまとめ、チームのツールやデータ
    への接続はpluginsとして追加する。手順の再利用と外部能力への接続を別の層として
    捉え、必要な層だけを組み合わせる拡張設計である。
  tags: [skills, plugins, reuse, integration]

- id: f08
  title: 変更とレビューの職務分離
  type: framework
  source_chapter: See what Codex CLI can do
  source_quote: |
    "Run a dedicated review against uncommitted changes, a commit, or a base branch. Codex reports prioritized findings without modifying your working tree, so you can address risks before you commit or open a pull request."
  summary: |
    実装とは別に専用レビューを走らせ、未コミット差分、コミット、基準ブランチのいずれかを
    明示して検査する。レビュー中は作業ツリーを変更せず、優先順位付きの指摘を得て、
    コミットまたはPR作成前にリスクへ対処する検査フローである。
  tags: [code-review, separation-of-duties, risk, pre-ship]
