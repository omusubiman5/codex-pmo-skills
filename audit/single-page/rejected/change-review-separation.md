# 不採用候補: 変更とレビューの職務分離

```yaml
id: f08
title: 変更とレビューの職務分離
merged_from: [f08, p08]
V1_cross_domain:
  passed: false
  reason: "レビュー紹介とUse whenの記述は同じ対象・同じ結論の反復であり、別対象に適用された独立証拠ではない。"
V2_predictive_power:
  passed: true
  novel_question: "実装担当の変更を検査するとき、レビュー中に自動修正も行うべきか。"
  derived_answer: "専用reviewとして対象差分を指定し、まず作業ツリーを変更せず優先順位付き指摘を得る。"
V3_exclusivity:
  passed: false
  reason: "変更担当とreviewを分離し、commit前にriskを確認する考え方は一般的な開発慣行である。"
disposition: reviewの補助原則として保持
```
