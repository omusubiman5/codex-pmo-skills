# 不採用候補: 複雑作業の分割・再統合

```yaml
id: f06
title: 複雑作業の分割・再統合
merged_from: [f06]
V1_cross_domain:
  passed: false
  reason: "subagentsの説明は機能一覧の一箇所だけで、別の対象・章による裏付けがない。"
V2_predictive_power:
  passed: true
  novel_question: "複数packageにまたがるmigration調査をどう分けるか。"
  derived_answer: "packageや懸念ごとに焦点を限定して委譲し、主sessionで依存関係と結論を再統合する。"
V3_exclusivity:
  passed: false
  reason: "大きな問題を分割し、専門担当の結果を統合する方法は一般的な分業原則である。"
disposition: 機能例として保持
```
