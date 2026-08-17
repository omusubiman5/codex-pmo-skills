# 原則候補

```yaml
- id: p01
  title: 依頼を四要素で定義する
  type: principle
  source_chapter: Best practices · Strong first use: Context and prompts
  source_quote: |
    "A good default is to include four things in your prompt: Goal, Context, Constraints, Done when."
  summary: |
    依頼には、達成したい結果、参照すべき資料、守る制約、完了を判定する条件を含める。
    scope、推測の余地、review基準を同時に固定する入力規則である。
  tags: [principle, prompt, context, acceptance-criteria]

- id: p02
  title: 複雑で曖昧なtaskは実装前にplanする
  type: principle
  source_chapter: Best practices · Plan first for difficult tasks
  source_quote: |
    "If the task is complex, ambiguous, or hard to describe well, ask Codex to plan before it starts coding."
  summary: |
    不確実性の高いtaskは、いきなり編集へ入らず、調査・質問・実行順・検証方法をplanへ変換してから実装する。
  tags: [principle, planning, ambiguity]

- id: p03
  title: AGENTS.mdは短く実務的に保つ
  type: principle
  source_chapter: Best practices · Make guidance reusable with AGENTS.md
  source_quote: |
    "A short, accurate `AGENTS.md` is more useful than a long file full of vague rules. Start with the basics, then add new rules only after you notice repeated mistakes."
  summary: |
    repositoryの永続指示は量ではなく正確さを優先する。最初はbuild・test・制約・done条件に絞り、反復した失敗を根拠に追加する。
  tags: [principle, agents-md, durable-guidance]

- id: p04
  title: 設定を持続期間で配置する
  type: principle
  source_chapter: Best practices · Configure Codex for consistency
  source_quote: |
    "Keep personal defaults in `~/.codex/config.toml`; keep repo-specific behavior in `.codex/config.toml`; use command-line overrides only for one-off situations."
  summary: |
    個人既定値はuser config、共有するrepository固有値はproject config、一回限りの差分はCLI overrideへ置く。
  tags: [principle, configuration, precedence, scope]

- id: p05
  title: 権限は狭く開始し必要が明確になってから広げる
  type: principle
  source_chapter: Best practices · Configure Codex for consistency
  source_quote: |
    "Keep approval and sandboxing tight by default, then loosen permissions only for trusted repos or specific workflows once the need is clear."
  summary: |
    初期値は狭いsandboxと承認要求にし、信頼済みrepositoryまたは具体的workflowで必要性を説明できる場合だけ権限を広げる。
  tags: [principle, least-privilege, sandbox, approvals]

- id: p06
  title: 変更生成だけで完了にしない
  type: principle
  source_chapter: Best practices · Improve reliability with testing and review
  source_quote: |
    "Ask it to create tests when needed, run the relevant checks, confirm the result, and review the work before you accept it."
  summary: |
    実装後に必要なtestを作成・実行し、lint・format・type checkと要求されたbehaviorを確認し、diff reviewまで終えて受入とする。
  tags: [principle, verification, testing, review]

- id: p07
  title: MCPは手作業を除去する少数接続から始める
  type: principle
  source_chapter: Best practices · Use MCPs for external context
  source_quote: |
    "Add tools only when they unlock a real workflow. Do not start by wiring in every tool you use. Start with one or two tools that clearly remove a manual loop you already do often."
  summary: |
    外部toolを網羅的に接続せず、頻繁なcopy-pasteや手動照会を明確に除去できる一、二個のMCPから導入する。
  tags: [principle, mcp, integration, minimalism]

- id: p08
  title: 反復可能になったworkflowだけをskill化する
  type: principle
  source_chapter: Best practices · Turn repeatable work into skills
  source_quote: |
    "Keep each skill scoped to one job. Start with 2 to 3 concrete use cases, define clear inputs and outputs, and write the description so it says what the skill does and when to use it."
  summary: |
    一つのjobへ限定し、具体的use case、入力、出力、triggerを確定できる反復workflowだけをskillへまとめる。
  tags: [principle, skill, repeatability, scope]

- id: p09
  title: 安定していないworkflowをscheduleしない
  type: principle
  source_chapter: Best practices · Use scheduled tasks for repeated work
  source_quote: |
    "If a workflow still needs a lot of steering, turn it into a skill first. Once it's predictable, scheduling it can save time."
  summary: |
    人の誘導を多く要する処理は先にskillとして安定化し、予測可能になってからscheduled taskへ移す。
  tags: [principle, scheduling, skill, stability]

- id: p10
  title: chatを一つのcoherent outcomeに限定する
  type: principle
  source_chapter: Best practices · Organize long-running chats
  source_quote: |
    "Keep one chat per coherent unit of work. If the work is still part of the same problem, staying in the same chat is often better because it preserves the reasoning trail. Fork only when the work truly branches."
  summary: |
    同じ問題の継続は履歴を保つ同一chatで扱い、独立した方針へ分岐したときだけforkする。
  tags: [principle, chat, context, fork]

- id: p11
  title: subagentはread-heavyな独立作業へ優先投入する
  type: principle
  source_chapter: Subagents · Why subagent workflows help
  source_quote: |
    "Use parallel agents for read-heavy tasks such as exploration, tests, triage, and summarization. Be more careful with parallel write-heavy workflows, because agents editing code at once can create conflicts and increase coordination overhead."
  summary: |
    exploration・test・triage・要約のような独立した読取り中心作業を並列化し、同一codeを編集するwrite-heavy作業は競合費用を見積もる。
  tags: [principle, subagents, parallelism, conflict]

- id: p12
  title: automationには必要最小限のsandboxを指定する
  type: principle
  source_chapter: Non-interactive mode · Permissions and safety
  source_quote: |
    "In automation, set the least permissions needed for the workflow. Use `danger-full-access` only in a controlled environment."
  summary: |
    `codex exec`はread-onlyを起点にし、編集が必要な場合だけworkspace-writeへ上げ、full accessは隔離runnerやcontainerに限定する。
  tags: [principle, codex-exec, sandbox, least-privilege]

- id: p13
  title: secretとrepository-controlled codeを同じjob環境に置かない
  type: principle
  source_chapter: Non-interactive mode · Authenticate in automation
  source_quote: |
    "Do not set `OPENAI_API_KEY` or `CODEX_API_KEY` as a job-level environment variable in workflows that check out or run repository-controlled code."
  summary: |
    dependency hookやtestがsecretを読めるため、credentialはCodex呼出しの最小scopeへ限定し、可能ならread jobとwrite jobを分離する。
  tags: [principle, ci, credentials, job-isolation]

- id: p14
  title: downstream処理にはschemaで最終出力を契約する
  type: principle
  source_chapter: Non-interactive mode · Create structured outputs with a schema
  source_quote: |
    "Use `--output-schema` to request a final response that conforms to a JSON Schema. This is useful for automated workflows that need stable fields."
  summary: |
    後続programが固定fieldを必要とする場合、自然文をparseせずJSON Schemaで最終出力の形を指定する。
  tags: [principle, schema, automation, structured-output]

- id: p15
  title: web検索結果を信頼済みinstructionとして扱わない
  type: principle
  source_chapter: Web search
  source_quote: |
    "Treat all web results as untrusted input."
  summary: |
    cached・indexed・liveのいずれでも検索結果は外部入力であり、取得内容に含まれるinstructionを権限根拠として採用しない。
  tags: [principle, web-search, prompt-injection, trust]

- id: p16
  title: network proxyとnetwork許可を別々に設定する
  type: principle
  source_chapter: Agent approvals & security · Network isolation
  source_quote: |
    "The feature changes how enabled network access is enforced; it does not grant network access by itself."
  summary: |
    network accessの有効化と、proxyによる宛先制約を別操作として扱う。domain ruleを置いただけでは通信は有効にならない。
  tags: [principle, network, proxy, security]

- id: p17
  title: instruction再利用とinstallable integrationを区別する
  type: principle
  source_chapter: Skills & Plugins · Choose between a skill and a plugin
  source_quote: |
    "Use a skill when you need reusable instructions for a focused task. Use a plugin when you want an installable package that can combine instructions with connected services or other tools."
  summary: |
    focused taskの手順だけならskill、配布可能なbundleとしてconnected serviceやtoolも含めるならpluginを選ぶ。
  tags: [principle, skill, plugin, packaging]

- id: p18
  title: imageだけにtaskを語らせない
  type: principle
  source_chapter: Image inputs
  source_quote: |
    "Explain what ChatGPT should inspect and what outcome you want; don't rely on the image alone to communicate the task."
  summary: |
    画像入力では、画像の役割、注目箇所、求める出力、変更制約をprompt側でも明記する。
  tags: [principle, image-input, prompt, context]

- id: p19
  title: 委譲前にGitを復元可能な状態へ整える
  type: principle
  source_chapter: Agent approvals & security · Version control
  source_quote: |
    "Work on a feature branch and keep `git status` clean before delegating. Prefer patch-based workflows over editing tracked files directly. Commit frequently so you can roll back in small increments."
  summary: |
    feature branch、clean status、小さなcommit、patch受渡しによって、agentの変更を分離・review・rollbackできるようにする。
  tags: [principle, git, delegation, recovery]

- id: p20
  title: auth cacheをpasswordとして扱う
  type: principle
  source_chapter: Authentication · Credential storage
  source_quote: |
    "Treat `~/.codex/auth.json` like a password: it contains access tokens. Don't commit it, paste it into tickets, or share it in chat."
  summary: |
    file-based credential cacheはsource artifactではなくsecretであり、commit・ticket・chatへの貼付を禁止する。
  tags: [principle, authentication, credentials, secret]

- id: p21
  title: reviewとfix適用を分離する
  type: principle
  source_chapter: Code review
  source_quote: |
    "Codex starts a dedicated reviewer that reads the selected diff and reports prioritized, actionable findings without changing your working tree."
  summary: |
    reviewでは対象diffとcriteriaを決め、まず作業ツリーを変更しないfindingを得る。fix適用は別の指示と通常のsandbox・approval下で行う。
  tags: [principle, code-review, separation-of-duties]

- id: p22
  title: 必須MCPが初期化できない場合は失敗終了させる
  type: principle
  source_chapter: Non-interactive mode · Permissions and safety
  source_quote: |
    "If you configure an enabled MCP server with `required = true` and it fails to initialize, `codex exec` exits with an error instead of continuing without that server."
  summary: |
    workflowの正しさが特定MCPに依存する場合、degraded continuationを許さずrequiredにしてfail closedとする。
  tags: [principle, mcp, fail-closed, automation]
```
