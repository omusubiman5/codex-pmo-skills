# 段階1.5 — 重複統合監査

以下は棄却ではなく、同じ方法論を別skillへ水増ししないため通過候補へ統合したもの。

```yaml
- id: f10
  title: command networkの許可・制約二段階モデル
  merged_into: f11
  reason: "network permissionとproxy policyは、f11が扱う複数通信surfaceのうちcommand network面の具体化である。独立skillにすると境界と判定が重なる。"

- id: f12
  title: currentnessとprompt-injectionリスクによる検索モード選択
  merged_into: f11
  reason: "cached/live searchの選択とuntrusted-result規則は、f11のsearch surfaceに固有な下位判断である。"

- id: f14
  title: 読み書き比率による並列化判定
  merged_into: f13
  reason: "read-heavy taskを並列化しwrite conflictを避ける規則は、bounded subagent分解の境界条件である。"

- id: f15
  title: subagent役割と計算資源の適合設計
  merged_into: f13
  reason: "role別instructions・model・sandbox・toolsは、bounded subagentを実装する構成要素である。"

- id: f23
  title: 安全側から必要分だけ権限を拡張する段階設計
  merged_into: f09
  reason: "最小状態からの段階拡張は、sandbox能力とapproval同意を二層で設計するf09の運用規則である。"
```

