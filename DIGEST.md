# Codex CLI公式資料 — 精華

> 本文は cangjie-skill により、固定したOpenAI公式資料15件から三重検証を通過し、
> かつ原典の具体例をRIA++のA1へ置けた9方法論だけを再構成したものです。
> 全体の案内は [INDEX.md](./INDEX.md)、用語は [GLOSSARY.md](./GLOSSARY.md) を参照してください。
>
> 著者: OpenAI | 固定取得日: 2026-08-17

## この資料群が解こうとしていること

Codex CLIの公式資料は、単なるcommand一覧ではない。通底しているのは、AIへ大きな自由を渡すほど、
入力、実行場所、権限、通信、出力、検証を暗黙のままにしてはいけないという運用思想である。
Codexはrepositoryを読み、commandを実行し、外部情報へ接続し、ときには変更まで生成する。
したがって「何を頼むか」だけでなく、「どこで」「どの能力で」「どの情報を使い」「何を成果物として」
動くのかを分解しなければ、便利さと危険が同じ設定の中で膨らむ。

公式資料が繰り返す基本形は、最初から最大能力を与えることではない。仕事を小さな契約へ変換し、
最小の実行面と権限から始め、必要な能力だけを局所的に追加する。そして出力を人間向け文章のまま
pipelineへ流さず、機械が判定できる形へ固定する。さらに、外部通信やMCPを「接続済みだから安全」と
一括りにせず、経路とtoolごとに境界を作る。本稿の9方法論は、この一連の設計を異なる角度から支える。

---

## 1. 仕事を正しい実行面へ置く

### 対話・自動化・cloudの実行形態選択

**解く問題**: 同じCodexでも、手元terminalで対話する仕事、CIで繰り返す仕事、隔離環境へ長時間委譲する
仕事では、必要な運用が異なる。入口を誤ると、無人jobが途中の人間承認を待ったり、対話が必要な探索を
硬いpipelineへ押し込んだりする。

**核心**: 人の介入時点、反復性、実行場所、結果を受け取る時点の四軸で選ぶ。探索・編集・実行を
その場で往復するなら対話型CLI。同じ処理をscriptやCIで再現するなら `codex exec`。長時間作業を
隔離環境へ委譲し後から結果をreviewするならCodex cloudである。これは機能比較ではなく運用時間軸の選択だ。

**公式資料の用法**: `npm test` の出力をstdinでexecへ渡し、失敗要約をfileへ保存する例では、
人がturnごとに誘導しない処理をrepeatable pipelineへ変えている。別の例では最終出力をPR commentの
入力として利用する。資料は構成上の到達状態を示すが、成功率や費用分岐点は示さない。

**失効条件**: workflowがまだ不安定ならscheduleへ急がない。実行面がexecに決まった後のJSON field設計は
別方法論の仕事である。

→ [codex-execution-mode-routing](./codex-execution-mode-routing/SKILL.md)

### 非対話実行の入出力契約化

**解く問題**: AIの自由文を後続processが暗黙にparseすると、表示や文体の変化がpipeline failureになる。
また、進捗表示、全event、最終値を一つのstreamへ混ぜるとconsumerごとの責任が曖昧になる。

**核心**: 通常のexecでは進捗をstderr、最終messageをstdoutとして扱う。全state changeが必要ならJSONL、
後続jobがfieldを必要とするなら `--output-schema` で最終responseをJSON Schemaへ拘束する。
観測用streamと成果物contractを分けることで、人向け表示と機械向けAPIを同一視しない。

**公式資料の用法**: project metadata抽出例は `project_name` と `programming_languages` を必須fieldにし、
最終JSONをfileへ保存する。test log例ではinstructionをprompt、観測データをstdin、要約をfileへ分離する。
これは「JSONを出して」と頼むだけでなく、consumer側の要求をschemaへ昇格した例である。

**失効条件**: 人が一度読むだけなら厳密schemaは過剰になり得る。JSONLは一個の最終JSONではない。

