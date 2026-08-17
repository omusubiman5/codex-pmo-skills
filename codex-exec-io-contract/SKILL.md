---
name: codex-exec-io-contract
description: |
  codex execをCI・script・他processへ接続し、stdout、stderr、JSONL、output schema、file artifactの契約を決めるときに使う。「JSONで受けたい」「進捗と最終値を分ける」「stdinを渡す」「downstreamでparse」が信号。実行面の選択、権限設計、自由な対話だけには使わない。
source_book: Codex CLI official documentation — OpenAI
source_chapter: Non-interactive mode — output streams, JSONL, output schema
tags: [codex-exec, jsonl, json-schema, automation]
related_skills:
  - slug: codex-execution-mode-routing
    relation: composes-with
  - slug: codex-ci-patch-handoff
    relation: composes-with
---

# 非対話実行の入出力契約化

## R — 原文 (Reading)

> “Codex streams progress to `stderr` and prints only the final agent message to `stdout`.” “When you enable `--json`, `stdout` becomes a JSON Lines (JSONL) stream.” “Use `--output-schema` to request a final response that conforms to a JSON Schema.”
>
> — OpenAI, Non-interactive mode

## I — 方法論骨架 (Interpretation)

非対話実行では、人向け文章を暗黙のAPIにしない。
進捗、event、最終値、保存artifactを別の流れとして設計する。
通常実行では進捗をstderr、最終messageをstdoutとして扱う。
全eventが必要ならJSONL、後続processがfieldを要求するならJSON Schemaで最終値を拘束する。
観測用streamとdownstream契約を分けることで、表示変更がpipelineを壊す範囲を小さくする。

## A1 — 公式資料中の適用

### ケース1: project metadataをSchemaで固定
- **問題**: 後続処理が自由文でなく安定fieldを必要とする。
- **方法論の使用**: `project_name` と `programming_languages` を必須にしたschemaを `--output-schema` へ渡し、`-o` でfileへ保存する。
- **結論**: prompt上の希望ではなくJSON Schemaを最終値の契約にする。
- **結果**: 公式例は必須fieldを持つJSON最終出力を示す。実測成功率は示さない。

### ケース2: promptとtest logを分離
- **問題**: 大量のtest出力と指示を混ぜずに処理したい。
- **方法論の使用**: 指示をprompt引数、観測値をstdinとしてexecへ渡し、最終値をfile化する。
- **結論**: instruction channelとdata channelを分ける。
- **結果**: 最終要約を `test-summary.md` に保存するpipelineが示される。

## A2 — 触発場面 (Future Trigger)

### 使用場面

1. exec出力をCIの次stepがparseする。
2. progress表示と最終成果物を別々に保存したい。
3. event履歴をJSONLで監視・監査したい。
4. 既存commandの出力をstdin contextとして渡したい。

### 言語信号

- 「stdoutとstderrをどう分ける？」
- 「--json / JSONL / --output-schemaを使いたい」
- 「後続jobでparseできる形にして」
- “prompt plus stdin” / “machine-readable output”

### 隣接skillとの区別

- `codex-execution-mode-routing` はexecを選ぶまで。本skillはexec採用後の通信契約を作る。
- `codex-ci-patch-handoff` はpatchをsecurity boundaryとして渡す。一般のstructured outputは本skillが扱う。

## E — 実行手順 (Execution)

1. **consumerを列挙する** — 人、監視器、後続jobごとに必要情報を一行ずつ書ければ完了。
2. **channelを割り当てる** — progress=stderr、最終値=stdout/file、event=JSONLを選び、重複用途がなければ完了。
3. **最終契約を固定する** — 必須field・型・許容値をschemaにし、自由文依存がなくなれば完了。
4. **failureを試す** — invalid output、non-zero exit、空stdinを後続処理が明示的に拒否または扱えれば完了。

## B — 境界 (Boundary)

### 使用しない場面

- 人が一度読むだけの対話型session。
- repository write権限やsecretの配置を決める場合。
- JSONLの全eventを単一の最終JSONと誤認する場合。

### 公式資料が警告する失敗

- `--json` はstdout全体をJSONL event streamへ変えるため、通常の最終message前提のconsumerと混用しない。
- Git repository検査をskipするoptionは、信頼できるdirectoryに限定する。

### 資料の限界

- Schema conformanceの例はあるが、長期versioningやconsumer migration規則は扱わない。

## 関連skills

- composes-with: `codex-execution-mode-routing` — exec選択後の契約を具体化する。
- composes-with: `codex-ci-patch-handoff` — patch artifact以外のstatus/outputも明示契約にする。

## 監査情報

- **検証通過**: V1 ✓ / V2 ✓ / V3 ✓
- **原典case**: c01, c03, c04
- **テスト通過率**: 100% (6/6)
- **蒸留日**: 2026-08-17
