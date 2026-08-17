# Counter-example candidates — Codex CLI公式資料集

```yaml
- id: ce01
  title: Gitチェックポイントなしで変更を進める
  type: counter-example
  source_chapter: "Codex CLI · Getting started · Start your first task"
  source_quote: |
    "Create Git checkpoints before and after a task so you can revert changes."
  failure_mode: |
    タスク前後のGitチェックポイントを作らず、変更を戻すための基準点がないまま作業を進める。
  mechanism: |
    本文はチェックポイントを変更のrevertに使うものとしているため、作らなければその回復手段を確保できない。
  warning_signs:
    - タスク開始前のGitチェックポイントがない
    - タスク終了後のGitチェックポイントがない
  bound_to:
    - "変更を回復可能に保つ"
    - "Codex CLIでリポジトリを編集する"
  tags: [counter-example, git, checkpoint, recovery]

- id: ce02
  title: code reviewの排他的selectorを同時指定する
  type: counter-example
  source_chapter: "Developer commands · codex review"
  source_quote: |
    "`--uncommitted`, `--base`, `--commit`, and a custom `PROMPT` conflict with one another."
  failure_mode: |
    review対象を選ぶ排他的な引数を同時に与え、競合するCLI入力を作る。
  mechanism: |
    公式リファレンスが4種類のselectorは互いに競合すると明記している。
  warning_signs:
    - reviewコマンドに複数の対象selectorがある
    - "--title"を"--commit"なしで使っている
  bound_to:
    - "専用reviewerで差分を検証する"
  tags: [counter-example, cli, review, conflicting-flags]

- id: ce03
  title: 名前指定のsession削除を確認なしで強制する
  type: counter-example
  source_chapter: "Developer commands · codex delete"
  source_quote: |
    "Use `--force` only with a session UUID."
  failure_mode: |
    繰り返しまたは曖昧になり得るsession名を、確認なしで削除しようとする。
  mechanism: |
    UUIDと違って名前は反復・曖昧になり得るため、CLIはnamed sessionに確認を要求して誤削除を防ぐ。
  warning_signs:
    - "codex delete"の対象がUUIDではなく名前
    - 名前指定と"--force"を組み合わせようとしている
  bound_to:
    - "保存sessionを安全に管理する"
  tags: [counter-example, session, deletion, ambiguity]

- id: ce04
  title: 隔離VM外でapprovalとsandboxを迂回する
  type: counter-example
  source_chapter: "Developer commands · Flag combinations and safety tips"
  source_quote: |
    "avoid `--dangerously-bypass-approvals-and-sandbox` unless you are inside a dedicated sandbox VM."
  failure_mode: |
    専用sandbox VMではない環境でapprovalとsandboxを同時に迂回する。
  mechanism: |
    このflagは二つの保護層を外すため、公式資料は専用の隔離環境に利用を限定している。
  warning_signs:
    - "--dangerously-bypass-approvals-and-sandbox"を指定している
    - 実行環境が専用sandbox VMではない
  bound_to:
    - "sandboxとapprovalを分離して最小権限を設計する"
  tags: [counter-example, sandbox, approval, full-access]

- id: ce05
  title: 公開または信頼されない環境へCodex実行を露出する
  type: counter-example
  source_chapter: "Authentication · Sign in with an API key"
  source_quote: |
    "Don't expose Codex execution in untrusted or public environments."
  failure_mode: |
    API keyで動くCodexの実行入口を、信頼されない利用者や公開環境から呼べる状態にする。
  mechanism: |
    公式資料はprogrammatic workflowを認める一方、Codex実行そのものをuntrusted/public環境へ露出しないよう明示している。
  warning_signs:
    - 公開endpointからCodex CLIを起動できる
    - 呼出元の信頼境界が定義されていない
  bound_to:
    - "API key認証で自動化する"
  tags: [counter-example, authentication, public-exposure, untrusted]

- id: ce06
  title: auth.jsonを通常ファイルとして共有する
  type: counter-example
  source_chapter: "Authentication · Credential storage"
  source_quote: |
    "treat `~/.codex/auth.json` like a password"
  failure_mode: |
    auth.jsonをrepositoryへcommitしたり、ticketやchatへ貼り付けたり、他者と共有する。
  mechanism: |
    auth.jsonにはaccess tokenが含まれ、file storageでは平文ファイルとして保存されるため、漏えいはcredential漏えいになる。
  warning_signs:
    - auth.jsonがGitの追跡対象に入っている
    - ticketまたはchatへauth.jsonの内容を貼ろうとしている
    - credential storeではなくfile storageを使っている
  bound_to:
    - "認証情報を保存・移送する"
    - "headless環境へログイン情報を渡す"
  tags: [counter-example, credential, token, secret-leak]

- id: ce07
  title: AGENTS.mdを長く曖昧な規則で膨らませる
  type: counter-example
  source_chapter: "Best practices · Make guidance reusable with AGENTS.md"
  source_quote: |
    "A short, accurate `AGENTS.md` is more useful than a long file full of vague rules."
  failure_mode: |
    実用的で正確な指示より、曖昧な規則を大量にAGENTS.mdへ積み上げる。
  mechanism: |
    公式ガイドは短く正確な内容の方が有用であり、大きくなった場合はtask別Markdownへ分離するよう勧めている。
  warning_signs:
    - AGENTS.mdに具体的な実行方法や検証条件がない
    - task固有の長い説明がmain fileへ集中している
  bound_to:
    - "repository guidanceをAGENTS.mdへ持続化する"
  tags: [counter-example, agents-md, vague-rules, context]

- id: ce08
  title: 生成した変更を検証せず受け入れる
  type: counter-example
  source_chapter: "Best practices · Improve reliability with testing and review"
  source_quote: |
    "Don’t stop at asking Codex to make a change."
  failure_mode: |
    Codexに変更だけを依頼し、tests・関連checks・behavior確認・diff reviewを経ずに受け入れる。
  mechanism: |
    ガイドは信頼性向上のloopとして、変更後のtest、check、結果確認、reviewを明示している。
  warning_signs:
    - Done whenにtestやbehavior確認がない
    - 変更後にdiffを見ていない
    - lint、format、type checkの対象が未定義
  bound_to:
    - "変更の完了条件を契約化する"
    - "testsとreviewで受入判定する"
  tags: [counter-example, validation, testing, review]

- id: ce09
  title: 実ワークフローなしに外部toolを一括接続する
  type: counter-example
  source_chapter: "Best practices · Use MCPs for external context"
  source_quote: |
    "Do not start by wiring in every tool you use."
  failure_mode: |
    解消したい反復作業を特定せず、利用中のtoolを最初からすべてMCP等で接続する。
  mechanism: |
    ガイドはmanual loopを明確に除く一、二個のtoolから始め、必要に応じて拡張する順序を示している。
  warning_signs:
    - 各toolが解消するmanual loopを説明できない
    - 初回導入で多数のtoolを同時追加する
  bound_to:
    - "MCPで外部contextとtoolを接続する"
  tags: [counter-example, mcp, tool-sprawl, integration]

- id: ce10
  title: skill初版で全edge caseを覆おうとする
  type: counter-example
  source_chapter: "Best practices · Turn repeatable work into skills"
  source_quote: |
    "Don’t try to cover every edge case up front."
  failure_mode: |
    代表taskを動かして反復する前に、skill初版へあらゆるedge caseと補助資産を詰め込む。
  mechanism: |
    ガイドは一つの代表taskから開始し、動作を確認してからskill化・改善し、scriptやassetは信頼性を上げる場合だけ加えるとしている。
  warning_signs:
    - 代表use caseがまだ実行確認されていない
    - reliabilityへの寄与を説明できないscriptやassetがある
    - 一つのjobを越えるscopeを持つ
  bound_to:
    - "反復workflowをskill化する"
  tags: [counter-example, skill, overengineering, scope]

- id: ce11
  title: 手動で不安定なworkflowをscheduleする
  type: counter-example
  source_chapter: "Best practices · Use scheduled tasks for repeated work"
  source_quote: |
    "Scheduling a recurring task before it’s reliable manually"
  failure_mode: |
    人のsteeringを多く必要とし、手動でも予測可能になっていないworkflowを定期実行へ移す。
  mechanism: |
    ガイドはまずmethodをskillとして安定させ、predictableになってからscheduleする順序を示している。
  warning_signs:
    - 毎回多くのsteeringが要る
    - 手動実行の結果が安定していない
    - methodがskill等へ固定されていない
  bound_to:
    - "安定したworkflowをscheduled taskへ移す"
  tags: [counter-example, scheduling, automation, reliability]

- id: ce12
  title: 同じfile群でlive taskを並行実行する
  type: counter-example
  source_chapter: "Best practices · Common mistakes"
  source_quote: |
    "Running live tasks on the same files without using Git worktrees"
  failure_mode: |
    Git worktreeで作業領域を分離せず、同じfile群に対するlive taskを同時実行する。
  mechanism: |
    公式ガイドはこれをcommon mistakeとして列挙し、subagent資料は同時編集がconflictとcoordination overheadを増やすと説明している。
  warning_signs:
    - 複数taskが同じworking treeを使う
    - 編集対象fileがtask間で重なる
  bound_to:
    - "作業を並列化する"
    - "Git worktreeで変更を隔離する"
  tags: [counter-example, parallelism, worktree, conflict]

- id: ce13
  title: プロジェクト全体を一つのchatへ詰め込む
  type: counter-example
  source_chapter: "Best practices · Common mistakes"
  source_quote: |
    "This leads to bloated context and worse results over time"
  failure_mode: |
    coherent outcomeごとにchatを分けず、一つのchatをプロジェクト全体に使い続ける。
  mechanism: |
    ガイドはchatがcontext・decision・actionを蓄積し、project-wideな一chatはcontext肥大と結果悪化を招くと明記している。
  warning_signs:
    - 一つのchatに複数の独立outcomeが混在する
    - 作業が分岐してもforkしていない
  bound_to:
    - "chatをresume・fork・compactする"
  tags: [counter-example, chat, context-bloat, quality]

- id: ce14
  title: 非隔離環境でdanger-full-accessを使う
  type: counter-example
  source_chapter: "Non-interactive mode · Permissions and safety"
  source_quote: |
    "Use `danger-full-access` only in a controlled environment"
  failure_mode: |
    isolated CI runnerやcontainer等のcontrolled environmentではない場所で、自動実行に広範なaccessを与える。
  mechanism: |
    非対話実行では人が途中確認できないため、公式資料はleast permissionsを原則とし、full accessをcontrolled environmentに限定している。
  warning_signs:
    - "--sandbox danger-full-access"を指定している
    - runnerまたはcontainerの隔離境界がない
  bound_to:
    - "codex execを最小権限で自動化する"
  tags: [counter-example, automation, sandbox, full-access]

- id: ce15
  title: repository codeとjob-level API keyを同居させる
  type: counter-example
  source_chapter: "Non-interactive mode · CI/CD"
  source_quote: |
    "Do not set `OPENAI_API_KEY` or `CODEX_API_KEY` as a job-level environment variable"
  failure_mode: |
    repository-controlled codeをcheckoutまたは実行するjob全体へAPI keyをenvironment variableとして公開する。
  mechanism: |
    同じjobのbuild script、test、dependency lifecycle hook、compromised actionがjob-level environment variableを読める。
  warning_signs:
    - API keyがjob-level envに設定されている
    - 同じjobでrepository-controlled codeを実行する
    - untrusted codeとcodex execが同じprocess environmentを共有する
  bound_to:
    - "CIでCodexを認証する"
    - "credentialとwrite権限をjob分離する"
  tags: [counter-example, ci, api-key, credential-exposure]

- id: ce16
  title: public repositoryでCodex account auth cacheを使う
  type: counter-example
  source_chapter: "Non-interactive mode · Codex account authentication"
  source_quote: |
    "Do not use this workflow for public or open-source repositories."
  failure_mode: |
    publicまたはopen-source repositoryのautomationに、永続化・更新されるauth.jsonを使うCodex account認証workflowを持ち込む。
  mechanism: |
    auth.jsonはaccess tokenを含むpassword相当のcacheであり、資料はAPI keyをautomationの推奨defaultとしている。
  warning_signs:
    - repositoryがpublicまたはopen source
    - runner間でauth.jsonを永続化する
  bound_to:
    - "CI/CDの認証方式を選ぶ"
  tags: [counter-example, ci, auth-json, public-repository]

- id: ce17
  title: 安全確認なしにGit repository checkを飛ばす
  type: counter-example
  source_chapter: "Non-interactive mode · Git repository required"
  source_quote: |
    "Codex requires commands to run inside a Git repository to prevent destructive changes."
  failure_mode: |
    環境の安全性を確認せず、"--skip-git-repo-check"でGit repository要件を迂回する。
  mechanism: |
    このcheckはdestructive changesを防ぐためのもので、公式資料はenvironmentがsafeだと確信できる場合だけoverrideを認めている。
  warning_signs:
    - "--skip-git-repo-check"を指定している
    - 実行場所にGitの復元・差分確認手段がない
  bound_to:
    - "codex execを安全な作業領域で実行する"
  tags: [counter-example, git, automation, destructive-change]

- id: ce18
  title: 画像だけにtask意図を託す
  type: counter-example
  source_chapter: "Image inputs · Add images to your prompt"
  source_quote: |
    "don't rely on the image alone to communicate the task."
  failure_mode: |
    screenshotやdiagramだけを渡し、何を調べ、どの結果を求めるかを文章で示さない。
  mechanism: |
    画像はvisual contextであり、資料はinspect対象とdesired outcomeを別途説明するよう求めている。
  warning_signs:
    - promptが画像添付だけで構成される
    - inspect対象または期待結果が書かれていない
  bound_to:
    - "画像をtask contextとして追加する"
  tags: [counter-example, image-input, context, ambiguity]

- id: ce19
  title: write-heavy taskをsubagentで同時編集する
  type: counter-example
  source_chapter: "Subagents · Benefits"
  source_quote: |
    "agents editing code at once can create conflicts and increase coordination overhead."
  failure_mode: |
    書込み対象が重なるworkを複数subagentへ同時委譲する。
  mechanism: |
    同時code editingはconflictを作り、結果をまとめるためのcoordination overheadを増やす。
  warning_signs:
    - 複数subagentが同じfileを編集する
    - task境界がread-heavyではなくwrite-heavy
    - 統合担当と順序が定義されていない
  bound_to:
    - "boundedなsubagentへ独立作業を委譲する"
  tags: [counter-example, subagent, parallel-write, conflict]

- id: ce20
  title: 非対話subagentに新規approval必須actionを任せる
  type: counter-example
  source_chapter: "Subagents · Approvals and sandbox controls"
  source_quote: |
    "an action that needs new approval fails"
  failure_mode: |
    fresh approvalを表示できないnon-interactive flowへ、実行中に新規approvalが必要となるactionを配置する。
  mechanism: |
    approvalを新たに提示できないrunではactionが失敗し、errorがparent workflowへ返る。
  warning_signs:
    - flowがnon-interactive
    - delegated actionがsandbox外操作または新規approvalを必要とする
  bound_to:
    - "subagent workflowの権限を設計する"
  tags: [counter-example, subagent, approval, non-interactive]

- id: ce21
  title: web検索結果を信頼済み入力として扱う
  type: counter-example
  source_chapter: "Web search · Overview and cached search"
  source_quote: |
    "Treat all web results as untrusted input."
  failure_mode: |
    liveまたはcachedのweb結果に含まれる指示を、検証せずagentの命令として扱う。
  mechanism: |
    cached modeもprompt injection riskを低減するだけで除去せず、web結果はすべてuntrusted inputとされる。
  warning_signs:
    - web本文の命令をそのまま実行する
    - cached searchだから安全だとみなす
  bound_to:
    - "web searchで最新contextを取得する"
  tags: [counter-example, web-search, prompt-injection, untrusted-input]

- id: ce22
  title: search domain filterで他の通信経路も制限したつもりになる
  type: counter-example
  source_chapter: "Web search · Configure web search"
  source_quote: |
    "Search-domain filters do not restrict local command traffic, apps, connectors, or MCP servers."
  failure_mode: |
    web search用domain filterを設定しただけで、local command、apps、connectors、MCPの通信も制限されたと判断する。
  mechanism: |
    web searchはsandboxed local command networkingとは別のhosted toolで、各経路は別々のcontrolを使う。
  warning_signs:
    - web search allowlistだけでegress全体を管理している
    - command networkやMCPのpolicyが未設定
  bound_to:
    - "外部通信経路を分離して制御する"
  tags: [counter-example, web-search, network, policy-gap]

- id: ce23
  title: domain ruleだけでcommand network proxyが有効だと思う
  type: counter-example
  source_chapter: "Agent approvals & security · Network access"
  source_quote: |
    "Adding domain rules does not enable the proxy by itself."
  failure_mode: |
    network_proxy featureを有効にせずdomain allow ruleだけを書き、command trafficが制約されたとみなす。
  mechanism: |
    proxy featureを省略するとcommandはdirect network accessを使い、allow ruleはdestinationを制限しない。
  warning_signs:
    - domain ruleはあるがnetwork_proxy featureがoff
    - command network accessがonでdirect trafficを許している
  bound_to:
    - "command networkをdomain policyで制御する"
  tags: [counter-example, network-proxy, allowlist, misconfiguration]

- id: ce24
  title: global wildcardを狭いallowlistとして扱う
  type: counter-example
  source_chapter: "Agent approvals & security · Domain rules"
  source_quote: |
    "Treat `*` as broad network access"
  failure_mode: |
    global "*" allow ruleをscopeされたdomain許可と同等に扱う。
  mechanism: |
    global wildcardはdenyされていない任意のpublic hostへmatchするため、broad network accessになる。
  warning_signs:
    - allow ruleにglobal "*"がある
    - 必要hostを列挙していない
  bound_to:
    - "network domain allowlistを最小化する"
  tags: [counter-example, network, wildcard, broad-access]

- id: ce25
  title: CodexのDNS checkだけでhostile DNSを完全防御する
  type: counter-example
  source_chapter: "Agent approvals & security · DNS rebinding protections"
  source_quote: |
    "The check reduces DNS rebinding risk, but it does not eliminate it."
  failure_mode: |
    hostile DNSがthreat modelに入る環境で、Codexのbest-effort DNS/IP classificationだけを防御にする。
  mechanism: |
    classificationはrebinding riskを除去せず、完全防止にはtransport layerでのresolved IP pinningが必要とされる。
  warning_signs:
    - hostile DNSが想定される
    - lower-layer egress controlがない
  bound_to:
    - "network proxyでegressを制御する"
  tags: [counter-example, dns-rebinding, network, defense-in-depth]

- id: ce26
  title: trust boundary拡大型network設定を通常環境で使う
  type: counter-example
  source_chapter: "Agent approvals & security · Dangerous settings"
  source_quote: |
    "Two settings deliberately widen the trust boundary"
  failure_mode: |
    tightly controlled environmentではない場所で、non-loopback proxy公開または全Unix socket許可を有効にする。
  mechanism: |
    一方はproxy listenerをloopback外へ露出し、他方はUnix socket allowlistを迂回する。
  warning_signs:
    - dangerously_allow_non_loopback_proxyがtrue
    - dangerously_allow_all_unix_socketsがtrue
  bound_to:
    - "sandboxed networkのtrust boundaryを維持する"
  tags: [counter-example, network-proxy, unix-socket, trust-boundary]

- id: ce27
  title: command network proxyで全通信面をfilterしたつもりになる
  type: counter-example
  source_chapter: "Agent approvals & security · Traffic outside the command network proxy"
  source_quote: |
    "It does not filter web search, app or connector tool calls, MCP server connections"
  failure_mode: |
    local command sandboxのproxyだけを設定し、web search、apps、connectors、MCP、browser、cloud等も同じfilter下にあるとみなす。
  mechanism: |
    command proxyがfilterするのはsandbox内のscript、program、child processで、他surfaceは別のservice connectionやpolicyを使う。
  warning_signs:
    - command proxy以外のsurface controlが未設定
    - MCPやweb searchを同じdomain ruleで制御できると想定する
  bound_to:
    - "外部接続surfaceごとにpolicyを構成する"
  tags: [counter-example, network-proxy, mcp, connectors]

- id: ce28
  title: 悪意あるrepositoryをfull-access devcontainerで開く
  type: counter-example
  source_chapter: "Agent approvals & security · Run Codex in Dev Containers"
  source_quote: |
    "a malicious project can exfiltrate anything available inside the devcontainer"
  failure_mode: |
    trustedでないrepositoryを、Codex credential等を持つdevcontainer内でdanger-full-accessまたはsandbox bypass付きで実行する。
  mechanism: |
    containerは全攻撃を防がず、malicious projectはcontainer内で利用可能なものをCodex credentialを含めてexfiltrateできる。
  warning_signs:
    - repositoryがtrustedではない
    - container内にCodex credentialがある
    - container内でdanger-full-accessまたはbypass flagを使う
  bound_to:
    - "containerを外側の隔離境界として使う"
  tags: [counter-example, devcontainer, exfiltration, credential]

- id: ce29
  title: telemetryを非機密データとして無制御に送る
  type: counter-example
  source_chapter: "Agent approvals & security · Security and privacy guidance"
  source_quote: |
    "Treat tool arguments and outputs as sensitive."
  failure_mode: |
    prompt、tool argument、tool outputを機密性のないtelemetryとして、管理外collectorへ無期限・無redactionで送る。
  mechanism: |
    promptにはsource codeやsensitive dataが含まれ得るため、公式資料はprompt loggingを既定offに保ち、管理下collector、retention、access control、redactionを求めている。
  warning_signs:
    - log_user_promptがpolicy承認なしにtrue
    - collectorを自組織がcontrolしていない
    - retention limitまたはredactionがない
  bound_to:
    - "OTelでCodexを観測する"
  tags: [counter-example, telemetry, privacy, sensitive-data]
```
