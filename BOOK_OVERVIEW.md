# Codex CLI公式資料集 — 全体理解（段階0成果物）

> 本文書は cangjie-skill の段階0成果物であり、後続のextractorとskillはこれを全体文脈として使用する。

## 基本情報

- **タイトル**: Codex CLI公式資料集
- **著者・提供者**: OpenAI
- **公開時期**: 各ページに記載なし
- **内容タイプ**: 公式技術資料集・運用ガイド・コマンドリファレンス
- **バージョンソース**: [SOURCE_MANIFEST.md](./SOURCE_MANIFEST.md)記載の15ページ
- **取得・処理日**: 2026-08-17

---

## 1. 構造（Structural）

### タイプ

導入、対話操作、自動化、設定、認証、権限制御、外部連携、並列実行、レビューを横断する実務運用資料集。

### 一文の主旨

Codex CLIを安全かつ再現可能に使うには、タスクの文脈と完了条件を明示し、対話・自動化・クラウド・分業の実行形態を選び、権限・検証・復元・外部接続を独立した制御層として設計する。

### 骨格（主要論点と関係）

1. **正しい作業文脈を与える**: 目標、関連ファイル、制約、完了条件を提示し、視覚情報・履歴・最新情報・外部情報を適切な入口から追加する。
2. **知識を持続層へ昇格させる**: 一時的prompt、`AGENTS.md`、config、skills、pluginsを、再利用範囲と変更頻度に応じて使い分ける。
3. **実行形態を仕事の性質で選ぶ**: 人が誘導する対話型CLI、無人の`codex exec`、隔離環境へ委譲するCodex cloud、独立部分を処理するsubagentsを区別する。
4. **能力と権限を分離して制御する**: sandboxが技術的に可能な操作を、approval policyが確認を要する操作を決め、network・MCP・apps・searchは別々の経路として管理する。
5. **出力と検証を契約化する**: `stdout`/`stderr`、JSONL、JSON Schema、テスト、diff、専用reviewを用いて、結果を機械処理・判定・監査できる形にする。
6. **復元可能性と観測可能性を保つ**: Git checkpoint、branch、patch、session resume/fork、status、diagnostics、任意のtelemetryによって失敗から戻り、実行状態を確認できるようにする。

**論点間の関係**: 1と2が文脈設計、3が実行配置、4が安全境界、5が受入判定、6が回復と監査を担う。順番に一度だけ通る工程ではなく、タスクごとに組み合わせる制御面である。

### 著者が解決しようとしている核心問題

Codexを単発のコード生成器としてではなく、ローカル・CI・クラウド・外部ツールを横断する開発チームメイトとして運用しながら、文脈不足、過剰権限、出力の不安定さ、並列作業の衝突、認証情報漏えい、検証不足をどう抑えるか。

---

## 2. 解釈（Interpretive）

### 主要用語（資料内での用法）

| 用語 | 資料内での意味 | 一般的な用法との差 |
|---|---|---|
| interactive TUI | 人がturnを誘導し、commandとdiffを見ながら同じsessionで反復する作業面 | 単なるterminal UIではなく、人間参加型の制御ループ |
| `codex exec` | TUIを開かずscript・CIから完了まで走る非対話入口 | 通常の一回実行ではなく、sandbox・output・schemaを固定できる自動化面 |
| Codex cloud | 再現可能な隔離環境でbackground・parallel実行し、summaryとdiffを後でreviewする委譲面 | local CLIの単純なremote版ではない |
| sandbox mode | commandが技術的に読める・書ける・networkへ出られる範囲 | approvalの有無とは別の強制境界 |
| approval policy | sandbox外操作や特定actionで、実行前に誰の承認が必要かを決める規則 | sandbox自体の許可範囲とは別層 |
| web search | cached/indexed/liveを選べるhosted tool | command network proxyやdomain allowlistとは別経路 |
| MCP | modelへ外部toolとcontextを接続するprotocol | pasted contextではなく、認証・tool policyを伴う実行接続 |
| skill | 一つの反復task向けinstructionとsupporting resourceの再利用単位 | 外部接続を必須としない |
| plugin | skillsやMCP connectorを含められるinstallable bundle | focused instructionsだけのskillより配布・接続範囲が広い |
| `AGENTS.md` | repositoryまたはsubdirectoryへ自動注入するdurable guidance | 一回のpromptではなく、場所に応じて優先順位が変わるagent用README |
| subagent | 独立したbounded taskを別threadで処理し、要約をmain agentへ返すagent | 単なる追加workerではなく、context pollutionを隔離する手段 |
| JSONL output | `codex exec --json` がstate changeごとに出すevent stream | 最終回答だけでなく途中のcommand・tool・turn状態を機械処理できる |
| output schema | 最終回答に要求するJSON Schema | streaming event形式ではなく、downstreamへ渡す最終データ契約 |
| code review | 指定diffを専用reviewerが読み、作業ツリーを変えず優先順位付きfindingを返す処理 | 修正適用とは分離される |
| session resume / fork | 同じ履歴を継続するか、履歴を保持した別chatへ分岐する操作 | 新規chatとは異なりreasoning trailを再利用する |

### 核心命題（再構成）

