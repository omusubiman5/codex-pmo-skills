# 不採用候補: 回復可能な初回タスク導入

```yaml
id: f02
title: 回復可能な初回タスク導入
merged_from: [f02, p04, p05, ce01]
V1_cross_domain:
  passed: false
  reason: "焦点を絞った依頼とGitチェックポイントはいずれもGetting startedの同じ導入文脈にあり、別章・別対象の独立した裏付けがない。"
V2_predictive_power:
  passed: true
  novel_question: "初めて触るlegacy repositoryで最初に何を任せるべきか。"
  derived_answer: "作業前のcheckpointを確保し、まず説明または限定的変更を依頼し、作業後に差分を固定する。"
V3_exclusivity:
  passed: false
  reason: "小さく始めてGitで戻せるようにするのは、エージェント固有ではない一般的な開発慣行である。"
disposition: onboarding例とBoundary材料として保持
```