→ [codex-exec-io-contract](./codex-exec-io-contract/SKILL.md)

---

## 2. capabilityとpermissionを分ける

### sandboxとapprovalの二層境界設計

**解く問題**: 「安全設定」を一つの強弱sliderとして扱うと、操作を技術的に不可能にすることと、
実行前に人へ尋ねることが混ざる。無人実行では、後者へ依存した設計が停止原因にもなる。

**核心**: sandboxはCodexがread/write/networkできる技術的能力を決める。approval policyは、境界を越える
actionでいつ人へ止めるかを決める。まず必要動作をread、write、execute、networkへ分け、最小sandboxを選ぶ。
次に昇格点をask、deny、事前許可へ割り当てる。hostが十分なsandboxを提供しないなら、containerやVMを
一段外の境界として使う。

**公式資料の用法**: Linux sandboxをhostで直接使えない場合のsecure Dev Container構成は、
非隔離host上でfull accessにするのではなく、実行環境そのものを外側へ封じ込める。

**失効条件**: VM内だから何でも安全とは限らない。host mount、credential、敵対repositoryがcontainer内へ
入れば境界は広がる。破壊操作の対象も広いpathやglobで指定しない。

→ [codex-sandbox-approval-boundary](./codex-sandbox-approval-boundary/SKILL.md)

### 認証方式を利用面と統制境界へ対応させる

**解く問題**: developer workstation、headless host、短命CI runnerへ同じlogin方式を配ると、不要なcredential
保存や共有が起きる。特に認証cacheのcopyは、単なる設定fileの配布ではない。

**核心**: 対話端末ではChatGPT sign-in、GUIのない対話hostではdevice codeまたは別machine callback、
automationではprocess-scoped API keyを候補にする。credentialの方式、寿命、保存先、読取主体、revoke方法を
一つの表で決める。`auth.json` はpassword同等の秘密として扱う。

**公式資料の用法**: headless environmentではdevice code authenticationまたは別machineでlocalhost flowを
完了する選択肢が示される。CI例ではAPI keyを一回のexec processへscopeする。

**失効条件**: public repository、log、artifact、共有homeへcredentialを置かない。組織SSOやrotation周期は
公式資料だけでは決まらない。

→ [codex-auth-boundary-selection](./codex-auth-boundary-selection/SKILL.md)

---

## 3. 外向き通信を一個のnetworkにしない

### 複数通信経路を個別統制する脅威モデル

**解く問題**: search domainを絞ったから、Codexの全trafficも制限されたと考える誤りである。実際にはweb search、
sandboxed command、MCP、direct HTTPが別のsurfaceとして存在する。

**核心**: まずsurface inventoryを作り、それぞれの必要性、鮮度、宛先、approval、loggingを個別に決める。
searchではcachedとliveをcurrentnessとprompt injection riskで比較する。command networkではpermissionが能力を開き、
proxy policyが宛先を狭める。MCPはさらにserverとtoolへ分解する。一経路のdenyを別経路が迂回できないかを確認する。

**公式資料の用法**: package取得等のcommand通信を有効にしながら、proxy policyで許可domainを限定する構成が
示される。これはallowlistだけでnetwork能力が生えるという意味でも、全surfaceがfilterされるという意味でもない。

**失効条件**: web resultはuntrusted inputであり、domain限定だけでprompt injectionが消えるわけではない。
DNS検査やcommand proxyも完全防御ではない。

→ [codex-egress-surface-governance](./codex-egress-surface-governance/SKILL.md)

### MCP接続の必須性・tool範囲・承認の三段階制御

**解く問題**: MCP serverを接続しただけで、その全toolを常時利用可能にすると、正しさと権限が同時に広がる。
反対に、taskに必須のserverが落ちても推測で続ければ、正常終了に見える不完全な成果が生まれる。

