# Codex導入・初期運用PMO — 10のskill

このフォルダには、OpenAIのCodex CLI公式資料を読んで作った9つのskillと、日常の横断PMO運用を担う1つのskillが入っています。

「Codex CLIをまだ使ったことがない」「skillやMCPという言葉も知らない」という人でも、
このREADMEだけで全体像が分かるように説明します。

一言でいえば、これはCodexにコードを書かせるskill集ではありません。

> Codexをプロジェクトへ参加させ、事故を起こさず仕事を始められる状態まで整えるPMO skill集です。

## 担当する範囲

プロジェクト発足から、初期運用を安定させるところまでを担当します。

- Codexをどこで動かすか決める
- 権限、認証、外部接続を設計する
- agentの役割分担を決める
- 入出力と成果物の形式を決める
- CIやMCPとの接続方法を整える
- 初期運用で安全に動くことを確認する

次のような定常運用の実務は担当しません。

- 課題一覧やbacklogの管理
- 個別bugの原因調査と修正
- 障害対応と復旧
- 日常的な保守、release、性能改善

これらの仕事を行う別のagentやskillに対して、開始時の役割・権限・報告形式を設計するところまでが本skill集の範囲です。

## まず、これは何ですか？

### Codexとは

Codexは、コードや設定ファイルを読んだり、修正したり、commandを実行したりできるAIです。

### CLIとは

CLIは「文字でcommandを入力してcomputerを操作する画面」のことです。
WindowsのPowerShellや、macOS・Linuxのterminalが該当します。

### skillとは

skillは、Codexに特定の仕事の進め方を教える説明書です。

たとえば「安全にやって」とだけ頼んでも、安全の意味は人によって違います。
このskill集は、次のような判断を具体的な手順にします。

- どこでCodexを動かすか
- どのfileを読ませ、どこへ書かせるか
- 外部networkへ接続させるか
- login情報をどこへ置くか
- AIの出力を次のprogramへどう渡すか

skillはCodex本体を改造するものではありません。
仕事に応じて読み込まれる、再利用可能な作業手順です。

## このskill集が必要な理由

Codexは便利ですが、頼み方や権限設定が曖昧だと、次の問題が起きます。

- 人が確認するはずの操作が自動実行される
- 必要のないfileやnetworkへアクセスできてしまう
- CIの秘密鍵とrepositoryの書込み権限が同じ場所に集まる
- AIの自由文が変わっただけで自動処理が壊れる
- 複数のAIが同じfileを同時に編集して衝突する
- Web検索を制限したつもりでも、別の通信経路が残る

公式資料を元にした9つのskillは、これらを一つの大きな「安全設定」で済ませず、問題ごとに分けて判断します。加えてPMO運用skillが、実際の複数プロジェクトの進行を扱います。

## 10のskill

### 1. どこでCodexを動かすか決める

#### `codex-execution-mode-routing`

対話型CLI、`codex exec`、Codex cloudのどれを使うか決めます。

- 手元で会話しながら作業する → 対話型CLI
- CIや定期処理で同じ仕事を繰り返す → `codex exec`
- 長い仕事を別環境へ預け、後で結果を受け取る → Codex cloud

[詳しい説明](./codex-execution-mode-routing/SKILL.md)

### 2. Codexの出力をprogramで扱える形にする

#### `codex-exec-io-contract`

`codex exec` の進捗、最終回答、JSON、保存fileをどう分けるか決めます。

たとえば、画面には進捗を表示しながら、次のprogramには決まった形のJSONだけを渡せます。

[詳しい説明](./codex-exec-io-contract/SKILL.md)

### 3. CIの自動修正を安全にPRへ渡す

#### `codex-ci-patch-handoff`

Codexが修正案を作る場所と、repositoryへ書き込む場所を分けます。

Codex側には読取り権限だけを与え、変更内容をpatchという差分fileにします。
別のjobがpatchを検査してからbranchやPRを作ります。

[詳しい説明](./codex-ci-patch-handoff/SKILL.md)

### 4. Codexに何を許すか決める

#### `codex-sandbox-approval-boundary`

次の二つを分けて考えます。

- sandbox: Codexが技術的に何をできるか
- approval: 実行前に人の確認が必要か

「できない」と「確認すればできる」は別物です。

