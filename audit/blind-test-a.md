# Blind Test A — Codex CLI routing

## 判定方針

- `selected_skill` は `INDEX.md` にある9件から、promptの中心課題に最も直接対応するものを1件だけ選んだ。該当しない場合は `none` とした。
- `would_trigger` は、その表の対象skillを実際に発火するかを示す。
- 判定には各対象の `SKILL.md`、INDEXのskill名・説明、各test caseの `id` と `prompt` だけを使用した。

## codex-execution-mode-routing

| id | prompt | selected_skill | would_trigger | reason | if_triggered_action |
|---|---|---|---|---|---|
| should-trigger-01 | この調査は手元の対話型CLI、codex exec、cloudのどれで回すべき？ | `codex-execution-mode-routing` | yes | 対話型CLI・exec・cloudの実行面選択そのものが中心課題。 | 介入モデル、反復性、実行場所、結果の受領方法を整理し、実行面を1つ選ぶ。 |
| should-trigger-02 | 毎晩同じrepository検査をCIで無人実行したい。Codexの実行方法を決めて。 | `codex-execution-mode-routing` | yes | CIでの反復可能な無人実行に適したCodex surfaceを決める依頼。 | 無人反復として `codex exec` を選び、入出力・権限・credentialの下位設計へ渡す。 |
| should-trigger-03 | 長いmigration調査を隔離環境へ投げ、明日の朝に結果をreviewしたい。 | `codex-execution-mode-routing` | yes | 長時間作業を非同期に委譲し、後で結果を受け取る実行モデルの選択。 | 非同期隔離としてcloudを選び、実行条件と受領方法を明記する。 |
| should-not-trigger-01 | codex execの最終出力をJSON Schemaで固定したい。field設計をして。 | `codex-exec-io-contract` | no | exec採用後の最終出力schema設計であり、実行面は既に確定している。 | —（対象skillは発火しない） |
| should-not-trigger-02 | この小さな関数の名前を一つ提案して。 | `none` | no | 実行面、機械入出力、権限境界など9 skillのrouting対象ではない。 | —（対象skillは発火しない） |
| edge-01 | 今はterminalで試しているが、安定したら週次jobにしたい。 | `codex-execution-mode-routing` | yes | 対話的な試行から反復可能な定期jobへ移す時点と実行面を決める課題。 | 現状は対話型CLIを維持し、workflowの安定条件を満たした後に週次 `codex exec` へ移す基準を定める。 |

## codex-exec-io-contract

| id | prompt | selected_skill | would_trigger | reason | if_triggered_action |
|---|---|---|---|---|---|
| should-trigger-01 | codex execの進捗はmonitorへ、最終JSONだけ次jobへ渡したい。stdoutとstderrを設計して。 | `codex-exec-io-contract` | yes | execのprogress、最終値、downstream consumerのchannel分離が中心課題。 | progressをstderr、最終値をstdoutまたはfileへ割り当て、次job向けschemaを固定する。 |
| should-trigger-02 | AIの自由文でpipelineが壊れる。--output-schemaで必須fieldを固定したい。 | `codex-exec-io-contract` | yes | downstream parseを安定させるためのoutput schema契約を求めている。 | consumerを確認し、必須field・型・許容値をJSON Schemaで定義してfailure処理も決める。 |
| should-trigger-03 | test logをstdinで渡し、Codexの全eventをJSONLで監査したい。 | `codex-exec-io-contract` | yes | stdinによるdata入力とJSONL event streamの監査設計が明示されている。 | 指示とstdin dataを分離し、`--json` のJSONLをevent consumerへ接続して最終成果物の扱いも別に定める。 |
| should-not-trigger-01 | この仕事を対話型CLIとCodex cloudのどちらへ置くべき？ | `codex-execution-mode-routing` | no | 入出力契約ではなく、同期対話か非同期委譲かという実行面選択。 | —（対象skillは発火しない） |
| should-not-trigger-02 | API keyとrepository write tokenを別のCI jobへ分けたい。 | `codex-ci-patch-handoff` | no | CI job間で推論credentialとwrite authorityを分離する課題。 | —（対象skillは発火しない） |
| edge-01 | 一回だけ人が読むcodex execの回答をfileへ保存したい。schemaも必要？ | `codex-exec-io-contract` | yes | exec採用後のfile artifactとschema要否を決める小規模な入出力契約の相談。 | 人だけが一度読むconsumerなら最終messageのfile保存を選び、機械parse要件がない限りschemaは追加しない。 |

## codex-ci-patch-handoff

| id | prompt | selected_skill | would_trigger | reason | if_triggered_action |
|---|---|---|---|---|---|
| should-trigger-01 | CI failureをCodexに直させたいが、Codex jobにはcontents: readしか与えたくない。PRまでどう繋ぐ？ | `codex-ci-patch-handoff` | yes | read-only生成jobから別jobのPR作成へ安全に差分を渡す設計そのもの。 | 生成jobをread-onlyにし、patch・hash・元commitをartifact化し、検証後に別jobでbranchとPRを作る。 |
| should-trigger-02 | repositoryのtest scriptからAPI keyを隠しつつ、自動修正patchを作りたい。 | `codex-ci-patch-handoff` | yes | repository-controlled code、AI credential、生成差分のtrust boundary分離が必要。 | authority inventoryを作り、credential露出を限定した生成jobからbinary-safe patchだけを後続jobへ渡す。 |
| should-trigger-03 | 署名鍵をAI processへ渡さず、生成差分だけ別jobで署名・pushしたい。 | `codex-ci-patch-handoff` | yes | AI processと署名・push authorityをjob間で分離する明示的な依頼。 | AI側は差分artifactのみ生成し、元commit照合・test・差分確認後に別jobで署名とpushを行う。 |
| should-not-trigger-01 | localでCodexに小さなtypoを直させ、私が手動commitする。 | `none` | no | localの通常修正であり、CI job間のcredential・patch handoffは存在しない。 | —（対象skillは発火しない） |
| should-not-trigger-02 | codex execからproject_nameをJSONで返して次stepが読むようにしたい。 | `codex-exec-io-contract` | no | downstreamがparseするstructured outputの契約であり、patchやwrite authorityの分離ではない。 | —（対象skillは発火しない） |
| edge-01 | read-only jobがpatchを作り、別jobが無検査でmainへ直接pushする設計でよい？ | `codex-ci-patch-handoff` | yes | patchをtrust boundaryとして渡すCI設計だが、適用側の検査と保護が欠けた危険な構成。 | 無検査の直接pushを避け、元commit照合、patch適用、test、差分確認を経て保護branchまたはPRへ渡す。 |
