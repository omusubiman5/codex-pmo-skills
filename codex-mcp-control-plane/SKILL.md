---
name: codex-mcp-control-plane
description: |
  CodexへMCP serverを接続し、必須性、enabled/disabled tools、tool approvalを別々に設定するときに使う。「MCPが落ちたら失敗させる」「read toolだけ見せる」「toolごとに承認」「required server」が信号。接続先を選ぶだけ、一般network allowlist、MCPを使わないlocal作業には使わない。
source_book: Codex CLI official documentation — OpenAI
source_chapter: MCP / Non-interactive mode / Subagents
tags: [mcp, tools, approvals, fail-closed]
related_skills:
  - slug: codex-egress-surface-governance
    relation: depends-on
  - slug: codex-context-entry-routing
    relation: composes-with
  - slug: codex-bounded-subagents
    relation: composes-with
---

# MCP接続の必須性・tool範囲・承認の三段階制御

## R — 原文 (Reading)

> “Use `enabled_tools` or `disabled_tools` to control which tools Codex can use.” “Mark an MCP server as required when the task must fail if the server cannot initialize.”
>
> — OpenAI, MCP / Non-interactive mode

## I — 方法論骨架 (Interpretation)

MCP接続を単純なon/offとして扱わない。
第一に、そのserverなしでtaskを続けてよいかをrequiredで決める。
第二に、接続できてもagentへ見せるtoolを必要最小限にfilterする。
第三に、見えているtoolを呼ぶ際のapprovalを操作riskに応じて決める。
subagentへ付与する場合はroleごとにserverとread/write toolをさらに狭める。
必須文脈が取得できないときは推測で続行せずfail closedにする。

## A1 — 公式資料中の適用

### ケース1: PR reviewのdocs researcherへ専用MCPを限定付与
- **問題**: API correctnessを公式docsで照合したいが、reviewer全員へ外部toolやwrite能力は不要である。
- **方法論の使用**: docs researcher roleへ専用MCP serverとread-only sandboxを割り当て、調査結果だけを親へ返す。
- **結論**: roleに必要なcontext toolだけを公開する。
- **結果**: 公式資料はhistory・risk・docs調査の分担構成を示す。tool制限による定量的risk低減値はない。

## A2 — 触発場面 (Future Trigger)

### 使用場面

1. 必須MCPが起動しない場合にexecを停止したい。
2. server内のread toolだけをCodexへ見せたい。
3. update/delete toolだけapproval必須にしたい。
4. subagent roleごとに異なるMCPを割り当てたい。

### 言語信号

- 「このMCPなしならfailさせて」
- 「enabled_tools / disabled_toolsを絞る」
- 「tool approvalを個別設定したい」
- “required MCP server” / “fail closed”

### 隣接skillとの区別

- `codex-egress-surface-governance` はMCPを含む全network surfaceを監査する。本skillはMCP内部の三段階controlを具体化する。
- `codex-context-entry-routing` はMCPを入口として選ぶまで。
- `codex-bounded-subagents` は制限済みMCPをどの役割へ付与するかを決める。

## E — 実行手順 (Execution)

1. **依存性を判定する** — serverなしでも正しい成果が出せるかをyes/noで決め、noならrequiredにすれば完了。
2. **tool surfaceを最小化する** — taskで使うtool名だけをallowlist化し、read/write区分を記録できれば完了。
3. **approvalを割り当てる** — toolごとにautomatic、ask、denyをrisk理由付きで決めれば完了。
4. **failure pathを試す** — init failure、timeout、denied tool、approval unavailableで推測続行せず期待どおり停止・縮退すれば完了。

## B — 境界 (Boundary)

### 使用しない場面

- MCPなしでlocal fileだけを処理する場合。
- 便利そうという理由だけで全server・全toolを接続する場合。
- 必須server failureを黙って無視し、不完全なcontextで正常終了する場合。

### 公式資料が警告する失敗

- workflowを定めず多数のtoolを一度に接続しない。
- global wildcardを狭いapproval policyの代用にしない。
- required MCPの初期化失敗やtimeoutはexec failureとして扱う。

### 資料の限界

- 各third-party MCP serverの実装安全性やdata retentionは個別監査が必要である。

## 関連skills

- depends-on: `codex-egress-surface-governance` — MCPを独立network surfaceとして先に認識する。
- composes-with: `codex-context-entry-routing` — MCPが適切なcontext入口の場合にcontrolを加える。
- composes-with: `codex-bounded-subagents` — role別にserver/toolを限定する。

## 監査情報

- **検証通過**: V1 ✓ / V2 ✓ / V3 ✓
- **原典case**: c05
- **テスト通過率**: 100% (6/6)
- **蒸留日**: 2026-08-17