[詳しい説明](./codex-sandbox-approval-boundary/SKILL.md)

### 5. 外部networkへの出口を調べる

#### `codex-egress-surface-governance`

Codexには複数の外部通信経路があります。

- Web検索
- commandからのnetwork接続
- MCP
- programからの直接HTTP通信

一つの経路を制限しても、ほかの経路まで自動的に制限されるとは限りません。
このskillは経路を一つずつ確認します。

[詳しい説明](./codex-egress-surface-governance/SKILL.md)

### 6. 大きな仕事を複数のAIへ安全に分ける

#### `codex-bounded-subagents`

subagentは、親のAIから小さな仕事を任される別のAIです。

調査や比較のような「読む仕事」は分担しやすい一方、同じfileを複数のAIが同時に書くと衝突します。
このskillは担当範囲を狭く決め、最後に親AIが結果をまとめる手順を作ります。

[詳しい説明](./codex-bounded-subagents/SKILL.md)

### 7. Codexへ情報を渡す方法を選ぶ

#### `codex-context-entry-routing`

必要な情報の種類に応じて、入口を選びます。

- 画面の見た目 → screenshotや画像
- 今日の価格や最新version → Web検索
- 社内資料や外部service → MCP
- 前の作業の判断履歴 → conversationのresumeまたはfork

画像だけを渡して目的が曖昧な場合は、作業を始める前に完了条件を補います。

[詳しい説明](./codex-context-entry-routing/SKILL.md)

### 8. login方法と秘密情報の置き場所を決める

#### `codex-auth-boundary-selection`

使用場所に応じて、ChatGPT login、API key、device codeなどを選びます。

特に `auth.json` は普通の設定fileではなく、passwordと同じ種類の秘密として扱います。

[詳しい説明](./codex-auth-boundary-selection/SKILL.md)

### 9. MCPで使える道具を制限する

#### `codex-mcp-control-plane`

MCPは、Codexを外部の資料や道具へ接続する仕組みです。

このskillは次の三つを別々に決めます。

1. MCP serverが使えない場合、仕事を中止するか
2. Codexへどのtoolを見せるか
3. toolを実行するとき、人の確認を必要とするか

[詳しい説明](./codex-mcp-control-plane/SKILL.md)

### 10. 複数プロジェクトを止めずに回す

#### `codex-pmo-orchestration`

PMOが、10分粒度のタスク分解、担当・監査の並列実行、停止イベントの追跡、リリース直行レーンを運用します。

[詳しい説明](./codex-pmo-orchestration/SKILL.md)

## どのskillを使えばよいか迷ったら

| 困っていること | 最初に見るskill |
|---|---|
| CLI、exec、cloudのどれを使うか | `codex-execution-mode-routing` |
| JSONやstdout・stderrを設計したい | `codex-exec-io-contract` |
| CIで安全に自動修正したい | `codex-ci-patch-handoff` |
| file・commandの権限を決めたい | `codex-sandbox-approval-boundary` |
| 外部通信を制限したい | `codex-egress-surface-governance` |
| 複数のAIへ仕事を分けたい | `codex-bounded-subagents` |
| 画像・Web・MCPのどれで情報を渡すか | `codex-context-entry-routing` |
| loginやAPI keyを扱いたい | `codex-auth-boundary-selection` |
| MCP serverやtoolを制限したい | `codex-mcp-control-plane` |
| 複数プロジェクトの停滞、重複、並行実行、リリースを管理したい | `codex-pmo-orchestration` |

## 「依存」と「統合」は違います

### 統合したもの

同じ問題をほぼ同じ方法で解く候補は、一つのskillにまとめました。

- network permission、proxy、Web検索risk → `codex-egress-surface-governance`
- subagentの並列化、役割、使用resource → `codex-bounded-subagents`
- 最小権限と段階的な権限拡張 → `codex-sandbox-approval-boundary`

これは、似たskillが同時に反応するのを防ぐためです。

### 分けたまま依存関係にしたもの

別の問題を解くskillは、一緒に使う場合でも分けています。

- `codex-ci-patch-handoff` は `codex-sandbox-approval-boundary` を前提にする
- `codex-egress-surface-governance` は `codex-sandbox-approval-boundary` を前提にする
- `codex-mcp-control-plane` は `codex-egress-surface-governance` を前提にする

