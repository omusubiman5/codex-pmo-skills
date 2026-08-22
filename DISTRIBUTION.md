# Codex PMO Skills 0.1.0

Codexをプロジェクトへ導入し、初期運用を安全に開始するためのPMO skill集です。

## 対象範囲

- プロジェクト発足
- 実行方式の選定
- sandbox・approval・認証・外部通信の設計
- MCPとsubagentの統制
- CI接続と機械可読な成果物の設計
- 初期運用の検証
- 横断task分解、event follow-up、重複制御、release lane、evidence gate

別系列の `codex-pmo-orchestration` は横断PMO運用だけを扱い、個別製品の実装や、source adapter未接続時のbackground automationは行いません。

課題一覧の実作業、個別bug修正、障害復旧、日常保守は対象外です。

## 内容

- Official-source RIA++ skills: 9
- Separate operational PMO skills: 1
- Total installable skill directories: 10
- Source: OpenAI Codex CLI公式資料15件（9 official-source skills）
- RIA++: 原文、解釈、公式事例、trigger、実行手順、境界
- Tests: 54 official routing prompts + 7 PMO forward-test prompts = 61
- Independent results: official 54/54; PMO 7/7; cross-skill bait 18/18
- Cross-skill bait test: 18/18

## 初めて使う場合

最初に [README.md](./README.md) を読んでください。専門用語を知らない読者向けに、
各skillの役割、依存と統合の違い、試験内容を説明しています。

## Codexへユーザー単位でインストールする

ZIPを展開し、10の `codex-*` skill directoryをCodexのユーザーskill directoryへコピーします。

Windows PowerShellの例:

```powershell
$source = "展開したdirectoryの絶対path"
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
  Copy-Item -LiteralPath (Join-Path $source $name) -Destination $target -Recurse
}
```

既に同名directoryがある場合、この例は上書きせずerrorになります。既存版を確認してから更新してください。

## 完全性を確認する

同梱の `CHECKSUMS.sha256` と展開後fileのSHA-256を比較できます。

```powershell
Get-FileHash -Algorithm SHA256 ".\codex-execution-mode-routing\SKILL.md"
```

## Licenseと出典

- Library: `kangarooking/cangjie-skill`, base commit `149cb39f559cafcb82910f8662b3f4e3b9ee5574`
- Library license: GNU Affero General Public License v3.0
- Source documentation: OpenAI公式資料。固定URLと取得hashは `SOURCE_MANIFEST.md` に記録。
- 公式資料の引用と、蒸留側の解釈・将来例を区別しています。

## 重要な注意

このskill集はsecurityを自動保証しません。組織policy、法令、secret管理、接続先MCPの安全性は別途確認してください。