**核心**: 第一にserverなしでtaskを続けてよいかをrequiredで決める。第二に `enabled_tools` / `disabled_tools` で
見えるtoolを必要最小限にする。第三に各tool callのapprovalをautomatic、ask、denyへ分ける。
接続可否、tool可視性、呼出し同意は別controlである。必須文脈が欠ける場合はfail closedにする。

**公式資料の用法**: PR review例ではdocs researcher roleに専用MCPとread-only sandboxを与え、API docs調査だけを
担当させる。全reviewerへ全toolを配らない。

**失効条件**: 「便利そう」だけで全serverをrequired、全toolをautomaticにしない。third-party server自体の実装と
data retentionは別監査が必要である。

→ [codex-mcp-control-plane](./codex-mcp-control-plane/SKILL.md)

---

## 4. contextを所在と鮮度でrouteする

### 外部文脈の入口選択

**解く問題**: 不足情報を長いpromptだけで埋めようとすると、視覚情報、最新情報、社内system、過去の判断履歴が
同じ形式へ押し込まれる。情報に適した入口を選ばなければ、鮮度や信頼境界を失う。

**核心**: visual stateはimage、変動する公開情報はweb search、外部systemの構造化contextはMCP、既存taskの判断履歴は
resume/forkから得る。選択軸は情報の所在、鮮度、構造、信頼境界、履歴継続の必要性である。入口を選んだ後に、
inspect対象、期待output、制約、done criteriaを添える。

**公式資料の用法**: UIのspacing・typography差をscreenshotまたはdesign referenceで渡し、修正後に新しいscreenshotを
撮って比較する例がある。画像は証拠を与えるが、「いい感じに」の意味までは与えないためtask languageが必要になる。

**失効条件**: local repositoryだけで答えが出るなら外部入口を増やさない。web resultは検証し、無関係な別成果は
一つのconversationへ混ぜずforkする。

→ [codex-context-entry-routing](./codex-context-entry-routing/SKILL.md)

---

## 5. 並列化より先に境界を作る

### bounded subagentへの分解と要約再統合

**解く問題**: subagentを増やすだけでは速くならない。同じfileを複数agentが変更すれば競合し、中間logを全部親へ
戻せばcontext pollutionが増える。価値は人数ではなく、問いとauthorityを分離できることにある。

**核心**: 各subagentへ一つの問い、対象scope、禁止操作、返却形式、done criteriaを与える。history探索、risk評価、
docs照合のようなread-heavy仕事を並列化し、write-heavy部分はsingle writerへ集約する。roleごとにmodel、sandbox、MCP、
toolを最小化し、親は出典付き要約を比較して矛盾と次actionを決める。

**公式資料の用法**: PR reviewをhistory explorer、risk reviewer、API docs researcherへ分ける例と、frontend障害を
browser reproduction、code tracing、minimal fixへ段階分解する例がある。どちらも証拠収集を先行し、変更担当を限定する。

**失効条件**: 小作業を過剰分解しない。同じworking directory・同じfileを同時変更するなら、single writer、段階実行、
またはworktree隔離へ戻す。最適agent数の定量基準は資料にない。

→ [codex-bounded-subagents](./codex-bounded-subagents/SKILL.md)

---

## 6. CIではcredentialとwrite authorityを同居させない

### CI修正の権限分離とpatch受け渡し

**解く問題**: CI failureをAIに直させるjobへAPI key、repository-controlled test、write tokenを同時に置くと、
一つの侵害が推論credentialとrepository変更権限の両方へ届く。

**核心**: Codex jobはread-only checkoutと短命な推論credentialだけを持ち、失敗再現、最小修正、retestを行う。
変更はbinary-safe patch、元commit、hashをartifactとして渡す。別jobが照合、適用、test、diff確認を済ませてからbranch、
署名、push、PR作成を行う。境界を越えるのは任意commandでなく差分である。

**公式資料の用法**: GitHub Actions例ではCodex jobが `contents: read` のみを持ち、差分がある場合だけpatch artifactを作る。
後続jobが `codex/auto-fix-$RUN_ID` branchへcommitしPRを開く。資料はworkflow構造を示すが、特定repositoryでの
成功率や安全性の実測値は示さない。

