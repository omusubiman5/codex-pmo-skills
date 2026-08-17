# 段階4 独立盲検 C

## 判定条件

- 候補は `books/codex-cli/INDEX.md` に記載された9 skills。
- 各 `test-prompts.json` からは PowerShell の `ConvertFrom-Json` を使い、`test_cases` の `id` と `prompt` だけを抽出した。
- `would_trigger` は、その節の対象skillを発火するかを示す。
- 判定はprompt本文とskillのrouting境界に基づき、期待値ラベルを採点材料にしていない。

## codex-context-entry-routing

### should-trigger-01

- prompt: UIのspacing差を直したい。screenshot、文章、MCPのどのcontextをCodexへ渡す？
- selected_skill: `codex-context-entry-routing`
- would_trigger: yes
- reason: UIの視覚的な差を調べるためのcontext入口を、画像・文章・MCPから選ぶ依頼であり、visual contextのroutingが主題だから。
- if_triggered_action: spacing差の主要証拠としてscreenshotを最小入口に選び、比較対象、期待する修正、制約、完了条件をtask contractとして添える。

### should-trigger-02

- prompt: 社内API仕様と今日の公開料金表を照合したい。MCPとweb searchをどう使い分ける？
- selected_skill: `codex-context-entry-routing`
- would_trigger: yes
- reason: external structured contextである社内仕様と、current public informationである当日の料金を、それぞれ適切な入口へ振り分ける依頼だから。
- if_triggered_action: 社内API仕様はMCP、今日の公開料金表はlive web searchから取得し、各入口の取得対象と照合の完了条件を明示する。

### should-trigger-03

- prompt: 前のCodex taskの判断履歴を残したまま別案を試したい。resumeかforkかも含めて決めて。
- selected_skill: `codex-context-entry-routing`
- would_trigger: yes
- reason: 既存conversationの判断履歴をcontextとして再利用しつつ別案へ分岐する入口選択が主題だから。
- if_triggered_action: 元taskをそのまま継続するならresume、履歴を保持して独立した別案を試すならforkを選び、この依頼ではforkを推奨する。

### should-not-trigger-01

- prompt: MCPのupdate toolを無効化し、read toolだけapprovalなしにしたい。
- selected_skill: `codex-mcp-control-plane`
- would_trigger: no
- reason: MCPをcontext入口として採用するかではなく、接続後のtool可視性とapprovalを設定する依頼だから。
- if_triggered_action: `codex-mcp-control-plane` へrouteし、updateをdisabled、readだけをenabledにしてautomatic approvalの妥当性をriskに応じて決める。

### should-not-trigger-02

- prompt: local repository内のREADMEだけを要約して。
- selected_skill: none
- would_trigger: no
- reason: 必要情報がlocal repository内で完結しており、画像、search、MCP、conversation historyの入口選択が不要だから。
- if_triggered_action: routing skillは使わず、対象READMEをlocal fileとして読み要約する。

### edge-01

- prompt: screenshotだけ添付した。いい感じに直して。
- selected_skill: none
- would_trigger: no
- reason: screenshotはあるが、inspect対象、期待結果、制約、完了条件がなく、画像入口を選ぶためのtask contractが成立していないから。
- if_triggered_action: 直ちに修正へ進まず、どの画面要素をどう直し、何を完了とするかの具体化を求める。

## codex-auth-boundary-selection

### should-trigger-01

- prompt: browserのないremote serverでCodex CLIへloginしたい。device codeを使うべき？
- selected_skill: `codex-auth-boundary-selection`
- would_trigger: yes
- reason: browserのないheadless interactive hostに適したCodex CLI認証flowを選ぶ依頼だから。
- if_triggered_action: device codeまたは別machineで完了するlocalhost callbackを比較し、headless hostに適したflow、保存scope、revoke方法を決める。

### should-trigger-02

- prompt: CIのcodex execへAPI keyを一回のprocessだけ渡し、logやartifactには残したくない。
- selected_skill: `codex-auth-boundary-selection`
- would_trigger: yes
- reason: non-interactive automationにprocess-scoped credentialを割り当て、その露出経路を制御する依頼だから。
- if_triggered_action: API keyを単一processの環境へ限定して渡し、repository、log、artifact、shell history、child processへの漏出を検査する。

### should-trigger-03

- prompt: auth.jsonを別hostへコピーして使い回してよいかsecurity reviewして。
- selected_skill: `codex-auth-boundary-selection`
- would_trigger: yes
- reason: 保存済み認証cacheのhost間移送、共有、保存riskの評価が主題だから。
- if_triggered_action: `auth.json` をpassword同等の秘密として扱い、コピー主体、保存先権限、同期・漏出経路、rotation/revokeを確認し、可能ならhostごとの認証を選ぶ。

