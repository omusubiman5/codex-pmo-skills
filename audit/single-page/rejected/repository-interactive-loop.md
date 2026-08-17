# 不採用候補: リポジトリ中心の対話型開発ループ

```yaml
id: f03
title: リポジトリ中心の対話型開発ループ
merged_from: [f03, p01, p06]
V1_cross_domain:
  passed: true
  reason: "Why use、See what Codex CLI can do、Use Codex CLI whenの別セクションで、repository内の調査・編集・実行が反復される。"
V2_predictive_power:
  passed: true
  novel_question: "原因不明のflaky testを調べるとき、会話を分断すべきか。"
  derived_answer: "同じrepositoryとsessionで調査、コマンド実行、差分確認、追加指示を反復し、途中で方向修正する。"
V3_exclusivity:
  passed: false
  reason: "調査・計画・編集・実行を同じ開発ループで回し、人が差分を確認する方法は一般的なagentic codingの運用である。"
disposition: 実行形態選択skillの対話型モード例として保持
```