1. 良いpromptは「Goal・Context・Constraints・Done when」の四点でscopeと受入条件を作る。
2. 複雑・曖昧なtaskではcoding前にplanを作り、曖昧さを質問と検証可能な手順へ変換する。
3. 繰り返すrepository規約は`AGENTS.md`へ、安定した反復workflowはskillへ、外部tool接続を伴う配布単位はpluginへ置く。
4. 対話型、`codex exec`、cloud、subagentは優劣ではなく、人の関与、反復性、隔離、並列性で選ぶ。
5. sandboxとapprovalは同じものではなく、前者が可能性、後者が確認時点を制御する。
6. network proxyを有効にしてもnetwork access自体は付与されず、web search・MCP・appsなど他経路も制御されない。
7. 自動化では最小権限を使い、secretをrepository-controlled codeと同じjob環境へ広く露出させない。
8. downstream処理には人向け文章ではなく、JSONL、最終message file、JSON Schemaなど明示的な出力契約を使う。
9. Codexの変更はtest・lint・type check・behavior確認・diff reviewまで通して初めて完了する。
10. 並列agentはread-heavyな独立作業に向き、write-heavyな同時編集では競合と調整費用が増える。
11. 一つのchatは一つのcoherent outcomeに保ち、仕事が分岐するときだけforkする。
12. Git、patch、branch、review、status、diagnosticsを使い、変更と実行状態を戻せる・説明できる形にする。

### 論証の連鎖

資料集は、導入ページでCLIの作業面を示し、best practicesで文脈・計画・持続的guidance・検証の原則を提示する。コマンドリファレンスと個別ガイドが、その原則を`/plan`、`/permissions`、`/review`、`codex exec`、`--json`、`--output-schema`、`resume`、MCP設定などの操作へ落とす。security資料はsandbox・approval・network経路を分離し、auth資料はcredentialとworkspace policyの境界を補う。最後にCI auto-fix、PR review agents、frontend debugging agentsという構成例が、権限分離・task分割・結果統合を具体化する。

---

## 3. 批判（Critical）

### 時点依存の限界

- command、model名、feature maturity、sandbox実装、認証方式、plugin提供条件は更新されるため、skillへ固定する値は再検証が必要である。
- ページに公開日・対象versionが明記されず、コマンドリファレンスの一部は動的tableでMarkdown本文に展開されない。
- best practicesはCLI、IDE extension、desktop appを横断するため、CLIだけに当てはまる規則と共通規則を区別する必要がある。

### 提供者の立場による盲点

- OpenAI自身の製品資料であり、代替agent、failure rate、token費用、運用要員、vendor lock-inとの比較は行わない。
- 成功経路と推奨構成を中心にし、長期運用での誤検知、並列agentの統合失敗、schema逸脱率などの定量結果は示さない。
- 公式例は構成例であって、多くは実環境で測定されたcase studyではない。

### 未証明の前提

- 利用者がGit、shell、CI、JSON Schema、credential管理を理解し、生成されたdiffとcommandを評価できることを前提にする。
- 「適切なcontext」と「明確なDone when」が品質を改善すると述べるが、どの程度改善するかの比較データはない。
- sandboxとapprovalを設定すれば安全性が高まるが、prompt injection、supply-chain code、hostile DNSなどを完全には排除できない。
- subagentでcontext pollutionを減らせても、誤った要約やmain agentによる統合失敗は別途検証が必要である。

### 最強の反対意見

この資料集は優れた運用地図とreferenceを提供する一方、推奨策の効果を測った独立評価ではない。したがって、ここから作るskillは「公式に説明された運用手順」を再現する用途に限定し、安全性・品質・費用を保証する規範として扱ってはならない。

---

## 4. 適用可能性（Applicability）

### skill化できる候補

- [ ] Goal・Context・Constraints・Done whenで依頼を設計する
- [ ] 曖昧で複雑なtaskをplan-firstへ切り替える
- [ ] prompt・`AGENTS.md`・config・skill・pluginの持続層を選ぶ
- [ ] 対話型CLI・`codex exec`・Codex cloud・subagentを選び分ける
- [ ] sandbox・approval・network経路を分離して最小権限を設計する
- [ ] `codex exec`をJSONL・schema・exit behavior付きのautomationへ組み込む
- [ ] CI credentialとwrite権限をjob分離し、patch経由でPR化する
- [ ] repository・image・web search・MCPから必要contextの入口を選ぶ
- [ ] boundedなsubagentを設計し、main threadへ結果を再統合する
- [ ] tests・checks・diff・専用reviewで完了判定を構成する
- [ ] chatをcoherent outcome単位でresume・fork・compactする
- [ ] ChatGPT、API key、access token、device codeを環境別に選ぶ

### 独立skillに適さない内容

- 個別command・flagの暗記は時点依存性が高く、公式reference検索または用語辞典に適する。
- theme、terminal pet、keymapなど外観・操作嗜好はmethodologyではない。
- インストールcommandだけでは判断過程がなく、独立skillにしない。
- 機能一覧は、複数資料で方法・境界・具体例が揃わない限りskill化しない。

### 予想skill数

**6〜10個**。最終数は三重検証に加え、公式資料内の具体例をA1へ割り当てられるかで決める。

### 優先順位（一般利用者への有用性）

1. sandbox・approval・network経路を分離して最小権限を設計する
2. Goal・Context・Constraints・Done whenで依頼を設計する
3. tests・checks・diff・専用reviewで完了判定を構成する
4. 対話型CLI・`codex exec`・Codex cloud・subagentを選び分ける
5. `codex exec`を機械可読automationへ組み込む
6. boundedなsubagentを設計し、結果を再統合する
7. prompt・`AGENTS.md`・config・skill・pluginの持続層を選ぶ
8. CI credentialとwrite権限を分離する

---

## 品質ゲート

- [x] 主旨を一文で明示
- [x] 骨格を3〜7個の主要論点で構成
- [x] 主要用語を5件以上定義
- [x] 批判段階で3件以上の限界を列挙
- [ ] 拡張コーパス版についてユーザー確認を取得

**ユーザー確認日時**: 未確認
