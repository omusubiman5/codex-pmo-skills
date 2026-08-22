---
name: codex-pmo-orchestration
description: |
  複数プロジェクトを横断するPMOとして、実行・監査・ユーザー確認を小さなタスクへ分け、止まった担当を次の行動へ変換し、リリースを管理改善で止めないときに使う。PM看板、Beads、担当Codex、監査Codexの運用が対象。個別製品の実装そのものには使わない。
---

# PMOの並列実行とリリース運用

## 目的

PMOは実装者の代わりではない。優先順位、依存、完了ゲート、担当と監査の起動、進捗の可視化を担い、実装・テスト・Git操作は対象プロジェクトの担当Codexへ渡す。

## 作業の単位

- 実行issueは、AIが10分以内に実装・検証・証拠・報告まで終えられる一成果物に限定する。10分を超える見込みのものはdispatchせず、epic・複数task・外部gateへ分割する。
- 大きな目的はepicにし、複数成果物・複数外部依存を一つの実行issueにしない。
- 新規issueの前に、`project + normalized objective + deliverable + source reference` の同一性を確認する。完全一致は既存issueへ追記し、類似候補はPM判断まで新IDを発行しない。
- 依存がない作業は、担当と監査を分けて並行にする。同じファイルを同時に編集する作業は一人のwriterへ戻す。

## 進行中タスクの扱い

担当のidle/completed、質問、監査PASS/FAIL、外部前提の成立、または`in_progress`なのに次actionがない状態をイベントとして扱う。各eventは`source task + event type + source revision/event ID`を処理keyとして記録し、再送は既存actionの参照またはno-opにする。二重dispatch、Inbox重複、二重closeを作らない。

同じreview cycle内で必ず次のいずれか一つへ変換する。

1. 依存しない次の10分taskをdispatchする。
2. ユーザーに必要な一手を一件だけInboxへ出す。
3. 証拠を確認して完了へ閉じる。

自動source adapterが未接続なら、background監視・自動wake・自動dispatchは存在しない。PMがeventを受信または確認したreview cycleだけ処理する。この制約を明示し、模擬テストの合格を実際の自動拾い上げと混同しない。

## リリース直行レーン

- 実装、自動テスト、監査準備は並行で進める。最終の独立監査は、固定したrelease candidateだけを対象にする。
- リリースを止められるのは、必要な自動試験の失敗、独立監査FAIL、実機、外部認証、安全性、公開承認などの実在するゲートだけ。
- Beads移行、PM改善、可視化、Petなどの改善作業は、リリース候補と別レーンに置く。
- ユーザーが特定project/iterationのBeads延期を承認した場合、既存recordsを残したまま例外を明示し、実装と監査を止めない。

## 状態と証拠

- dispatch前に、taskごとのrequired evidence、evidence location/ref、判定者を固定する。完了は担当報告だけでは決めない。必要な自動試験、実機、本番、独立監査の証拠が揃った時だけ完了にする。PMは証拠を照合し、実装・試験・Git操作を代行しない。
- 看板の上部件数と下部カードは、同じフィルタ済みtask集合から算出する。
- PM Inboxは第二台帳にしない。元taskを参照する通知として扱う。
- 告知文や決定は会話だけに残さず、PMプロジェクト内のMarkdownへ保存する。

## 境界

- PMOが対象プロジェクトの実装、試験、Git操作を抱え込まない。
- 進行可能な作業を「設計待ち」「確認待ち」と呼んで停止しない。
- 未確認の進捗、模擬テスト、配置だけをリリース済み・適用済みとして扱わない。