### should-not-trigger-01

- prompt: Codex jobはread-onlyにしてpatchを別jobでpushしたい。
- selected_skill: `codex-ci-patch-handoff`
- would_trigger: no
- reason: credential方式ではなく、推論jobのread-only性とwrite authorityをpatch handoffで分離する設計だから。
- if_triggered_action: `codex-ci-patch-handoff` へrouteし、生成jobはread-onlyでpatchを出力し、別の権限付きjobで検証後にpushする。

### should-not-trigger-02

- prompt: workspace外へのwriteを毎回approvalにしたい。
- selected_skill: `codex-sandbox-approval-boundary`
- would_trigger: no
- reason: 認証前後のcredential選択ではなく、filesystem能力と人の昇格同意の境界設定だから。
- if_triggered_action: `codex-sandbox-approval-boundary` へrouteし、workspace外writeをsandbox境界の外に置いて都度approvalを要求する。

### edge-01

- prompt: 共有workstationなので、一人のauth.jsonを全員で読めるfolderへ置けば便利だよね？
- selected_skill: `codex-auth-boundary-selection`
- would_trigger: yes
- reason: `auth.json` の共有と読取scopeは認証cacheの保存・共有riskそのものであり、利便性より秘密境界の評価が必要だから。
- if_triggered_action: 全員読取可能な保存を拒否し、利用者ごとのsign-inまたは個別credentialを使い、file ACLとrevoke境界を分離する。

## codex-mcp-control-plane

### should-trigger-01

- prompt: 社内台帳MCPが起動しなければ監査jobを失敗させたい。required serverをどう設定する？
- selected_skill: `codex-mcp-control-plane`
- would_trigger: yes
- reason: MCP serverの必須性とinit failure時のfail-closed動作を設定する依頼だから。
- if_triggered_action: 台帳なしで正しい監査ができないことを確認してserverをrequiredにし、初期化失敗やtimeoutでjobが失敗する経路を試す。

### should-trigger-02

- prompt: 一つのMCPにread、update、delete toolがある。Codexにはreadだけ見せたい。
- selected_skill: `codex-mcp-control-plane`
- would_trigger: yes
- reason: 接続済みMCP内でCodexへ公開するtool surfaceをreadだけに制限する依頼だから。
- if_triggered_action: read toolだけを`enabled_tools`へallowlist化するか、update/deleteを`disabled_tools`で除外し、不可視toolを呼べないことを確認する。

### should-trigger-03

- prompt: docs researcher subagentにだけ公式docs MCPを付け、他agentからは隠したい。
- selected_skill: `codex-mcp-control-plane`
- would_trigger: yes
- reason: roleごとにMCP serverとtool可視性を限定するcontrol-plane設計が主題だから。
- if_triggered_action: docs researcher roleだけへ公式docs MCPのread toolを付与し、他agentのserver/tool surfaceから除外する。

### should-not-trigger-01

- prompt: search、MCP、direct HTTPを含む全egress経路を棚卸ししたい。
- selected_skill: `codex-egress-surface-governance`
- would_trigger: no
- reason: MCP内部のrequired・tool・approval設定ではなく、複数のnetwork surfaceを横断した通信経路の監査だから。
- if_triggered_action: `codex-egress-surface-governance` へrouteし、search、MCP、direct HTTPを個別surfaceとして棚卸ししてallow/deny条件を決める。

### should-not-trigger-02

- prompt: 画像と最新Web情報のどちらをcontextとして渡すべき？
- selected_skill: `codex-context-entry-routing`
- would_trigger: no
- reason: MCP制御ではなく、visual contextとcurrent public contextのどちらを入口にするかの選択だから。
- if_triggered_action: `codex-context-entry-routing` へrouteし、必要情報が視覚状態なら画像、変動する公開情報ならlive web searchを選ぶ。

### edge-01

- prompt: MCPは便利そうだから全serverをrequired、全toolをautomatic approvalにしよう。
- selected_skill: `codex-mcp-control-plane`
- would_trigger: yes
- reason: 提案内容は危険だが、server必須性、tool範囲、approvalというMCP control-planeの三要素を決める場面だから。
- if_triggered_action: 一括設定を拒否し、taskごとに必須serverだけをrequired、必要toolだけをallowlist化し、writeや高risk toolはaskまたはdenyへ分ける。
