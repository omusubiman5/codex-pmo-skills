# 段階4 独立盲検 B

## 判定条件

- 対象: `codex-sandbox-approval-boundary`、`codex-egress-surface-governance`、`codex-bounded-subagents`
- 候補: `INDEX.md` にある9件のskill、または `none`
- 参照: 対象3件の `SKILL.md`、`INDEX.md` のskill名と説明、各 `test-prompts.json` から構造化抽出した `id` と `prompt` のみ
- `would_trigger` は、その節の対象skillを発火するかを表す。

## codex-sandbox-approval-boundary

### should-trigger-01

- **prompt**: Codexにはworkspace内を書かせたいが、境界外commandは毎回確認したい。sandboxとapprovalを設計して。
- **selected_skill**: `codex-sandbox-approval-boundary`
- **would_trigger**: yes
- **reason**: workspace内のwrite能力と境界外commandの承認条件を、sandboxとapprovalの二層で直接設計する依頼だから。
- **if_triggered_action**: 必要なread/write/execute/network能力を範囲付きで棚卸しし、最小sandboxを選び、境界外commandをaskへ割り当てる。

### should-trigger-02

- **prompt**: 無人execをread-onlyから始め、必要なdirectoryだけwrite可能にしたい。
- **selected_skill**: `codex-sandbox-approval-boundary`
- **would_trigger**: yes
- **reason**: 無人実行におけるfilesystem能力の最小化と、限定directoryへのwrite許可が主題だから。
- **if_triggered_action**: read-onlyを起点に必要directoryだけへwrite範囲を広げ、途中approvalに依存しない停止条件も確認する。

### should-trigger-03

- **prompt**: このhostではLinux sandboxが使えない。danger-full-accessを安全に動かす隔離境界は？
- **selected_skill**: `codex-sandbox-approval-boundary`
- **would_trigger**: yes
- **reason**: host sandbox不足時の外側の隔離境界と `danger-full-access` の安全条件を問う依頼だから。
- **if_triggered_action**: Dev ContainerまたはVMをfilesystem/processの外側境界として設計し、秘密・mount・repository信頼性を含めて露出を最小化する。

### should-not-trigger-01

- **prompt**: search、MCP、direct HTTPのどの経路から外部送信できるか監査して。
- **selected_skill**: `codex-egress-surface-governance`
- **would_trigger**: no
- **reason**: 基礎的なnetwork能力や承認ではなく、複数の外向き通信surfaceを分解して監査する依頼だから。
- **if_triggered_action**: 対象skillでは実行せず、`codex-egress-surface-governance` でsurface inventoryと経路別controlを作る。

### should-not-trigger-02

- **prompt**: headless serverのloginをdevice codeとAPI keyのどちらにする？
- **selected_skill**: `codex-auth-boundary-selection`
- **would_trigger**: no
- **reason**: sandbox能力ではなく、利用面に適合する認証flowとcredential scopeの選択だから。
- **if_triggered_action**: 対象skillでは実行せず、`codex-auth-boundary-selection` でheadless環境の認証方式とcredential境界を比較する。

### edge-01

- **prompt**: VM内だからapprovalもsandboxも全部外してよい？
- **selected_skill**: `codex-sandbox-approval-boundary`
- **would_trigger**: yes
- **reason**: VMという外側境界を根拠にsandboxとapprovalを解除できるかという、まさに二層境界の妥当性判断だから。
- **if_triggered_action**: VMの隔離範囲、mount、secret、network、repository信頼性を確認し、必要能力だけを許す。VM内であることだけを全面解除の十分条件にはしない。

## codex-egress-surface-governance

### should-trigger-01

- **prompt**: searchのdomain filterを設定した。MCPとsandbox commandの通信も同じ制限を受ける？
- **selected_skill**: `codex-egress-surface-governance`
- **would_trigger**: yes
- **reason**: search、MCP、sandboxed commandという別surface間でdomain制約が共有されるかを監査する依頼だから。
- **if_triggered_action**: 各surfaceの有効化、宛先制約、approval、loggingを個別に確認し、search filterが他経路へ波及すると仮定しない。

### should-trigger-02

- **prompt**: package取得だけ許可したい。command network permissionとproxy allowlistをどう組み合わせる？
- **selected_skill**: `codex-egress-surface-governance`
- **would_trigger**: yes
- **reason**: command network能力の有効化と、proxyによる宛先限定を組み合わせる通信経路統制だから。
- **if_triggered_action**: sandboxed commandのnetwork permissionを必要範囲で有効にし、package取得先だけをproxy allowlistへ置き、迂回経路も検査する。

### should-trigger-03