ここでいう依存は、programのlibrary依存ではありません。
「この順番で考えると判断を間違えにくい」という知識上の依存です。

すべてを一つの巨大なskillにすると、MCPの小さな設定をしたいだけなのに、CIや認証まで反応するようになります。
そのため、独立した問題は分け、関係だけを明示しています。

関係図は [INDEX.md](./INDEX.md) にあります。

## 中身の見方

各skill directoryには次のfileがあります。

| file | 内容 |
|---|---|
| `SKILL.md` | Codexが読む作業手順 |
| `test-prompts.json` | 正しく反応するか確かめる質問集 |
| `test-results.md` | 独立したAIによる試験結果 |

公式資料由来9件の `SKILL.md` はRIA++という形で構成されています。別系列の `codex-pmo-orchestration` は、日常運用向けのPMO契約として構成されています。

| 記号 | 意味 |
|---|---|
| R | 公式資料の原文 |
| I | 原文をかみ砕いた説明 |
| A1 | 公式資料に実際に掲載された使用例 |
| A2 | このskillを使うべき状況と言葉の信号 |
| E | Codexが実行する具体的手順 |
| B | 使ってはいけない状況と失敗例 |

公式資料に実例がなかった内容は、実例を作り話で補っていません。

## 試験結果

公式資料由来9件は54 routing promptsで独立blind test 54/54、別系列PMO 1件は7 forward-test promptsで独立forward test 7/7です。合計は10 skill・61 promptsですが、試験方式は別々に記録しています。

- 呼び出すべき質問
- 呼び出してはいけない誘餌の質問
- 判断が曖昧になる境界の質問
- ほかのskillと間違えやすい質問

作成に参加していない独立subagentが、正解を見ずに判定しました。
初回は54件中53件が通過し、曖昧なscreenshot依頼で1件失敗しました。
skill本文の矛盾を修正して同じ質問を再試験し、最終的に54件すべて通過しました。

詳しい記録は [blind-test-summary.md](./audit/blind-test-summary.md) にあります。

## もっと詳しく読みたい場合

- 最初に全体を読む: [DIGEST.md](./DIGEST.md)
- skill同士の関係を見る: [INDEX.md](./INDEX.md)
- 用語を調べる: [GLOSSARY.md](./GLOSSARY.md)
- 使用した公式資料を確認する: [SOURCE_MANIFEST.md](./SOURCE_MANIFEST.md)
- 候補の採用・棄却理由を見る: [verified.md](./verified.md) / [rejected/](./rejected/)
- 納品検査を見る: [DELIVERY_MANIFEST.md](./DELIVERY_MANIFEST.md)

## インストールについて

まずrepositoryをcloneします。

```powershell
git clone https://github.com/omusubiman5/codex-pmo-skills.git
cd codex-pmo-skills
```

ユーザー単位でCodexへインストールする場合の標準的な場所は次です。

```text
%USERPROFILE%\.codex\skills
```

repository直下にある、試験を通過した10の `codex-*` skill directoryを丸ごとコピーします。
候補資料、棄却記録、監査fileをskill directoryへ混ぜる必要はありません。

PowerShellの例:

```powershell
$target = Join-Path $env:USERPROFILE ".codex\skills"
$skillNames = @(
  "codex-execution-mode-routing",
  "codex-exec-io-contract",
  "codex-ci-patch-handoff",
  "codex-sandbox-approval-boundary",
  "codex-egress-surface-governance",
  "codex-bounded-subagents",
  "codex-context-entry-routing",
  "codex-auth-boundary-selection",
  "codex-mcp-control-plane",
  "codex-pmo-orchestration"
)

foreach ($name in $skillNames) {
  Copy-Item -LiteralPath (Join-Path $PWD $name) -Destination $target -Recurse
}
```

既に同名directoryがある場合は上書きせず、既存版との差分を確認してください。

## 大切な注意

- このskill集は、安全を自動的に保証する装置ではありません。
- 組織のsecurity policy、法令、秘密情報の管理規則を置き換えません。
- OpenAI公式資料は更新されるため、将来のCodexでは設定名や既定値が変わる可能性があります。
- この成果物は2026-08-17に取得した15件の公式資料へ固定して作られています。
