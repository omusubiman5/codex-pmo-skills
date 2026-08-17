- id: f01
  title: Goal・Context・Constraints・Done whenによる依頼設計
  type: framework
  source_chapter: "Best practices — Strong first use: Context and prompts"
  source_quote: |
    "A good default is to include four things in your prompt: Goal: What are you trying to change or build? Context: Which files, folders, docs, examples, or errors matter for this task? Constraints: What standards, architecture, safety requirements, or conventions should Codex follow? Done when: What should be true before the task is complete, such as tests passing, behavior changing, or a bug no longer reproducing?"
  summary: |
    依頼を目標、必要な文脈、守るべき制約、完了判定の四要素へ分解する。
    作業範囲と受入条件を同時に渡すことで、暗黙の推測を減らし、実装後の
    判定とレビューまで同じ契約に基づいて進めるための入力設計である。
  tags: [prompting, context, constraints, acceptance-criteria]

- id: f02
  title: 複雑・曖昧タスクのplan-first切替
  type: framework
  source_chapter: "Best practices — Plan first for difficult tasks"
  source_quote: |
    "If the task is complex, ambiguous, or hard to describe well, ask Codex to plan before it starts coding."
    "Plan mode lets Codex gather context, ask clarifying questions, and build a stronger plan before implementation."
  summary: |
    複雑さ、曖昧さ、説明困難性を検知したら、実装を始めず計画へ切り替える。
    文脈収集、確認質問、仮定の検査を先に行い、検証可能な実装手順へ変換してから
    コード変更へ進む判断フレームワークである。
  tags: [planning, ambiguity, clarification, implementation]

- id: f03
  title: 実摩擦から持続的ガイダンスへ昇格する学習ループ
  type: framework
  source_chapter: "Best practices — Make guidance reusable with AGENTS.md"
  source_quote: |
    "Keep it practical. A short, accurate `AGENTS.md` is more useful than a long file full of vague rules. Start with the basics, then add new rules only after you notice repeated mistakes."
    "When Codex makes the same mistake twice, ask it for a retrospective and update `AGENTS.md`."
  summary: |
    最初から網羅的規則を作らず、最小限の正確な指示で運用を始める。同じ失敗が
    再発した時点で振り返りを行い、原因に対応する指示だけをAGENTS.mdへ追加する。
    実際の摩擦を観測して持続知識を育てるフィードバックループである。
  tags: [agents-md, feedback-loop, durable-guidance, retrospective]

- id: f04
  title: 変更頻度と適用範囲による設定層の選択
  type: framework
  source_chapter: "Best practices — Configure Codex for consistency"
  source_quote: |
    "Keep personal defaults in `~/.codex/config.toml` (Settings > Configuration > Open config.toml in the ChatGPT desktop app)"
    "Keep repo-specific behavior in `.codex/config.toml`"
    "Use command-line overrides only for one-off situations (if you use the CLI)"
  summary: |
    個人に恒常的な既定値、リポジトリ固有の共有動作、一度限りの例外を区別し、
    それぞれユーザー設定、プロジェクト設定、コマンドライン上書きへ配置する。
    設定の寿命と共有範囲を一致させて、セッション間の一貫性と例外の局所性を保つ。
  tags: [configuration, scope, precedence, consistency]

- id: f05
  title: 生成・検証・レビューの完了ループ
  type: framework
  source_chapter: "Best practices — Improve reliability with testing and review"
  source_quote: |
    "Don’t stop at asking Codex to make a change. Ask it to create tests when needed, run the relevant checks, confirm the result, and review the work before you accept it."
  summary: |
    コード生成を終点にせず、必要なテストの追加、関連チェックの実行、要求された
    挙動の確認、差分レビューを一連の受入ループとして扱う。promptまたはAGENTS.mdで
    「良い結果」を定義し、その基準を満たすまで完了としない。
  tags: [verification, testing, review, done-criteria]

- id: f06
  title: 対話・自動化・cloudの実行形態選択
  type: framework
  source_chapter: "Codex CLI — Use Codex CLI when… / Codex cloud — Use Codex cloud when…"
  source_quote: |
    "You work from the terminal: Explore, edit, and run a repository in one focused loop."
    "You need scripting or CI: Run a non-interactive command in a repeatable workflow."
    "Work needs to run in the background: Delegate a longer task and return when it is ready."
  summary: |
    人が同じ場で反復して誘導する作業には対話型CLI、再現可能なpipelineには
    codex exec、長時間・並列・不在時の委譲にはcloudを選ぶ。機能の多寡ではなく、
    人の関与、反復性、隔離環境、結果を受け取る時点を判断軸にする。
  tags: [execution-mode, interactive, automation, cloud]

