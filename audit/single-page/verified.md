# 三重検証通過候補

## 検証集計

- 方法論候補（重複統合後）: 8件
- 通過: 1件
- 不通過: 7件
- 補助候補: 用語10件、事例0件、反例1件

```yaml
- id: f04
  title: 実行形態の用途別選択
  type: framework
  merged_from: [f04, p03]
  V1_cross_domain:
    passed: true
    evidence:
      - "Why use Codex CLI: 対話利用と `codex exec` による反復workflow・pipelineを対比"
      - "Build a terminal workflow around Codex: 対話の継続、非対話実行、cloud委譲を別々の入口として提示"
      - "Use Codex CLI when…: terminal作業、scripting/CI、cloud委譲を用途別に再整理"
  V2_predictive_power:
    passed: true
    novel_question: "探索的な大規模リファクタ、毎晩の定型検査、数時間かかる独立調査を、それぞれどの実行形態へ置くべきか。"
    derived_answer: |
      人が途中で誘導する探索的リファクタは対話型CLI、入力と判定が固定された毎晩の検査は
      `codex exec`、ローカルで待ち続ける必要のない独立調査はCodex cloudへ置く。
  V3_exclusivity:
    passed: true
    why_not_common: |
      単なる「用途に合うツールを選ぶ」ではなく、Codex固有の三つの実行面を
      対話性・反復性・委譲性で対応付ける製品固有の選択規則になっている。
  disposition: 段階2へ進める
```
