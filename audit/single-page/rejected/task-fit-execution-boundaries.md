# 不採用候補: タスク適合型の実行境界設計

```yaml
id: f01
title: タスク適合型の実行境界設計
merged_from: [f01, p02, p09]
V1_cross_domain:
  passed: true
  reason: "一般的なtask-fitの説明と、runごとのpermissions・sandbox確認という別の文脈がある。"
V2_predictive_power:
  passed: true
  novel_question: "未知の大規模移行と既知の小さな文言修正で同じ設定を使うべきか。"
  derived_answer: "前者は必要な推論能力を上げつつ操作境界を精査し、後者は狭い権限と低い作業量へ抑える。"
V3_exclusivity:
  passed: false
  reason: "能力・権限・コマンドをタスクに合わせるという内容自体は一般的なリスクベース運用であり、独立skillにするほど反直感的ではない。"
disposition: 用語・境界設計の補助材料として保持
```