- **prompt**: 料金情報にはlive searchが必要だがprompt injectionが心配。取得経路を安全設計して。
- **selected_skill**: `codex-egress-surface-governance`
- **would_trigger**: yes
- **reason**: 情報鮮度のためのlive searchと、untrusted web inputによるriskを比較して取得surfaceを設計する依頼だから。
- **if_triggered_action**: live searchの必要性と対象domainを限定し、取得結果を未信頼入力として扱い、他の通信surfaceを不要なら無効化する。

### should-not-trigger-01

- **prompt**: repository内はread-only、build directoryだけwrite可能にしたい。
- **selected_skill**: `codex-sandbox-approval-boundary`
- **would_trigger**: no
- **reason**: 外向き通信ではなく、filesystemのread/write能力とpath境界の設計だから。
- **if_triggered_action**: 対象skillでは実行せず、`codex-sandbox-approval-boundary` で必要pathに限定した最小sandboxを選ぶ。

### should-not-trigger-02

- **prompt**: このMCP serverをrequiredにし、read toolだけ有効化したい。
- **selected_skill**: `codex-mcp-control-plane`
- **would_trigger**: no
- **reason**: egress経路全体ではなく、一つのMCP serverの必須性とtool可視性の制御が主題だから。
- **if_triggered_action**: 対象skillでは実行せず、`codex-mcp-control-plane` でserverのrequired設定、read tool限定、approvalを分けて設計する。

### edge-01

- **prompt**: proxy allowlistがあるので、悪意あるDNSや全network迂回も完全に防げるよね？
- **selected_skill**: `codex-egress-surface-governance`
- **would_trigger**: yes
- **reason**: proxy policyの保証範囲と、DNS・別surfaceによる迂回の残余riskを問う依頼だから。
- **if_triggered_action**: 完全防御とは判断せず、DNSの限界とMCP/direct HTTP等の別経路を棚卸しし、各surfaceへ同等controlまたは明示的risk受容を置く。

## codex-bounded-subagents

### should-trigger-01

- **prompt**: 大きなPRをhistory、security risk、API docsの三役で並列reviewし、親で統合したい。
- **selected_skill**: `codex-bounded-subagents`
- **would_trigger**: yes
- **reason**: 大規模reviewを独立したread-heavyな三役へ分け、親agentで統合する典型的な内部役割分解だから。
- **if_triggered_action**: 各役へ一つの問い、scope、禁止操作、証拠付きreturn formatを与え、read-only権限で並列化し、親が矛盾と未確認点を統合する。

### should-trigger-02

- **prompt**: frontend障害をbrowser再現、code path調査、最小修正へ分けてsubagentに任せたい。
- **selected_skill**: `codex-bounded-subagents`
- **would_trigger**: yes
- **reason**: 再現、調査、修正を役割・段階へ分けるsubagent設計を明示的に求めているから。
- **if_triggered_action**: browser再現とcode path調査を独立したread-heavy任務として先行させ、証拠を親へ戻した後、最小修正は一つのwriterへ限定する。

### should-trigger-03

- **prompt**: 20 packageを並列に読ませたいが、共有manifestは一つのagentだけに編集させたい。
- **selected_skill**: `codex-bounded-subagents`
- **would_trigger**: yes
- **reason**: packageごとの独立readを並列化しつつ、共有fileのwrite collisionを単一writerで避ける設計だから。
- **if_triggered_action**: package群を独立したread-only scopeへ分割し、各agentの要約を親で統合してから、共有manifestの変更を一つのwriter actionとして実行する。

### should-not-trigger-01

- **prompt**: 長時間task全体をcloudへ投げ、明日diffを受け取りたい。
- **selected_skill**: `codex-execution-mode-routing`
- **would_trigger**: no
- **reason**: 一つのtask内部の役割分解ではなく、task全体を非同期のcloud実行面へ委譲する選択だから。
- **if_triggered_action**: 対象skillでは実行せず、`codex-execution-mode-routing` でcloud実行の介入モデルとhandoffを選ぶ。

### should-not-trigger-02

- **prompt**: 3行の設定fileでtypoの場所を一つ探して。
- **selected_skill**: `none`
- **would_trigger**: no
- **reason**: 単一agentで短時間に完了できる小さなread作業であり、9件の専門routing skillを必要としないから。
- **if_triggered_action**: 対象skillは発火せず、単一agentが対象fileを直接確認して位置を返す。

### edge-01

- **prompt**: 三つのsubagentに同じlockfileを同時更新させれば速い？
- **selected_skill**: `codex-bounded-subagents`
- **would_trigger**: yes
- **reason**: subagent並列化の適否、とくに同一fileへのwrite-heavy競合という本skillの境界を判断する依頼だから。
- **if_triggered_action**: 同時更新は採用せず、調査だけをread-heavyに分けるか段階実行へ戻し、lockfile更新は一つのwriterまたは隔離されたworktreeへ限定する。