- id: f07
  title: 非対話実行の入出力契約化
  type: framework
  source_chapter: "Non-interactive mode — Basic usage / Make output machine-readable / Create structured outputs with a schema"
  source_quote: |
    "While `codex exec` runs, Codex streams progress to `stderr` and prints only the final agent message to `stdout`."
    "When you enable `--json`, `stdout` becomes a JSON Lines (JSONL) stream so you can capture every event Codex emits while it's running."
    "Use `--output-schema` to request a final response that conforms to a JSON Schema."
  summary: |
    自動化では進捗と最終結果の経路を分け、必要に応じて状態変化をJSONLで記録し、
    downstreamへ渡す最終値をJSON Schemaで拘束する。人向け文章への依存を減らし、
    観測、解析、受入判定を機械処理可能な契約へ変える。
  tags: [automation, jsonl, schema, interface-contract]

- id: f08
  title: CI修正の権限分離とpatch受け渡し
  type: framework
  source_chapter: "Non-interactive mode — Common automation patterns — Example: Autofix CI failures in GitHub Actions"
  source_quote: |
    "Check out the failing commit with repository read permissions only."
    "Save Codex's local changes as a patch artifact."
    "In a separate job, apply the patch and open a pull request."
  summary: |
    失敗再現と修正生成を読み取り権限のjobで行い、その成果をpatch artifactとして
    隔離する。別jobだけに書き込み権限を与えてpatchを適用しPRを作ることで、
    model/API credentialを持つ工程とrepositoryへ書く工程を分離する。
  tags: [ci, least-privilege, patch, separation-of-duties]

- id: f09
  title: sandboxとapprovalの二層境界設計
  type: framework
  source_chapter: "Agent approvals & security — Sandbox and approvals"
  source_quote: |
    "Codex security controls come from two layers that work together:"
    "Sandbox mode: What Codex can do technically (for example, where it can write and whether it can reach the network) when it executes model-generated commands."
    "Approval policy: When Codex must ask you before it executes an action (for example, leaving the sandbox, using the network, or running commands outside a trusted set)."
  summary: |
    実行可能性を強制するsandboxと、実行前に誰の確認を要するかを決めるapprovalを
    別の制御層として設計する。まず技術的な到達範囲を最小化し、その境界を越える操作や
    副作用のある操作へ承認点を配置して、能力と自律性を混同しない。
  tags: [sandbox, approvals, security-boundary, least-privilege]

- id: f10
  title: command networkの許可・制約二段階モデル
  type: framework
  source_chapter: "Agent approvals & security — Network access — Network isolation"
  source_quote: |
    "The feature changes how enabled network access is enforced; it does not grant network access by itself."
    "Network on + `network_proxy` on: network stays on, and outbound traffic is constrained by the configured network policy."
  summary: |
    commandのnetwork accessを与える判断と、その通信先をproxy policyで絞る判断を
    分離する。accessがoffならproxyは能力を追加せず、accessがonかつproxyがoffなら
    制約されないため、許可と宛先制限の両方を明示的に成立させる。
  tags: [network, proxy, allowlist, layered-control]

- id: f11
  title: 複数通信経路を個別統制する脅威モデル
  type: framework
  source_chapter: "Agent approvals & security — Network access — Traffic outside the command network proxy"
  source_quote: |
    "The network proxy filters scripts, programs, and child processes that run inside the local command sandbox. It does not filter web search, app or connector tool calls, MCP server connections, browser or Computer Use activity, Codex cloud tasks, or the client's model and authentication requests."
  summary: |
    外部通信を一つのnetwork設定と見なさず、sandbox内command、web search、apps、
    MCP、browser/computer use、cloud、model/authを別経路として列挙する。各経路に
    対応するfeature設定、tool policy、workspace policy、環境境界を個別に適用する。
  tags: [threat-model, network-paths, mcp, web-search]

- id: f12
  title: currentnessとprompt-injectionリスクによる検索モード選択
  type: framework
  source_chapter: "Web search — Configure local web search"
  source_quote: |
    "Cached mode uses an OpenAI-maintained index instead of fetching arbitrary pages live, which lowers—but doesn't remove—prompt injection risk."
    "Use live search when your task depends on the latest information."
  summary: |
    最新性が必須かを先に判定し、必須ならlive search、不要ならcached/indexed、
    外部情報が不要ならdisabledを選ぶ。検索結果は常に不信入力として扱いながら、
    currentnessの価値と任意ページ取得によるprompt injection露出を釣り合わせる。
  tags: [web-search, currentness, prompt-injection, risk]

