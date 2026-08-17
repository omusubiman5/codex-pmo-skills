---
name: codex-sandbox-approval-boundary
description: |
  Codex runのfilesystem・command・network能力と、人の承認が必要な昇格を設計するときに使う。「read-only / workspace-write」「approval policy」「sandboxを緩めたい」「danger-full-access」が信号。外向き通信先の個別統制、CI job間のsecret分離、認証方式だけには使わない。
source_book: Codex CLI official documentation — OpenAI
source_chapter: Agent approvals & security / Non-interactive mode
tags: [sandbox, approvals, least-privilege, codex]
related_skills:
  - slug: codex-egress-surface-governance
    relation: composes-with
  - slug: codex-ci-patch-handoff
    relation: composes-with
---

# sandboxとapprovalの二層境界設計

## R — 原文 (Reading)

> “Sandbox modes define the technical boundary: what Codex can read or write, and whether it can access the network.” “Approval policies define when Codex must pause and ask before it can run a command.”
>
> — OpenAI, Agent approvals & security

## I — 方法論骨架 (Interpretation)

安全設定を一つの「強い・弱い」尺度で考えない。
sandboxは実行主体が技術的に何をできるかを決める。
approval policyは境界を越える操作をいつ人へ止めるかを決める。
まずread-onlyなど安全側から始め、仕事に必要な能力だけをworkspace-write等へ広げる。
無人実行では途中承認に依存できないため、事前に許す能力をさらに狭くする。
host側でsandboxを提供できないなら、Dev ContainerやVMを外側の隔離境界として使う。

## A1 — 公式資料中の適用

### ケース1: Linux sandboxを提供できないhostでの隔離
- **問題**: host platformがCodexのLinux sandboxを直接提供できない。
- **方法論の使用**: repositoryをDev Container内へ置き、外側のcontainer/VMをfilesystem・process境界にする。
- **結論**: `danger-full-access` を非隔離hostで使うのではなく、信頼境界を一段外へ移す。
- **結果**: 公式資料はsecure Dev Container構成を提示する。特定脅威への実証値は示さない。

## A2 — 触発場面 (Future Trigger)

### 使用場面

1. read-only、workspace-write、full accessのどれを選ぶか判断する。
2. commandごとに人のapprovalを残すか、無人実行へ切り替える。
3. 特定directoryだけへ書込みを許したい。
4. host sandboxが不足しcontainer/VM隔離を検討する。

### 言語信号

- 「sandboxとapprovalの違いは？」
- 「workspace-writeまで許可したい」
- 「このcommandだけ承認なしで動かしたい」
- “danger-full-access” / “approval policy”

### 隣接skillとの区別

- `codex-egress-surface-governance` は許可後の通信経路と宛先を分けて統制する。本skillは基礎能力と昇格同意を決める。
- `codex-ci-patch-handoff` は複数job間のauthority分離を扱う。

## E — 実行手順 (Execution)

1. **必要能力を動詞で列挙する** — read、write、execute、networkを対象path/範囲付きで書ければ完了。
2. **最小sandboxを選ぶ** — 列挙能力を満たす最小modeと外側隔離を指定できれば完了。
3. **昇格点を決める** — sandbox外操作ごとにask/deny/pre-approvedを割り当てられれば完了。
4. **無人条件を検査する** — 途中approvalが発生する経路を除去または事前拒否し、失敗時停止が定義されれば完了。

## B — 境界 (Boundary)

### 使用しない場面

- 許可済みnetworkのdomain制約だけを設計する場合。
- 認証cacheの保存方式だけを選ぶ場合。
- 非隔離hostでapprovalを無効にし、sandbox bypassを安全策と呼ぶ場合。

### 公式資料が警告する失敗

- sandboxとapprovalを外してよいのは外側で隔離された環境に限る。
- hostile repositoryをfull-access Dev Containerで開くと、container内の秘密やmountが危険になる。
- named deleteのような破壊操作は対象を明示し、広いpathやglobを避ける。

### 資料の限界

- OS・container runtimeごとの完全なthreat modelや組織policyは利用者側で補う必要がある。

## 関連skills

- composes-with: `codex-egress-surface-governance` — network能力を許す場合に経路別controlを加える。
- composes-with: `codex-ci-patch-handoff` — job内境界とjob間境界を重ねる。

## 監査情報

- **検証通過**: V1 ✓ / V2 ✓ / V3 ✓
- **原典case**: c09
- **テスト通過率**: 100% (6/6)
- **蒸留日**: 2026-08-17
