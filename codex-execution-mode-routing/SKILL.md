---
name: codex-execution-mode-routing
description: |
  Codex作業を対話型CLI、codex exec、Codex cloudのどこで実行するか決めるときに使う。「CIで回したい」「バックグラウンドへ委譲」「terminalで反復」「interactive / non-interactive / cloud」が信号。出力形式の設計だけ、subagentへの分解だけ、既に実行面が確定した作業には使わない。
source_book: Codex CLI official documentation — OpenAI
source_chapter: Codex CLI / Codex cloud / Non-interactive mode
tags: [codex, execution-mode, automation, cloud]
related_skills:
  - slug: codex-exec-io-contract
    relation: composes-with
  - slug: codex-bounded-subagents
    relation: contrasts-with
---

# 対話・自動化・cloudの実行形態選択

## R — 原文 (Reading)

> “You work from the terminal: Explore, edit, and run a repository in one focused loop.” “You need scripting or CI: Run a non-interactive command in a repeatable workflow.” “Work needs to run in the background: Delegate a longer task and return when it is ready.”
>
> — OpenAI, Codex CLI / Codex cloud

## I — 方法論骨架 (Interpretation)

実行面は機能の多さではなく、人がいつ介入するかで選ぶ。
terminal内で探索、編集、実行を往復するなら対話型CLIを使う。
同じ入力と契約で繰り返すpipelineやCIなら `codex exec` にする。
長時間作業を隔離環境で走らせ、後から結果を受け取るならcloudへ委譲する。
まず仕事の時間軸、反復性、実行場所、受領方法を確定し、その後に権限と出力契約を設計する。

## A1 — 公式資料中の適用

### ケース1: test出力を非対話pipelineで要約
- **問題**: 大量の `npm test` 出力から失敗と最小修正候補を抽出したい。
- **方法論の使用**: test出力をstdinで `codex exec` へ渡し、指示はprompt引数へ固定する。
- **結論**: 人が逐次誘導しない反復可能な処理なので対話型CLIではなくexecを選ぶ。
- **結果**: 最終messageが `test-summary.md` に保存される構成が示される。実環境の成功率は資料にない。

### ケース2: PR commentをpipelineから生成
- **問題**: CIログを後続のPR処理へ渡せる一つの成果物にしたい。
- **方法論の使用**: 非対話実行の最終出力をfileへ保存する。
- **結論**: CI内の機械的な受け渡しとしてexecを使う。
- **結果**: 後続stepがそのfileをPR comment本文として利用する構成が示される。

## A2 — 触発場面 (Future Trigger)

### 使用場面

1. 手元terminalで対話を続けるか、非対話jobへ移すか迷っている。
2. CI・scheduled job・scriptにCodexを組み込みたい。
3. 長時間または並列作業をcloudへ委譲する妥当性を判断したい。
4. 同じ作業がmanual loopからrepeatable workflowへ成熟した。

### 言語信号

- 「これはCLIとexecのどちらで回す？」
- 「CI / pipeline / non-interactiveに組み込みたい」
- 「backgroundで走らせて後で受け取りたい」
- “interactive vs cloud” / “which Codex surface?”

### 隣接skillとの区別

- `codex-exec-io-contract` はexec採用後のstdout・stderr・schemaを決める。本skillはその前段の実行面を選ぶ。
- `codex-bounded-subagents` は一つの実行内で仕事を役割分解する。cloudへのtask委譲との同一視を避ける。

## E — 実行手順 (Execution)

1. **介入モデルを分類する** — 同期対話、無人反復、非同期委譲のいずれかを明記できれば完了。
2. **運用条件を記録する** — 反復頻度、想定時間、実行環境、結果の受領者が埋まれば完了。
3. **実行面を一つ選ぶ** — 同期対話=CLI、無人反復=exec、非同期隔離=cloudを基準に理由を一文で残す。
4. **下位設計へ渡す** — execなら入出力契約、権限境界、credential scopeを別途確定できれば完了。

## B — 境界 (Boundary)

### 使用しない場面

- 既にexec採用済みでJSON Schemaだけを決める場合。
- 一つのtask内の調査役を分けるだけの場合。
- 安定していないworkflowを、反復可能性の検証なしにscheduleする場合。

### 公式資料が警告する失敗

- 一つのchatへ無関係な成果を詰め込むとcontextが散る。
- 安定していないworkflowをscheduleしてはいけない。
- 非対話jobは途中approvalに依存させない。

### 資料の限界

- 資料は選択軸と例を示すが、規模別の性能比較や費用分岐点を実測していない。

## 関連skills

- composes-with: `codex-exec-io-contract` — execを選んだ後に機械契約を設計する。
- contrasts-with: `codex-bounded-subagents` — 実行面の選択と内部役割分解は別判断。

## 監査情報

- **検証通過**: V1 ✓ / V2 ✓ / V3 ✓
- **原典case**: c03, c04
- **テスト通過率**: 100% (6/6)
- **蒸留日**: 2026-08-17
