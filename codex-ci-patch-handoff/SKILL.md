---
name: codex-ci-patch-handoff
description: |
  CIでCodexに修正を生成させる一方、API key、repository write、署名・PR作成を同じjobへ置きたくないときに使う。「read-only job」「patch artifact」「別jobでpush」「secretをtestから隔離」が信号。通常のlocal修正、構造化JSON出力だけ、CI以外の一般論には使わない。
source_book: Codex CLI official documentation — OpenAI
source_chapter: Non-interactive mode — Autofix CI failures in GitHub Actions
tags: [codex, ci, least-privilege, patch]
related_skills:
  - slug: codex-sandbox-approval-boundary
    relation: depends-on
  - slug: codex-exec-io-contract
    relation: composes-with
  - slug: codex-auth-boundary-selection
    relation: composes-with
---

# CI修正の権限分離とpatch受け渡し

## R — 原文 (Reading)

> “The Codex job below has only `contents: read`.” “In a separate job, apply the patch and open a pull request.”
>
> — OpenAI, Non-interactive mode — Autofix CI failures in GitHub Actions

## I — 方法論骨架 (Interpretation)

推論するjobとrepositoryを変更するjobを同じ信頼境界に置かない。
Codex側はread-only checkoutで失敗を再現し、最小修正と再testを行う。
変更は実行可能commandでなくbinary patch artifactとして境界を越える。
別jobがpatchを検査・適用し、branch、署名、push、PR作成を担当する。
これにより推論credential、repository-controlled code、write tokenが同時に存在する場所をなくす。

## A1 — 公式資料中の適用

### ケース1: GitHub ActionsでCI failureをauto-fix
- **問題**: CodexへCI修正を依頼したいが、API keyとrepository write権限を同じjobへ与えたくない。
- **方法論の使用**: `contents: read` のCodex jobで再現・最小修正・retestを行い、差分をbinary patch artifactへ保存する。別jobだけが適用・push・PR作成する。
- **結論**: credentialとwrite authorityをjobで分け、patchだけを受け渡す。
- **結果**: 差分がある場合にartifactを作り、後続jobが `codex/auto-fix-$RUN_ID` branchとPRを作るworkflowが示される。特定repositoryでの成功実測はない。

## A2 — 触発場面 (Future Trigger)

### 使用場面

1. CI failureを自動修正しPR化したい。
2. repository内scriptを実行するjobへwrite tokenを渡せない。
3. AI credentialと署名鍵・deploy keyを分離したい。
4. 生成差分を別のtrust domainで検査してから適用したい。

### 言語信号

- 「Codex jobはread-onlyにしたい」
- 「patch artifactを別jobへ渡す」
- 「API keyとpush権限を分離して」
- “autofix CI without write permission”

### 隣接skillとの区別

- `codex-sandbox-approval-boundary` は一つのrun内の能力と同意を設計する。本skillはCI job間のcredential・write authorityを分離する。
- `codex-exec-io-contract` は一般出力契約。本skillの中心はpatchをtrust boundaryにすること。
- `codex-auth-boundary-selection` はcredential方式と保存場所を選ぶ。本skillは選んだcredentialをjobへ配置する構造を決める。

## E — 実行手順 (Execution)

1. **authority inventoryを作る** — read、execute、AI credential、write、sign、PR createの保有jobを表にできれば完了。
2. **生成jobを縮小する** — repository readと必要な短命credentialだけになり、write tokenがなければ完了。
3. **patch境界を作る** — binary-safe patch、hash、元commitをartifact化し、任意commandを渡していなければ完了。
4. **適用jobで検証する** — 元commit照合、patch適用、test、差分確認後だけbranch/PRを作れば完了。差分なしなら停止する。

## B — 境界 (Boundary)

### 使用しない場面

- 人がlocal repositoryで対話的に修正するだけの場合。
- patchを検査せず自動deployまで直結させる場合。
- repository-controlled setup/testへ長期secretを無制限に露出する構成。

### 公式資料が警告する失敗

- job-level API keyは、そのjob内で動くrepository codeから読める可能性がある。
- Codex jobへwrite permissionまで与えると侵害時の影響範囲が拡大する。

### 資料の限界

- 公式例はGitHub Actions構成を示すが、組織固有のbranch protection、署名、artifact retentionまでは決めない。

## 関連skills

- depends-on: `codex-sandbox-approval-boundary` — 生成job内でも最小能力を設定する。
- composes-with: `codex-exec-io-contract` — statusとartifactのmachine contractを決める。
- composes-with: `codex-auth-boundary-selection` — process-scoped credentialを選ぶ。

## 監査情報

- **検証通過**: V1 ✓ / V2 ✓ / V3 ✓
- **原典case**: c02
- **テスト通過率**: 100% (6/6)
- **蒸留日**: 2026-08-17