- id: f13
  title: bounded subagentへの分解と要約再統合
  type: framework
  source_chapter: "Subagents — Why subagent workflows help"
  source_quote: |
    "Keep the main agent focused on requirements, decisions, and final outputs. Run specialized subagents in parallel for exploration, tests, or log analysis. Return summaries from subagents instead of raw intermediate output."
  summary: |
    main threadには要求、判断、最終成果を残し、探索、テスト、ログ解析のような
    独立した作業を境界付きsubagentへ分ける。中間出力をそのまま集めず要約で戻し、
    context pollutionを抑えながらmain agentが統合判断を行う。
  tags: [subagents, decomposition, synthesis, context-management]

- id: f14
  title: 読み書き比率による並列化判定
  type: framework
  source_chapter: "Subagents — Why subagent workflows help"
  source_quote: |
    "As a starting point, use parallel agents for read-heavy tasks such as exploration, tests, triage, and summarization. Be more careful with parallel write-heavy workflows, because agents editing code at once can create conflicts and increase coordination overhead."
  summary: |
    タスクを独立性だけでなくread-heavyかwrite-heavyかでも分類する。探索、テスト、
    triage、要約は並列化候補とし、同一コードへの編集が多い場合は競合と統合費用を
    見積もって直列化または編集領域の分離を選ぶ。
  tags: [parallelism, read-heavy, write-conflicts, coordination]

- id: f15
  title: subagent役割と計算資源の適合設計
  type: framework
  source_chapter: "Subagents — Choosing models and reasoning / Custom agents"
  source_quote: |
    "Different agents need different model and reasoning settings."
    "The best custom agents are narrow and opinionated. Give each one clear job, a tool surface that matches that job, and instructions that keep it from drifting into adjacent work."
  summary: |
    各subagentの仕事を狭く定義し、その曖昧さ、推論深度、速度要求に応じてmodelと
    reasoning effortを選ぶ。同時にjobへ必要なtool surfaceとsandboxだけを与え、
    隣接作業への逸脱をinstructionsで防ぐ役割・資源対応フレームワークである。
  tags: [subagents, model-selection, tool-surface, role-design]

- id: f16
  title: coherent outcome単位のsession分岐
  type: framework
  source_chapter: "Best practices — Organize long-running chats / Developer commands — codex resume and codex fork"
  source_quote: |
    "Keep one chat per coherent unit of work. If the work is still part of the same problem, staying in the same chat is often better because it preserves the reasoning trail. Fork only when the work truly branches."
  summary: |
    同じ問題の継続ならresumeまたは同一chatを使ってreasoning trailを保持し、別案や
    独立成果へ本当に分岐した時だけforkする。長大化した履歴はcompactし、無関係な
    outcomeにはnew chatを使うことで、連続性とcontext純度を両立する。
  tags: [session, resume, fork, context-management]

- id: f17
  title: 外部文脈の入口選択
  type: framework
  source_chapter: "Image inputs — Write the prompt around the image / Best practices — Use MCPs for external context / Codex CLI — Build a terminal workflow around Codex"
  source_quote: |
    "Explain what ChatGPT should inspect and what outcome you want; don't rely on the image alone to communicate the task."
    "Use MCP when: The needed context lives outside the repo; The data changes frequently; You want Codex to use a tool rather than rely on pasted instructions."
  summary: |
    足りない文脈の型を判定し、視覚的根拠には説明付きimage、最新の公開情報には
    web search、頻繁に変わる外部システムや操作にはMCP、過去の作業履歴にはresumeを
    選ぶ。入口を増やす前に、必要情報と望む出力を明示する。
  tags: [context, image, mcp, input-selection]

- id: f18
  title: repeatabilityと接続性によるskill・plugin選択
  type: framework
  source_chapter: "Skills & Plugins — Choose between a skill and a plugin"
  source_quote: |
    "Use a skill when you need reusable instructions for a focused task. Use a plugin when you want an installable package that can combine instructions with connected services or other tools."
  summary: |
    一つの反復taskに必要なのが指示とsupporting resourceならskillを選び、配布可能な
    bundleとして外部service、connector、MCP toolも組み合わせる必要があるなら
    pluginを選ぶ。手順の再利用と外部接続の要否を主要な分岐条件にする。
  tags: [skill, plugin, reuse, integration]

