---
name: codex-egress-surface-governance
description: |
  Codexのweb search、sandboxed command network、MCP、direct HTTPを区別して外向き通信を監査・制限するときに使う。「domain allowlist」「cached vs live search」「proxy policy」「MCPも外へ出る？」が信号。filesystem権限だけ、認証方式だけ、単なるWeb検索依頼には使わない。
source_book: Codex CLI official documentation — OpenAI
source_chapter: Agent approvals & security / Web search / MCP
tags: [network, web-search, proxy, mcp, security]
related_skills:
  - slug: codex-sandbox-approval-boundary
    relation: depends-on
  - slug: codex-mcp-control-plane
    relation: composes-with
  - slug: codex-context-entry-routing
    relation: composes-with
---

# 複数通信経路を個別統制する脅威モデル

## R — 原文 (Reading)

> “Web search, MCP servers, and direct HTTP requests are separate network paths.” “When you enable network access for sandboxed commands, the proxy policy and network permission work together.”
>
> — OpenAI, Agent approvals & security

## I — 方法論骨架 (Interpretation)

「Codexのnetwork」を一個のswitchとして扱わない。
web search、sandbox内command、MCP server、direct HTTPは別々の通信surfaceである。
searchではcachedとliveを情報鮮度・prompt injection riskで選ぶ。
command networkではpermissionが通信能力を開き、proxy policyが宛先を狭める。
MCPはserver接続とtool callを別controlで縛る。
一経路のallowlistを他経路にも効くと推測せず、各surfaceの有効化、宛先、承認、記録を個別に確認する。

## A1 — 公式資料中の適用

### ケース1: command networkを許可しproxyで宛先制限
- **問題**: package取得などのcommand通信は必要だが、任意Internet accessは許せない。
- **方法論の使用**: sandboxed commandのnetwork permissionを有効にし、別のproxy policyで許可domainを限定する。
- **結論**: 能力の有効化と宛先policyを二段階で構成する。
- **結果**: 公式資料はpermissionとproxy policyを併用する設定例を示す。敵対的DNSを完全防御するとの主張はない。

## A2 — 触発場面 (Future Trigger)

### 使用場面

1. live web searchの必要性とprompt injection riskを比較する。
2. sandboxed commandへ限定networkを与える。
3. search domain filterがMCPやHTTPにも効くか監査する。
4. allowlist、proxy、approval、telemetryをsurface別に設計する。

### 言語信号

- 「このdomainだけnetwork許可したい」
- 「cached searchとlive searchのどちら？」
- 「MCP経由の通信も止まる？」
- “network proxy policy” / “egress surface”

### 隣接skillとの区別

- `codex-sandbox-approval-boundary` はnetwork能力そのものと昇格を扱う。本skillは通信surfaceと宛先の分解を扱う。
- `codex-mcp-control-plane` は一つのMCP server内の必須性、tool可視性、approvalを扱う。
- `codex-context-entry-routing` は情報をどの入口から得るかを選び、本skillは選択後の外向きriskを統制する。

## E — 実行手順 (Execution)

1. **surface inventoryを作る** — search、command、MCP、direct HTTP、telemetryの使用有無を埋めれば完了。
2. **各surfaceの必要性を判定する** — currentness・接続先・処理目的がないsurfaceをdisabledにできれば完了。
3. **controlを個別配置する** — mode、permission、domain/proxy、tool filter、approval、loggingを対応表にできれば完了。
4. **迂回路を検査する** — 一surfaceのdenyを別surfaceで回避できる経路を列挙し、同等controlまたは明示的受容があれば完了。

## B — 境界 (Boundary)

### 使用しない場面

- offline repositoryだけをreadする作業。
- search結果を権威あるsourceとして無検証採用する場合。
- domain ruleだけ設定し、network permissionも有効になったと推測する場合。

### 公式資料が警告する失敗

- web resultはuntrusted inputでありprompt injectionを含み得る。
- search domain filterはすべてのtrafficを制限しない。
- proxy policyだけではcommand network能力を有効にしない。
- DNS確認は悪意あるDNSや全迂回を完全には防がない。
- command proxyはMCPやdirect HTTPをfilterしない。

### 資料の限界

- 組織networkの完全なegress architectureや外部serverの信頼性評価は資料の範囲外である。

## 関連skills

- depends-on: `codex-sandbox-approval-boundary` — command network能力の基礎境界を先に決める。
- composes-with: `codex-mcp-control-plane` — MCP surfaceをserver/tool単位へ掘り下げる。
- composes-with: `codex-context-entry-routing` — context取得方法とそのrisk controlを接続する。

## 監査情報

- **検証通過**: V1 ✓ / V2 ✓ / V3 ✓
- **原典case**: c08
- **テスト通過率**: 100% (6/6)
- **蒸留日**: 2026-08-17
