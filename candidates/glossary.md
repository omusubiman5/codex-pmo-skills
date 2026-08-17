# 用語候補

```yaml
- id: g01
  term: sandbox mode
  type: term
  source_chapter: Agent approvals & security · Sandbox and approvals
  author_definition: |
    "What Codex can do technically, for example, where it can write and whether it can reach the network."
  key_distinction: "approval policyとは別で、操作の技術的可能範囲をOSレベルで制限する。"
  why_it_matters: "安全設計で『できない』と『確認が必要』を混同しないため。"
  tags: [term, sandbox, security]

- id: g02
  term: approval policy
  type: term
  source_chapter: Agent approvals & security · Sandbox and approvals
  author_definition: |
    "When Codex must ask you before it executes an action."
  key_distinction: "操作自体を封じるsandboxではなく、実行前の承認時点を決める。"
  why_it_matters: "同じsandboxでも自動性を別々に調整できる。"
  tags: [term, approvals, security]

- id: g03
  term: network proxy
  type: term
  source_chapter: Agent approvals & security · Network isolation
  author_definition: |
    "Constrains traffic to the network policy you configure when command network access is already enabled."
  key_distinction: "network accessを付与せず、既に許可されたcommand trafficの宛先を制約する。"
  why_it_matters: "domain ruleだけで通信が有効または全経路が制限されるという誤解を防ぐ。"
  tags: [term, network, proxy]

- id: g04
  term: web search
  type: term
  source_chapter: Web search · Configure local web search
  author_definition: |
    "A hosted tool, separate from sandboxed local command networking."
  key_distinction: "command network proxyやallowlistとは別経路で、cached・indexed・live modeを持つ。"
  why_it_matters: "networkを切ってもsearchが使える場合があり、別policyが必要になる。"
  tags: [term, web-search, trust-boundary]

- id: g05
  term: codex exec
  type: term
  source_chapter: Non-interactive mode
  author_definition: |
    "Run Codex from scripts without opening the interactive TUI."
  key_distinction: "人がturnを誘導するTUIではなく、CI・pipeline・CLI chain向けの非対話入口。"
  why_it_matters: "無人実行のsandbox、auth、output contractを設計する基点。"
  tags: [term, codex-exec, automation]

- id: g06
  term: JSONL output
  type: term
  source_chapter: Non-interactive mode · Make output machine-readable
  author_definition: |
    "A JSON Lines stream so you can capture every event Codex emits while it's running."
  key_distinction: "最終JSON一個ではなく、thread・turn・item・errorなどstate changeごとのevent stream。"
  why_it_matters: "進捗監視と最終データ取得を分ける必要がある。"
  tags: [term, jsonl, events]

- id: g07
  term: output schema
  type: term
  source_chapter: Non-interactive mode · Create structured outputs with a schema
  author_definition: |
    "Request a final response that conforms to a JSON Schema."
  key_distinction: "途中eventのJSONLではなく、最終responseのfield contract。"
  why_it_matters: "downstream処理が安定したfieldを必要とするときに使う。"
  tags: [term, json-schema, structured-output]

- id: g08
  term: AGENTS.md
  type: term
  source_chapter: Best practices · Make guidance reusable with AGENTS.md
  author_definition: |
    "An open-format README for agents that loads into context automatically."
  key_distinction: "一回のpromptではなく、global・repo・subdirectory階層に置く永続instruction。"
  why_it_matters: "繰り返すrepository規約を会話ごとの貼付から分離する。"
  tags: [term, agents-md, guidance]

- id: g09
  term: skill
  type: term
  source_chapter: Skills & Plugins
  author_definition: |
    "A reusable workflow that gives ChatGPT or Codex task-specific guidance."
  key_distinction: "一つのfocused task向けinstructionとresourceであり、installable integration全体ではない。"
  why_it_matters: "反復手順の再現性とtrigger精度を担う。"
  tags: [term, skill, workflow]

- id: g10
  term: plugin
  type: term
  source_chapter: Skills & Plugins
  author_definition: |
    "An installable bundle that can include skills, connectors, or both."
  key_distinction: "skill単体より広く、MCP-backed connectorやUIを含められる配布単位。"
  why_it_matters: "instruction再利用と外部接続を含む配布を選び分ける。"
  tags: [term, plugin, packaging]

- id: g11
  term: Model Context Protocol (MCP)
  type: term
  source_chapter: Model Context Protocol
  author_definition: |
    "Model Context Protocol connects models to tools and context."
  key_distinction: "静的に貼るcontextではなく、STDIOまたはHTTP serverを介したtool接続。"
  why_it_matters: "外部情報、認証、tool allow/deny、approvalを一体で扱う。"
  tags: [term, mcp, tools]

- id: g12
  term: subagent
  type: term
  source_chapter: Subagents · Core terms
  author_definition: |
    "A delegated agent that Codex starts to handle a specific task."
  key_distinction: "main chatの追加turnではなく、独立threadでbounded workを処理する。"
  why_it_matters: "parallelismだけでなくmain contextからnoiseを隔離する。"
  tags: [term, subagent, delegation]

- id: g13
  term: context pollution
  type: term
  source_chapter: Subagents · Why subagent workflows help
  author_definition: |
    "Useful information gets buried under noisy intermediate output."
  key_distinction: "context量の不足ではなく、logsや探索notesで重要情報が埋もれる状態。"
  why_it_matters: "subagentへoffloadする対象を判断する根拠になる。"
  tags: [term, context, noise]

- id: g14
  term: custom agent
  type: term
  source_chapter: Subagents · Custom agents
  author_definition: |
    "Standalone TOML files under personal or project-scoped agent directories."
  key_distinction: "spawnごとの一時指示ではなく、name・description・developer_instructionsを持つ再利用可能な専門agent。"
  why_it_matters: "model、reasoning、sandbox、MCP、skillsをroleごとに固定できる。"
  tags: [term, custom-agent, configuration]

- id: g15
  term: resume
  type: term
  source_chapter: Developer commands · codex resume
  author_definition: |
    "Continue an interactive session by ID or resume the most recent chat."
  key_distinction: "新規chatではなく既存transcriptと作業文脈を継続する。"
  why_it_matters: "同じ問題のreasoning trailを失わず再開する。"
  tags: [term, session, resume]

- id: g16
  term: fork
  type: term
  source_chapter: Developer commands · codex fork
  author_definition: |
    "Fork a previous interactive session into a new chat."
  key_distinction: "元transcriptを残しつつ新IDへ分岐し、代替方針を隔離する。"
  why_it_matters: "同じ問題の継続と、本当に分岐した作業を区別する。"
  tags: [term, session, fork]

- id: g17
  term: Codex cloud
  type: term
  source_chapter: Codex cloud
  author_definition: |
    "Run tasks in isolated cloud environments, work in parallel, and start work from the web, GitHub, Linear, or Slack."
  key_distinction: "local CLIのremote shellではなく、再現可能なenvironmentへtaskを委譲して後でdiffをreviewする面。"
  why_it_matters: "background・parallel・integration起点の仕事をlocal loopから分離する。"
  tags: [term, cloud, delegation]

- id: g18
  term: code review
  type: term
  source_chapter: Code review
  author_definition: |
    "A dedicated reviewer that reads the selected diff and reports prioritized, actionable findings without changing your working tree."
  key_distinction: "実装修正とは別turn・別役割で、対象diffを非変更で検査する。"
  why_it_matters: "生成と検査の職務分離を保つ。"
  tags: [term, review, diff]

- id: g19
  term: credential store
  type: term
  source_chapter: Authentication · Credential storage
  author_definition: |
    "`file`, `keyring`, or `auto` controls where the Codex CLI stores cached credentials."
  key_distinction: "login methodではなく、取得済みcredentialをローカルで保存する場所の選択。"
  why_it_matters: "auth.jsonのplaintext保存とOS keyringのsecurity tradeoffを扱う。"
  tags: [term, authentication, credentials]

- id: g20
  term: permission profile
  type: term
  source_chapter: Agent approvals & security · Network isolation
  author_definition: |
    "A named configuration that can extend workspace permissions and define network access and domain rules."
  key_distinction: "一回のflagではなく、sandbox・approval・networkを再利用可能なpolicyとして束ねる。"
  why_it_matters: "workflow別の安全設定を繰り返し適用できる。"
  tags: [term, permissions, profile]
```