**失効条件**: patchを無検査でmainへ直接適用してはいけない。branch protection、署名、artifact retentionは組織側の
policyで補う必要がある。

→ [codex-ci-patch-handoff](./codex-ci-patch-handoff/SKILL.md)

---

## 陥穽と反例

### 1. Git checkpointなしで大きな変更を委譲する

変更前の状態が曖昧だと、生成差分と既存差分を分けられず、rollbackもreviewも難しくなる。未commit変更がある、
対象branchが不明、元commitをartifactへ記録していないことが予兆である。

### 2. sandboxとapprovalを外せば自動化できると考える

無人化のために二つの境界を同時に消すと、repository code、外部network、host filesystemへ影響が連鎖する。
外側のVM/container境界、mount、secret配置を確認せず `danger-full-access` を使うことが危険信号である。

### 3. domain ruleが全trafficを制限すると考える

search、command network、MCP、direct HTTPは別経路である。search filterまたはcommand proxy一つだけを見て
「外部送信は限定済み」と結論するのはsurface漏れである。

### 4. web resultをinstructionとして信頼する

検索結果はuntrustedであり、prompt injectionや誤情報を含み得る。取得文がsystemの指示変更、秘密の開示、
別domainへの送信を要求したら、情報ではなく攻撃入力として分離する。

### 5. 全MCP・全toolを先に接続する

workflowが固まる前にtool surfaceを広げると、agentがどのtoolを使うべきか曖昧になり、approval policyも粗くなる。
必要server、必要tool、failure時の扱いを説明できない接続が予兆である。

### 6. write-heavy仕事をsubagentで同時編集する

read-heavy探索と違い、共有fileの同時writeはmerge collisionと状態不整合を生む。同じlockfile、manifest、generated stateを
複数agentが触るなら、single writerまたはworktree分離へ切り替える。

---

## 公式資料の限界

第一に、公式資料は製品の設定と推奨patternを説明する立場にあり、第三者によるsecurity auditや比較benchmarkではない。
構成例が示されても、特定組織での成功率、事故率、費用対効果が証明されたわけではない。

第二に、資料は継続更新される。ここでのsourceは2026-08-17に取得しSHA-256を固定した15件である。将来のCLI version、
default sandbox、認証flow、option名が変われば再取得と再蒸留が必要になる。

第三に、公式資料だけでは組織固有の脅威モデル、法令、data residency、secret rotation、branch protectionを決められない。
本稿のskillは判断枠を与えるが、外部systemの安全性や組織policyを代替しない。

第四に、三重検証を通った「skillとpluginの選択」は、固定コーパス内に最後まで適用したworked caseがなかったためskill化を
見送った。RIA++のA1を満たすために架空事例を作らない、という制約そのものが今回の蒸留品質を守っている。

---

## 重要語の速查

| 用語 | この資料での意味 | 混同しやすいもの |
|---|---|---|
| sandbox mode | 技術的に可能なread/write/network範囲 | approval policy |
| approval policy | action前に人へ確認する条件 | 技術的禁止 |
| codex exec | script・CI向け非対話入口 | interactive TUI |
| JSONL | 全eventの行stream | schemaで固定した最終JSON |
| MCP | 外部tool・contextへのserver接続 | 静的prompt context |
| subagent | bounded taskを処理する独立agent | main chatの追加turn |

完全版は [GLOSSARY.md](./GLOSSARY.md) を参照。

## 三文だけ持ち帰るなら

1. Codexへ仕事を渡す前に、実行面、能力、承認、通信、出力を別々の契約として決める。
2. search・command network・MCP・HTTPは別surfaceであり、一つのallowlistを全経路の安全証明にしない。
3. 自動化と並列化はauthorityを広げる理由ではなく、patch、schema、bounded roleで境界を細かくする理由である。

