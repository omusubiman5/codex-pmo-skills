# Codex CLI — 三重検証通過候補

検証対象は `SOURCE_MANIFEST.md` に固定した OpenAI 公式資料15件と、段階1の5候補ファイルのみ。
V2の問いと回答は検証用の外挿であり、公式資料の記述とは区別した。`A1_source_cases` は段階2で
原典の具体例を捏造せず配置できるかを示す補助監査項目で、三重検証そのものには加算していない。

```yaml
- id: f06
  title: 対話・自動化・cloudの実行形態選択
  merged_candidates: []
  V1_cross_domain:
    passed: true
    evidence:
      - "Codex CLI — 対話型terminal loopとscripting/CIを別用途として提示"
      - "Codex cloud — background、parallel、delegated workを独立した実行形態として提示"
      - "Non-interactive mode — codex execをpipeline向けに具体化"
  V2_predictive_power:
    passed: true
    novel_question: "夜間に30リポジトリを同じ規則で検査し、朝に結果だけ確認する仕事をどこで動かすか"
    derived_answer: "人の逐次介入を要しない反復処理なので対話型CLIではなくexecをpipeline化する。各仕事が長時間で独立し、隔離環境と非同期受領を優先するならcloudへ移す。"
  V3_exclusivity:
    passed: true
    why_not_common: "単なる『適切な道具を選ぶ』ではなく、CodexのCLI・exec・cloudを人の関与、反復性、実行場所、受領時点で割り当てる製品固有の選択表である。"
  A1_source_cases: [c03, c04]
  supporting_principles: [p10, p12]

- id: f07
  title: 非対話実行の入出力契約化
  merged_candidates: []
  V1_cross_domain:
    passed: true
    evidence:
      - "Non-interactive mode — progressはstderr、最終messageはstdoutというstream分離"
      - "Non-interactive mode — --jsonによるJSONL event stream"
      - "Non-interactive mode — --output-schemaによる最終値のJSON Schema拘束"
      - "CI例 — patch artifactと後続jobによる受け渡し"
  V2_predictive_power:
    passed: true
    novel_question: "監視画面には進捗を流しつつ、後続jobには検証済みの脆弱性件数だけ渡すにはどうするか"
    derived_answer: "event観測はJSONLまたはstderrから取り、downstream入力は件数fieldを必須にしたoutput schemaで別ファイルへ固定する。表示用streamを機械契約として誤用しない。"
  V3_exclusivity:
    passed: true
    why_not_common: "Codex execのstdout・stderr・JSONL・schema outputという具体的な面を、観測経路と最終成果物の別契約として組み合わせる。"
  A1_source_cases: [c01, c03, c04]
  supporting_principles: [p14]

- id: f08
  title: CI修正の権限分離とpatch受け渡し
  merged_candidates: []
  V1_cross_domain:
    passed: true
    evidence:
      - "Non-interactive mode — autofix例でCodex jobをcontents: readに限定しpatch artifactを生成"
      - "Agent approvals & security — credentialsをrepository-controlled codeから隔離する原則"
      - "Authentication — CODEX_API_KEYを一回のexec processだけにscopeする方法"
  V2_predictive_power:
    passed: true
    novel_question: "依存更新botの失敗をCodexに直させたいが、署名鍵は変更生成jobへ渡せない場合はどう分けるか"
    derived_answer: "生成jobはread-only checkoutと短命な推論credentialだけでpatchを出し、署名・pushは推論credentialを持たない後続jobが検証後に行う。"
  V3_exclusivity:
    passed: true
    why_not_common: "『最小権限』という抽象論ではなく、Codex credentialとrepository write権限を別jobに置き、binary patchを唯一の境界通過物にする具体構成である。"
  A1_source_cases: [c02]
  supporting_principles: [p12, p13]

- id: f09
  title: sandboxとapprovalの二層境界設計
  merged_candidates: [f23]
  V1_cross_domain:
    passed: true
    evidence:
      - "Agent approvals & security — sandboxが技術的能力、approval policyが昇格時の同意を制御"
      - "Non-interactive mode — execは既定read-onlyで、必要に応じworkspace-writeを選択"
      - "Best practices — 最小権限から始め必要時だけ拡張"
  V2_predictive_power:
    passed: true
    novel_question: "生成物directoryへの書込みは許すが、package installは毎回人が判断したい場合の構成は何か"
    derived_answer: "filesystem能力は対象workspaceへ限定したsandboxで与え、networkや境界外操作はapproval対象として残す。能力の有無と同意の要否を一つのflagに潰さない。"
  V3_exclusivity:
    passed: true
    why_not_common: "Codexの安全境界をsandbox modeとapproval policyという直交する二層へ分け、最小状態から段階的に拡張する固有モデルである。"
  A1_source_cases: [c09]
  supporting_principles: [p05, p12]

- id: f11
  title: 複数通信経路を個別統制する脅威モデル
  merged_candidates: [f10, f12]
  V1_cross_domain:
    passed: true
    evidence:
      - "Web search — cached searchとlive searchを分け、結果をuntrustedとして扱う"
      - "Agent approvals & security — command networkをpermissionとproxy policyの二段階で制御"
      - "Agent approvals & security — MCP trafficとdirect HTTPを別経路として列挙"
  V2_predictive_power:
    passed: true
    novel_question: "検索domainを限定したのにMCP経由の外部送信が残る構成を安全と判定できるか"
    derived_answer: "できない。search、sandboxed command、MCP、direct HTTPは別surfaceなので、各経路の有効化、宛先、approval、信頼境界を個別に監査する。"
  V3_exclusivity:
    passed: true
    why_not_common: "『networkを制限する』ではなく、Codexの複数egress surfaceを分解し、search mode、network permission、proxy policyを別制御として扱う脅威モデルである。"
  A1_source_cases: [c08]
  supporting_principles: [p15, p16]

- id: f13
  title: bounded subagentへの分解と要約再統合
  merged_candidates: [f14, f15]
  V1_cross_domain:
    passed: true
    evidence:
      - "Best practices — PR reviewをhistory・risk・API docsの独立役へ分解"
      - "Best practices — frontend debuggingをreproduction・code path・minimal fixへ段階分解"
      - "Subagents — roleごとのinstructions、model、sandbox、tool surfaceを設定"
  V2_predictive_power:
    passed: true
    novel_question: "大規模migrationの調査を並列化したいが同じmanifestへの競合編集を避けるにはどうするか"
    derived_answer: "各agentを依存関係調査、互換性確認、test impactのread-heavy成果物に限定し、親が要約を統合した後、一つのwriterだけがmanifestを変更する。"
  V3_exclusivity:
    passed: true
    why_not_common: "単なる並列化ではなく、bounded task、read-heavy優先、役割別tool/sandbox/model、親への圧縮再統合を一体にしたCodex subagent設計である。"
  A1_source_cases: [c05, c06]
  supporting_principles: [p07, p11]

- id: f17
  title: 外部文脈の入口選択
  merged_candidates: []
  V1_cross_domain:
    passed: true
    evidence:
      - "Image inputs — screenshotまたはdesign specをtask languageと共に渡す"
      - "Web search — cached/live searchでcurrent informationを取得"
      - "MCP — third-party contextとtoolsをserver経由で接続"
      - "Developer commands — resume/forkで既存conversation contextを再利用"
  V2_predictive_power:
    passed: true
    novel_question: "社内API仕様と現在の公開料金表を照合し、画面差分も直す仕事へ何を接続するか"
    derived_answer: "社内仕様は限定toolのMCP、変動する公開情報はlive search、視覚差分は画像入力、既存の判断履歴はresumeで供給し、異なる入口を一つの万能経路で代用しない。"
  V3_exclusivity:
    passed: true
    why_not_common: "Codex CLIが持つimage・search・MCP・conversationという異種context入口を、情報の所在と更新性で選ぶ製品固有のルーティングである。"
  A1_source_cases: [c07]
  supporting_principles: [p18]

- id: f18
  title: repeatabilityと接続性によるskill・plugin選択
  merged_candidates: []
  V1_cross_domain:
    passed: true
    evidence:
      - "Skills & plugins — skillをinstructions・resources・scriptsの再利用可能packageとして定義"
      - "Skills & plugins — pluginをskills、apps、connectors、MCP serversを含むbundleとして対比"
      - "Best practices — 安定し反復可能になったworkflowだけをskill化する成熟順序"
  V2_predictive_power:
    passed: true
    novel_question: "定型release checklistに社内ticket systemのlive操作も必要なとき、skillだけで配るべきか"
    derived_answer: "手順とscriptはskillにできるが、共有connectionとMCP capabilityまで一体配布する必要があるためplugin境界が適する。workflow自体が未安定なら先に手動運用で固める。"
  V3_exclusivity:
    passed: true
    why_not_common: "Codexにおけるskillとpluginの構成要素の差を、反復可能性と外部接続の配布要件へ対応させる固有の選択規則である。"
  A1_source_cases: []
  A1_note: "公式コーパスにskill/plugin選択を最後まで適用したworked caseはない。ユーザー確認済みの既定判断により、原典例A1を捏造せずskill化対象から除外し、GLOSSARYの選択上の区別へ降格した。"
  stage2_eligible: false
  supporting_principles: [p08, p09, p17]

- id: f19
  title: 認証方式を利用面と統制境界へ対応させる
  merged_candidates: []
  V1_cross_domain:
    passed: true
    evidence:
      - "Authentication — ChatGPT sign-inとAPI keyを利用形態・課金面で区別"
      - "Authentication — headless device code、localhost callback、pre-provisioned auth.jsonを区別"
      - "Non-interactive mode — CIではCODEX_API_KEYを一回のexec processへscope"
  V2_predictive_power:
    passed: true
    novel_question: "GUIなしの短命runnerと、複数開発者が使う固定workstationで同じlogin方式を使うべきか"
    derived_answer: "短命runnerはprocess-scoped API key、対話可能な固定端末はChatGPT sign-in、headless対話端末はdevice codeを検討し、auth cacheの複製はpassword同等の秘密移送として扱う。"
  V3_exclusivity:
    passed: true
    why_not_common: "CodexのChatGPT login、API key、device code、localhost callback、auth cacheを利用面とsecret boundaryへ具体的に対応させる認証選択表である。"
  A1_source_cases: [c12]
  supporting_principles: [p19, p20]

- id: f22
  title: MCP接続の必須性・tool範囲・承認の三段階制御
  merged_candidates: []
  V1_cross_domain:
    passed: true
    evidence:
      - "MCP — serverごとのenabled_tools/disabled_toolsとapproval policy"
      - "Non-interactive mode — required MCP serverが初期化失敗またはtimeoutならexecを終了"
      - "Subagents — docs researcherへ専用MCP serverとread-only sandboxだけを付与"
  V2_predictive_power:
    passed: true
    novel_question: "監査jobが社内台帳MCPなしでは正しい結論を出せないが、更新toolは不要な場合どう構成するか"
    derived_answer: "serverをrequiredにしてfail closedとし、enabled_toolsをread系に限定し、該当toolのapprovalを要求する。接続可否、tool可視性、呼出し同意を別々に設定する。"
  V3_exclusivity:
    passed: true
    why_not_common: "Codex MCP設定のrequired、tool filtering、approvalを独立した三段階controlとして組み合わせる固有モデルである。"
  A1_source_cases: [c05]
  supporting_principles: [p07, p22]
```

## 集計

- 通過: 10
- 既存通過候補へ統合: 5（f10, f12, f14, f15, f23）
- 棄却: 9（個別理由は `rejected/`）
- 三重検証通過率: 10 / 19 = 52.6%（統合後の独立候補を分母とする）
