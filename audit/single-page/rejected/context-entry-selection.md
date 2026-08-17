# 不採用候補: 必要文脈に応じた入口選択

```yaml
id: f05
title: 必要文脈に応じた入口選択
merged_from: [f05]
V1_cross_domain:
  passed: false
  reason: "resume、image、searchは同じ機能一覧に一度ずつ現れるだけで、各対応関係を裏付ける独立文脈がない。"
V2_predictive_power:
  passed: true
  novel_question: "過去の修正を続けつつ、画面エラーと最新dependency情報を同時に調べるには何を足すか。"
  derived_answer: "resumeで履歴を戻し、imageで画面情報を渡し、searchで現行情報を補う。"
V3_exclusivity:
  passed: true
  reason: "欠落文脈の型を `codex resume`、`--image`、`--search` へ対応付ける点はCodex CLI固有である。"
disposition: V1不足。リンク先詳細をコーパスへ追加する場合の再検証候補
```
