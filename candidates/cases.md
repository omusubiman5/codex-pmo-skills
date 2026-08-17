# Case candidates — Codex CLI official corpus

## Extraction audit

- **Stage**: 1（case extraction only）
- **Extractor contract**: `extractors/case-extractor.md`
- **Corpus**: `SOURCE_MANIFEST.md` に固定された OpenAI 公式資料15件
- **Corpus verification**: 2026-08-17 に15件を再取得し、全件の SHA-256 が manifest と一致することを確認した。
- **Boundary**: manifest 記載本文だけを使用した。本文中の二段階目以降のリンク先は開かず、証拠にもしていない。
- **Admission rule**: 具体的な構成例、worked example、または実運用手順のうち、資料本文が生成物・状態変化・制御効果を明記するものだけを収録した。単なる機能列挙、用途候補、結果のない例示は除外した。
- **Outcome caveat**: 公式資料にベンチマークや実測値がない例は、資料が明示する設計上の結果だけを記載し、実環境で成功したとは表現しない。

```yaml
- id: c01
  title: JSON Schemaでプロジェクトメタデータを固定形式にする
  type: case
  source_chapter: "Non-interactive mode — Create structured outputs with a schema"
  source_quote: |
    "use `--output-schema` to request a final response that conforms to a JSON Schema"
    "Example final output (stdout):"
  summary: |
    問題: 後段の自動処理が、人向けの自由文ではなく安定したフィールドを必要としている。
    適用: `project_name` と `programming_languages` を必須にした `schema.json` を作り、
    `codex exec "Extract project metadata" --output-schema ./schema.json -o ./project-metadata.json`
    を実行する。
    結論: 最終回答の形をプロンプト上の希望ではなくJSON Schemaの契約として指定し、
    ファイル出力を後段へ渡す。
  bound_to:
    - "機械可読な出力契約"
    - "codex execによる非対話自動化"
  outcome: |
    資料のサンプル最終出力は、`project_name: Codex CLI` と
    `programming_languages: [Rust, TypeScript, Shell]` を持つJSONである。
  tags: [case, worked-example, codex-exec, json-schema, automation]

- id: c02
  title: CI失敗の修正案を秘密情報と書込権限から分離してPR化する
  type: case
  source_chapter: "Non-interactive mode — Example: Autofix CI failures in GitHub Actions"
  source_quote: |
    "The Codex job below has only `contents: read`."
    "In a separate job, apply the patch and open a pull request."
  summary: |
    問題: CI失敗をCodexに修正させたいが、リポジトリ管理下のセットアップやテストへAPI keyを露出し、
    同じjobにリポジトリ書込権限まで与えると信頼境界が広がる。
    適用: 失敗したcommitをread-only権限でcheckoutし、Codex GitHub Actionに失敗の再現、最小修正、
    再テストを依頼する。変更はbinary patch artifactとして保存し、API keyを受け取らない別jobだけが
    patchを適用してbranchをpushし、PRを開く。
    結論: 推論用credentialとリポジトリ書込権限をjobで分離し、受け渡しをpatchに限定する。
  bound_to:
    - "CI credentialとwrite権限の分離"
    - "patchを境界にした自動修正"
    - "最小権限の自動化"
  outcome: |
    Codexが差分を生成した場合だけ`codex-fix-patch` artifactが作られ、後続jobが
    `codex/auto-fix-$RUN_ID` branchへcommitして「Auto-fix failing CI via Codex」というPRを作る。
    資料はworkflow構成と到達状態を示すが、特定repositoryでの成功率や実測結果は示していない。
  tags: [case, worked-example, ci, github-actions, least-privilege, patch]

- id: c03
  title: テスト出力をstdinで渡して失敗要約を成果物化する
  type: case
  source_chapter: "Non-interactive mode — Advanced stdin piping / Use prompt-plus-stdin"
  source_quote: |
    "pipe in the output as context"
    "summarize the failing tests and propose the smallest likely fix"
  summary: |
    問題: `npm test` の大量の出力から、失敗箇所と最小修正候補を人手で抽出する必要がある。
    適用: `npm test 2>&1` を、指示をprompt引数に固定した `codex exec` へpipeし、
    最終回答を `tee test-summary.md` で保存する。
    結論: instructionと観測データを分離し、既存CLIの出力をCodexのcontextとして直結する。
  bound_to:
    - "prompt-plus-stdin"
    - "CLIパイプラインによるログ要約"
  outcome: |
    コマンドの最終出力は`test-summary.md`に保存される。資料が指定する内容は、
    失敗テストの要約と最小の修正候補であり、具体的なテスト結果そのものは掲載されていない。
  tags: [case, worked-example, stdin, testing, artifact]

- id: c04
  title: CIログからPull Requestコメントを直接作成する
  type: case
  source_chapter: "Non-interactive mode — Draft a pull request comment from CI logs"
  source_quote: |
    "summarize the failure in 5 bullets for the pull request thread"
    "gh pr comment 789 --body-file -"
  summary: |
    問題: GitHub Actionsの実行ログを、PR参加者が読める短い更新へ変換して投稿したい。
    適用: `gh run view 123456 --log` の出力を `codex exec` に渡し、5項目の要約を
    `gh pr comment 789 --body-file -` の標準入力へ接続する。
    結論: 取得、要約、投稿を一つのpipeにし、中間ファイルなしで用途別の最終形式へ変換する。
  bound_to:
    - "prompt-plus-stdin"
    - "codex execのdownstream連携"
  outcome: |
    資料が示すコマンドの到達点は、CI失敗の5項目要約がPR 789のコメントとして渡されることである。
    投稿内容の実例や投稿成功の実測記録は示されていない。
  tags: [case, worked-example, github, ci-log, pipeline]

- id: c05
  title: PRレビューを探索・リスク評価・API確認の三役へ分割する
  type: case
  source_chapter: "Subagents — Example custom agents / Example 1: PR review"
  source_quote: |
    "This pattern splits review across three focused custom agents"
    "map the affected code paths, reviewer find real risks, and docs_researcher verify"
  summary: |
    問題: 一つのreviewerへコード探索、欠陥検出、外部API仕様確認を混在させると、役割とtool境界が曖昧になる。
    適用: `pr_explorer`をread-onlyの実行経路調査、`reviewer`をcorrectness・security・test risk、
    `docs_researcher`を専用docs MCPによるversion依存API確認へ割り当てる。三者とも変更を行わず、
    main agentがbranch対mainのレビュー結果を統合する。
    結論: read-heavyな独立作業を専門agentへ分け、証拠と検出結果をmain threadへ戻す。
  bound_to:
    - "bounded subagentの設計"
    - "read-heavy作業の並列化"
    - "専用tool surfaceと最小権限"
  outcome: |
    資料が示す返却物は、影響code pathの地図、具体的risk、patchが依存するframework APIの確認結果を
    main agentがまとめたreviewである。これは公式の構成例であり、実際のfinding本文や測定値は掲載されていない。
  tags: [case, configuration-example, subagents, code-review, mcp, read-only]

- id: c06
  title: UI障害をブラウザ再現・コード追跡・最小修正の三段階で処理する
  type: case
  source_chapter: "Subagents — Example custom agents / Example 2: Frontend integration debugging"
  source_quote: |
    "Have browser_debugger reproduce it, code_mapper trace the responsible code path"
    "ui_fixer implement the smallest fix once the failure mode is clear."
  summary: |
    問題: settings modalの保存失敗が、実行中UIとfrontend/backendコードをまたいでおり、再現前の編集は危険である。
    適用: `browser_debugger`がscreenshots・console・network evidenceを採取し、`code_mapper`がentry pointと
    state transitionをread-onlyで追跡する。そのfailure modeが明確になってから`ui_fixer`だけが最小修正を所有する。
    結論: 観測、コード対応付け、変更を役割分離し、編集開始を再現証拠の後へ置く。
  bound_to:
    - "証拠先行のfrontend debugging"
    - "bounded subagentの段階的再統合"
    - "write権限の役割分離"
  outcome: |
    資料が示す到達状態は、失敗の正確な再現記録、責任code pathの特定、理解済みfailure modeに対する
    最小修正と変更対象behaviorの検証である。実際の修正diffや成功測定は掲載されていない。
  tags: [case, configuration-example, subagents, frontend, browser, debugging]

- id: c07
  title: 画像比較をspacing・typography修正と再撮影検証へ限定する
  type: case
  source_chapter: "Image inputs — Write the prompt around the image"
  source_quote: |
    "Fix spacing and typography only; do not change behavior."
    "Verify the result with a new screenshot."
  summary: |
    問題: checkout画面とdesignの視覚差を修正したいが、UI挙動まで変えるscope creepを避けたい。
    適用: 比較対象を画像で与え、修正範囲をspacingとtypographyだけに限定し、behavior変更を禁止する。
    結論: 視覚入力、変更制約、完了時の再撮影を一つのprompt契約にする。
  bound_to:
    - "視覚contextを含む依頼設計"
    - "制約と検証条件の明示"
  outcome: |
    資料が要求する成果は、spacingとtypographyだけを直した画面と、その状態を確認する新しいscreenshotである。
    修正後画像そのものや実行済み結果は掲載されていない。
  tags: [case, worked-example, image-input, ui, visual-verification]

- id: c08
  title: command networkを許可しつつ宛先をproxy policyで絞る
  type: case
  source_chapter: "Agent approvals & security — Network isolation"
  source_quote: |
    "Network on + `network_proxy` on: network stays on"
    "outbound traffic is constrained by the configured network policy."
  summary: |
    問題: workspace内のcommandに外部通信は必要だが、無制限のoutbound accessは与えたくない。
    適用: `sandbox_workspace_write.network_access = true`でcommand network自体を許可し、
    `features.network_proxy.enabled = true`とdomain rulesを併用して`api.openai.com`をallow、
    `example.com`をdenyにする。
    結論: networkを使えるかという能力と、使える宛先というpolicyを別設定として同時に有効化する。
  bound_to:
    - "sandbox能力とnetwork policyの分離"
    - "allowlistによる最小権限"
  outcome: |
    資料が明記する効果は、network accessを維持したままoutbound trafficが設定policyに制約されることである。
    `deny`は`allow`より優先する。proxyだけを有効にしてもnetwork accessは付与されない。
  tags: [case, configuration-example, security, network-proxy, least-privilege]

- id: c09
  title: Linux sandboxを使えないhostでDev Containerを外側の隔離境界にする
  type: case
  source_chapter: "Agent approvals & security — Run Codex in Dev Containers"
  source_quote: |
    "let Docker provide the outer isolation boundary"
    "an allowlist-driven firewall profile for outbound access"
  summary: |
    問題: hostまたはcontainer設定がnamespace、setuid `bwrap`、`seccomp`を妨げ、CodexのLinux sandboxを直接使えない。
    適用: 公式secure devcontainer exampleの三要素、container設定、Ubuntu image、outbound firewall初期化を
    repositoryへ導入し、VS Codeまたは`devcontainer up`で起動する。内側で`bwrap`が可能ならCodex sandboxを残し、
    container自体を境界にする場合だけその内側でfull accessを使う。
    結論: sandbox不能を無条件full accessで済ませず、Docker側へ明示的な隔離・egress制御を移す。
  bound_to:
    - "実行環境による外側の隔離境界"
    - "sandbox互換性と防御層の選択"
  outcome: |
    資料のreference implementationは、Codexと開発toolを含むUbuntu 24.04環境、allowlist firewall、
    persistent mount、`bubblewrap`を構成する。一方でcontainer内credentialの窃取まで防ぐとはしておらず、
    trusted repositoryに限定する注意も明記する。
  tags: [case, configuration-example, devcontainer, sandbox, firewall]

- id: c10
  title: prompt本文を伏せたままCodex実行をOpenTelemetryへ送る
  type: case
  source_chapter: "Agent approvals & security — Monitoring and telemetry / Enable OTel"
  source_quote: |
    "log_user_prompt = false"
    "Codex batches events and flushes them on shutdown."
  summary: |
    問題: 利用状況、approval判断、tool実行を監査したいが、source codeや機密を含み得るprompt本文は収集したくない。
    適用: `[otel]`でenvironmentと自己管理collectorへのOTLP exporterを設定し、
    `log_user_prompt = false`を維持する。collector credentialはheaderの環境変数参照で渡す。
    結論: 観測可能性をopt-inで追加し、prompt内容の収集を独立した明示設定として無効にする。
  bound_to:
    - "監査可能性と機密性の分離"
    - "opt-in telemetry"
  outcome: |
    資料が示す結果は、conversation、API、stream、tool decision/resultなどのstructured eventがbatchされ、
    shutdown時に指定collectorへflushされること、promptは既定でredactされることである。
  tags: [case, configuration-example, observability, otel, privacy]

- id: c11
  title: 変更適用と分離した専用reviewerでworking treeを検査する
  type: case
  source_chapter: "Code review — Start a review / Work with review results"
  source_quote: |
    "reports prioritized, actionable findings without changing your working tree"
  summary: |
    問題: commitやpushの前にlocal変更のbehavior riskとmissing testを調べたいが、review工程自体に変更させたくない。
    適用: `/review`でbase branch、uncommitted changes、特定commit、custom criteriaのいずれかを選び、
    専用reviewerへdiffを読ませる。必要なら後から通常のsandbox・approval下で修正を別途依頼する。
    結論: finding生成とfix適用を別turn・別権限制御に分ける。
  bound_to:
    - "変更とレビューの分離"
    - "diffを用いた完了前検証"
  outcome: |
    review結果はtranscriptの一turnとして、優先順位付きのactionable findingを返し、working treeは変更しない。
  tags: [case, operational-example, review, verification, non-mutating]

- id: c12
  title: headless環境をdevice codeで認証する
  type: case
  source_chapter: "Authentication — Login on headless devices / Preferred: Device code authentication"
  source_quote: |
    "prefer device code authentication"
    "Open the link in your browser, sign in, then enter the one-time code."
  summary: |
    問題: remoteまたはheadless環境では、localhost callbackを使う通常のbrowser loginが成立しないことがある。
    適用: security/workspace設定でdevice code loginを有効にし、headless側で
    `codex login --device-auth`を実行する。表示されたlinkを別のbrowserで開き、one-time codeを入力する。
    結論: credential fileの手動転送より先に、秘密情報を直接コピーしないdevice-code flowを選ぶ。
  bound_to:
    - "環境別authentication方式の選択"
    - "headless loginのcredential保護"
  outcome: |
    資料が示す到達状態は、headless terminalで開始したloginをbrowser上のone-time code入力で完了することである。
    device codeが利用不能な場合だけ、auth cache転送またはSSH callback forwardingへfallbackする。
  tags: [case, operational-example, authentication, headless, device-code]
```

## Excluded near-matches

- `Tell me about this project`、release note生成、一般的なlog要約など、入力や用途だけで結果例・到達状態が示されないもの。
- Configuration landing page、MCP server一覧、skills/pluginsの用途一覧、Codex cloudの機能一覧。
- `/model`、`/theme`、`/copy`など単一commandの操作説明。状態変化は書かれていても、独立した方法論事例としては薄い。
- `AGENTS.md`更新、plan-first、scheduled tasksなどの推奨原則。具体的な適用と結果が同じ資料内に示されないため、caseへ変換していない。
- subagent資料の「multi-million-token document」例。分割可能性の説明だけで、実施された分割や返却結果は示されない。

