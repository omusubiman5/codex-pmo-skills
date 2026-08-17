---
name: codex-auth-boundary-selection
description: |
  CodexのChatGPT sign-in、API key、device code、localhost callback、auth.json移送を、interactive端末・headless host・CIへ割り当てるときに使う。「headless login」「CODEX_API_KEY」「auth.jsonをコピー」「CI credential」が信号。repository権限分離全体、MCP OAuth、通常のaccount問い合わせだけには使わない。
source_book: Codex CLI official documentation — OpenAI
source_chapter: Authentication / Non-interactive mode
tags: [authentication, api-key, device-code, secrets]
related_skills:
  - slug: codex-ci-patch-handoff
    relation: composes-with
  - slug: codex-sandbox-approval-boundary
    relation: composes-with
---

# 認証方式を利用面と統制境界へ対応させる

## R — 原文 (Reading)

> “Codex CLI supports signing in with ChatGPT or with an API key.” “For headless environments, use device code authentication or complete the localhost login flow on another machine.”
>
> — OpenAI, Authentication

## I — 方法論骨架 (Interpretation)

認証方式を利便性だけで統一しない。
人が対話する端末、GUIのないhost、短命なCI processでは適切なcredential境界が異なる。
対話端末はChatGPT sign-in、headless対話環境はdevice codeまたは別machineでのcallback、automationはprocess-scoped API keyを候補にする。
保存済み認証cacheはpasswordと同じ秘密として扱い、public repositoryや不用意な同期先へ置かない。
共有する場合も、認証fileを配ることと各利用者が認証することのrisk差を明示する。

## A1 — 公式資料中の適用

### ケース1: headless hostでdevice authentication
- **問題**: remote/headless環境でbrowser callbackを直接完了できない。
- **方法論の使用**: device code flow、または別machineでlocalhost login flowを完了する方法を選ぶ。
- **結論**: interactive browserの有無に認証flowを対応させる。
- **結果**: 公式資料はheadless向け手順と選択肢を示す。組織環境での成功率は示さない。

## A2 — 触発場面 (Future Trigger)

### 使用場面

1. GUIのないserverへCodex CLIをloginさせる。
2. CIでAPI keyを一回のexec processだけへ渡す。
3. ChatGPT sign-inとAPI keyのどちらを使うか選ぶ。
4. `auth.json` の移送・保存・共有riskを評価する。

### 言語信号

- 「headlessでCodex loginしたい」
- 「device code authenticationを使う？」
- 「CODEX_API_KEYをCIへ渡す」
- 「auth.jsonをコピーしてもよい？」

### 隣接skillとの区別

- `codex-ci-patch-handoff` はcredentialとwrite authorityをjobで分離する。本skillはcredentialの方式・scope・保存を選ぶ。
- `codex-sandbox-approval-boundary` は認証後にagentが持つ実行能力を決める。

## E — 実行手順 (Execution)

1. **利用面を分類する** — interactive workstation、headless interactive、non-interactive automationのいずれかを確定できれば完了。
2. **credential方式を選ぶ** — ChatGPT、API key、device code、callbackの選択理由を一文で残せれば完了。
3. **scopeと保存を決める** — process lifetime、保存path、読取主体、rotation/revoke方法が埋まれば完了。
4. **露出経路を検査する** — repository、log、artifact、child process、shared homeへの漏出がdenyまたは明示受容されれば完了。

## B — 境界 (Boundary)

### 使用しない場面

- MCP server固有のOAuth設定だけを扱う場合。
- 認証方式を決めずにauth cacheを複製する場合。
- public repositoryへ認証fileを置く場合。

### 公式資料が警告する失敗

- `auth.json` はpassword同等の秘密として扱う。
- job-level API keyはrepository-controlled codeから読まれ得る。
- API keyをshell history、log、artifactへ残さない。

### 資料の限界

- 組織SSO、secret manager製品、rotation周期の具体policyは利用環境側で決める必要がある。

## 関連skills

- composes-with: `codex-ci-patch-handoff` — CI credentialをread-only生成jobへ限定する。
- composes-with: `codex-sandbox-approval-boundary` — credential保有processの能力も最小化する。

## 監査情報

- **検証通過**: V1 ✓ / V2 ✓ / V3 ✓
- **原典case**: c12
- **テスト通過率**: 100% (6/6)
- **蒸留日**: 2026-08-17
