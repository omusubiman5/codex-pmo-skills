# 不採用候補: 反復手順と外部能力の分離

```yaml
id: f07
title: 反復手順と外部能力の分離
merged_from: [f07, p07]
V1_cross_domain:
  passed: false
  reason: "frameworkとprincipleは同じ一文を根拠にしており、独立した複数文脈ではない。"
V2_predictive_power:
  passed: true
  novel_question: "毎週同じrelease手順を実行し、team toolの状態も読む必要がある場合、何を用意するか。"
  derived_answer: "反復手順をskillへまとめ、外部tool・data接続をpluginで追加する。"
V3_exclusivity:
  passed: true
  reason: "Codex上でinstructionsとconnected toolsをskills/pluginsへ分離する点は製品固有である。"
disposition: V1不足。リンク先詳細をコーパスへ追加する場合の再検証候補
```