- id: f19
  title: 認証方式を利用面と統制境界へ対応させる
  type: framework
  source_chapter: "Authentication — OpenAI authentication / Use Codex access tokens for enterprise automation"
  source_quote: |
    "When you sign in with ChatGPT, Codex usage follows your ChatGPT workspace permissions, role-based access control (RBAC), and ChatGPT Enterprise retention and residency settings. With an API key, usage follows your API organization's retention and data-sharing settings instead."
  summary: |
    認証を単なるlogin手段ではなく、利用可能なsurface、課金、管理権限、保持・共有
    policyを選ぶ境界として扱う。対話的なworkspace利用はChatGPT、一般automationは
    API key、workspace統制が必要な信頼済みenterprise automationはaccess tokenを選ぶ。
  tags: [authentication, governance, api-key, access-token]

- id: f20
  title: 変更とレビューの職務分離
  type: framework
  source_chapter: "Code review — Start a review / Choose a review scope"
  source_quote: |
    "Codex starts a dedicated reviewer that reads the selected diff and reports prioritized, actionable findings without changing your working tree."
    "Choose one of these `/review` scopes: Review against a base branch; Review uncommitted changes; Review a commit; Custom review instructions."
  summary: |
    実装担当の変更処理からreviewを分離し、base branch差分、未コミット変更、特定commit、
    custom criteriaのいずれか一つへ検査対象を固定する。reviewerは作業ツリーを変更せず、
    優先順位付きfindingを返し、修正適用は別turnの権限境界で扱う。
  tags: [code-review, separation-of-duties, scope, findings]

- id: f21
  title: Gitを基盤にした回復可能な変更運用
  type: framework
  source_chapter: "Agent approvals & security — Version control / Codex CLI — Getting started"
  source_quote: |
    "Work on a feature branch and keep `git status` clean before delegating."
    "Prefer patch-based workflows (for example, `git diff`/`git apply`) over editing tracked files directly. Commit frequently so you can roll back in small increments."
  summary: |
    委譲前にcleanな作業状態とfeature branchを確保し、変更をdiffまたはpatchとして
    観測可能にする。小刻みなcommitとtask前後のcheckpointを置き、失敗時に狭い単位で
    戻せるようにしてからagentへ変更を任せる回復設計である。
  tags: [git, reversibility, checkpoint, patch]

- id: f22
  title: MCP接続の必須性・tool範囲・承認の三段階制御
  type: framework
  source_chapter: "Model Context Protocol — Connect Codex to an MCP server — Other configuration options"
  source_quote: |
    "`required` (optional): Set `true` to make startup fail if this enabled server can't initialize."
    "`enabled_tools` (optional): Tool allow list."
    "`default_tools_approval_mode` (optional): Default approval behavior for tools from this server."
  summary: |
    MCP serverごとに、接続できなければrunを失敗させる必須性、modelへ見せるtool集合、
    実行前承認の三点を独立して決める。依存関係の欠落を黙って許容せず、不要toolを
    隠し、副作用に応じた承認を置くことで外部能力をfail-closedに近づける。
  tags: [mcp, fail-closed, tool-policy, approvals]

- id: f23
  title: 安全側から必要分だけ権限を拡張する段階設計
  type: framework
  source_chapter: "Developer commands — Flag combinations and safety tips / Best practices — Configure Codex for consistency"
  source_quote: |
    "When you need to grant Codex write access to more directories, prefer `--add-dir` rather than forcing `--sandbox danger-full-access`."
    "Keep approval and sandboxing tight by default, then loosen permissions only for trusted repos or specific workflows once the need is clear."
  summary: |
    最初はdefaultまたはread-only/workspace-writeの狭い境界を使い、具体的な必要性が
    判明した時だけdirectory、network、commandの順に必要部分を追加する。全面解除を
    近道にせず、repositoryの信頼性とworkflowの要求に対応した最小差分で権限を広げる。
  tags: [least-privilege, permissions, incremental, trust]

- id: f24
  title: 安定化してから再利用・自動化する成熟度梯子
  type: framework
  source_chapter: "Best practices — Turn repeatable work into skills / Use scheduled tasks for repeated work"
  source_quote: |
    "Start with one representative task, get it working well, then turn that workflow into a skill and improve from there."
    "If a workflow still needs a lot of steering, turn it into a skill first. Once it’s predictable, scheduling it can save time."
  summary: |
    代表的な手動taskで手順を確立し、反復できる段階でskillへ固定し、入力と出力が
    予測可能になってからscheduleへ移す。人のsteeringが多い工程を早期に自動化せず、
    実行実績に応じて一回作業、再利用workflow、定期automationへ昇格させる。
  tags: [maturity-model, skill, scheduling, automation]
