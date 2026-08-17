---
name: codex-bounded-subagents
description: |
  大きなCodex作業を、競合しにくいread-heavyな役割へ分け、各subagentのinstructions・model・sandbox・toolsを限定して親へ要約統合するときに使う。「subagentで並列調査」「役割を分ける」「同じfileを触らせたくない」が信号。cloudへの非同期委譲、単一agentで十分な小作業、write-heavyな同時編集には使わない。
source_book: Codex CLI official documentation — OpenAI
source_chapter: Agent configuration — Subagents / Best practices
tags: [subagents, parallelism, orchestration, least-privilege]
related_skills:
  - slug: codex-execution-mode-routing
    relation: contrasts-with
  - slug: codex-context-entry-routing
    relation: composes-with
  - slug: codex-mcp-control-plane
    relation: composes-with
---

# bounded subagentへの分解と要約再統合

## R — 原文 (Reading)

> “Subagents work best when each one has a narrow, well-defined task.” “Use them for parallel, mostly read-heavy work, and have the parent agent synthesize the results.”
>
> — OpenAI, Agent configuration — Subagents

## I — 方法論骨架 (Interpretation)

subagentは人数を増やす機能ではなく、contextとauthorityを分割する仕組みとして使う。
各役割へ一つの問い、対象範囲、禁止事項、返却形式を与える。
独立した探索・比較・risk評価などread-heavy作業を並列にする。
同じfileへのwrite-heavy編集は競合するため、一つのwriterまたは段階実行へ戻す。
役割に応じてmodel、sandbox、tool surfaceを狭め、親agentは生logでなく要約された証拠を統合する。

## A1 — 公式資料中の適用

### ケース1: PR reviewを三役へ分割
- **問題**: 大きなPRのhistory、security risk、API correctnessを一つのcontextで同時に追いにくい。
- **方法論の使用**: history explorer、risk reviewer、API docs researcherへ独立したread-heavy任務を与える。
- **結論**: 異なる証拠源を並列収集し、親がreviewへ統合する。
- **結果**: 公式資料は役割別の分解例を示すが、速度改善の実測値は示さない。

### ケース2: frontend障害を段階分解
- **問題**: 視覚的な不具合の再現、code path特定、修正が混線する。
- **方法論の使用**: browser reproduction、code tracing、minimal fixを別段階・別役割へ割り当てる。
- **結論**: 証拠収集を先行し、writerを最後へ限定する。
- **結果**: 再現証拠から最小修正、再検証へ進む構成例が示される。

## A2 — 触発場面 (Future Trigger)

### 使用場面

1. 大規模reviewで複数の独立した証拠源を調査する。
2. frontend障害を再現・追跡・修正へ段階分解する。
3. 複数packageや仕様を並列にreadして比較する。
4. 役割ごとにMCP toolやsandboxを変えたい。

### 言語信号

- 「subagentに分けて調査して」
- 「並列に読むが編集競合は避けたい」
- 「reviewer / explorer / docs researcherを分ける」
- “bounded parallel agents” / “read-heavy delegation”

### 隣接skillとの区別

- `codex-execution-mode-routing` のcloud委譲はtask全体の実行面。本skillは一つのtask内部の役割分解。
- `codex-context-entry-routing` は必要情報の入口を選ぶ。本skillは入口ごとに担当agentを限定する場合に組み合わせる。
- `codex-mcp-control-plane` は担当へ付与するMCP server/toolを制限する。

## E — 実行手順 (Execution)

1. **成果を独立問いへ分解する** — 各役割が他agentの未完了writeに依存せず回答できれば完了。
2. **役割境界を記述する** — input、scope、禁止操作、return format、done criteriaが各agentにあれば完了。
3. **authorityを最小化する** — read-heavy役はread-only、必要MCP/toolだけとなれば完了。共有file編集が必要なら並列化を停止する。
4. **親が統合する** — 出典付き要約を比較し、矛盾・未確認事項・次の一つのwriter actionを決めれば完了。

## B — 境界 (Boundary)

### 使用しない場面

- 一人で短時間に完了する小さな作業。
- 複数agentが同じfile・同じstateを同時に変更する仕事。
- 途中approvalが不可避な非対話subagent。

### 公式資料が警告する失敗

- write-heavyな並列編集はcollisionと整合性低下を生む。
- live taskを同じworking directoryで動かすならworktree等の隔離が必要。
- 必要以上のtool・model・sandboxを全役割へ一律付与しない。

### 資料の限界

- 公式例は設計patternを示すが、最適agent数やtoken費用の定量基準は示さない。

## 関連skills

- contrasts-with: `codex-execution-mode-routing` — 内部分解と実行面委譲を区別する。
- composes-with: `codex-context-entry-routing` — context種別を担当へ割り当てる。
- composes-with: `codex-mcp-control-plane` — role専用MCPを最小化する。

## 監査情報

- **検証通過**: V1 ✓ / V2 ✓ / V3 ✓
- **原典case**: c05, c06
- **テスト通過率**: 100% (6/6)
- **蒸留日**: 2026-08-17
