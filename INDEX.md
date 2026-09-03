# Skill Library INDEX

## Codex CLI Official Documentation

# Codex CLI Official Documentation — Skill Index

> cangjie-skillで OpenAI 公式資料15件を蒸留し、**9 skills**を構築した。
> 処理日: 2026-08-17

初めて読む場合は、専門知識を前提にしない [README.md](./README.md) から始めてください。

## この資料群について

- **著者**: OpenAI
- **公開年**: 継続更新資料（固定取得日 2026-08-17）
- **一言主旨**: Codex CLIを、文脈・実行面・権限・出力・検証の明示契約として運用する。
- **全体理解**: [BOOK_OVERVIEW.md](./BOOK_OVERVIEW.md)
- **精華長文**: [DIGEST.md](./DIGEST.md)
- **用語集**: [GLOSSARY.md](./GLOSSARY.md)
- **固定source**: [SOURCE_MANIFEST.md](./SOURCE_MANIFEST.md)

## Skill一覧

### 実行と自動化

- [`codex-execution-mode-routing`](./codex-execution-mode-routing/SKILL.md) — CLI・exec・cloudを介入モデルで選ぶ。
- [`codex-exec-io-contract`](./codex-exec-io-contract/SKILL.md) — execのprogress、event、最終値を機械契約へ分ける。
- [`codex-ci-patch-handoff`](./codex-ci-patch-handoff/SKILL.md) — CIの推論credentialとwrite authorityをpatchで分離する。

### 安全境界と接続

- [`codex-sandbox-approval-boundary`](./codex-sandbox-approval-boundary/SKILL.md) — 技術的能力と人の昇格同意を二層で設計する。
- [`codex-egress-surface-governance`](./codex-egress-surface-governance/SKILL.md) — search・command・MCP・HTTPの通信経路を個別統制する。
- [`codex-auth-boundary-selection`](./codex-auth-boundary-selection/SKILL.md) — 利用面ごとに認証flowとcredential scopeを選ぶ。
- [`codex-mcp-control-plane`](./codex-mcp-control-plane/SKILL.md) — MCPの必須性・tool範囲・approvalを分離する。

### 文脈と分業

- [`codex-context-entry-routing`](./codex-context-entry-routing/SKILL.md) — image・search・MCP・conversationから適切な入口を選ぶ。
- [`codex-bounded-subagents`](./codex-bounded-subagents/SKILL.md) — read-heavyなbounded roleへ分解して親で再統合する。

## 関係図

```mermaid
graph LR
    MODE["execution-mode-routing"] ===>|composes-with| IO["exec-io-contract"]
    CI["ci-patch-handoff"] -->|depends-on| SAFE["sandbox-approval-boundary"]
    CI ===>|composes-with| IO
    CI ===>|composes-with| AUTH["auth-boundary-selection"]
    SAFE ===>|composes-with| EGRESS["egress-surface-governance"]
    EGRESS ===>|composes-with| MCP["mcp-control-plane"]
    MCP -->|depends-on| EGRESS
    CONTEXT["context-entry-routing"] ===>|composes-with| EGRESS
    CONTEXT ===>|composes-with| MCP
    SUB["bounded-subagents"] ===>|composes-with| CONTEXT
    SUB ===>|composes-with| MCP
    MODE -.->|contrasts-with| SUB
```

図例: `-->` はdepends-on、`-.->` はcontrasts-with、`===>` はcomposes-with。

## 推奨学習順

1. **codex-execution-mode-routing** — まずtaskをどの実行面へ置くか決める。
2. **codex-sandbox-approval-boundary** — 実行主体の能力と昇格条件を分ける。
3. **codex-exec-io-contract** — 非対話実行を選んだ場合の機械契約を作る。
4. **codex-auth-boundary-selection** — 利用面へcredential flowを対応させる。
5. **codex-egress-surface-governance** — 外向き通信をsurface別に監査する。
6. **codex-mcp-control-plane** — MCP surfaceをserver・tool・approvalへ掘り下げる。
7. **codex-context-entry-routing** — 問題に必要な外部contextの入口を選ぶ。
8. **codex-bounded-subagents** — contextとauthorityをbounded roleへ分ける。
9. **codex-ci-patch-handoff** — 上記の境界と契約をCI job分離へ統合する。

## 監査軌跡

- 候補池: [candidates/](./candidates/)
- 三重検証: [verified.md](./verified.md)
- 統合記録: [merged.md](./merged.md)
- 棄却理由: [rejected/](./rejected/)
- 単一ページ版の停止記録: [audit/single-page/](./audit/single-page/)

## conflict-clarity

Pack entry skill: [`conflict-clarity`](./conflict-clarity/SKILL.md)

# conflict-clarity — Skill Index

> cangjie-skillにより150曲を単一書籍として蒸留。検証済みskillは **11件**。
> 処理日: 2026-08-18

## この資料について

- **主な作詞者**: 柳沢亮太（ほか渋谷龍太、上杉研太）
- **一句の主旨**: 不確実さや痛みを消さず、人と向き合い、今の選択と継続で希望を具体化する。
- **全体理解**: [BOOK_OVERVIEW.md](./BOOK_OVERVIEW.md)
- **統合正本**: [corpus.json](./corpus.json)
- **用語集**: [GLOSSARY.md](./GLOSSARY.md)
- **精華長文**: [DIGEST.md](./DIGEST.md)（段階5）

---

## Skill一覧

### 感情・関係

- [`emotion-to-protected-value`](./emotion-to-protected-value/SKILL.md) — 矛盾感情から守りたい価値を逆算する
- [`imperfect-understanding-dialogue`](./imperfect-understanding-dialogue/SKILL.md) — 完全理解を待たずに関係を作る
- [`protected-object-boundary-test`](./protected-object-boundary-test/SKILL.md) — 自己犠牲か回避かを保護対象で判定する

### 判断・倫理

- [`gradient-beyond-binary`](./gradient-beyond-binary/SKILL.md) — 二択を連続量へ戻すグラデーション思考
- [`purpose-impact-justice-audit`](./purpose-impact-justice-audit/SKILL.md) — 正しさを目的と影響で監査する
- [`non-ranking-multiple-values`](./non-ranking-multiple-values/SKILL.md) — 複数の大切を安易に順位付けしない

### 時間・変化

- [`adaptive-continuity`](./adaptive-continuity/SKILL.md) — 変えない価値のために手段を更新する
- [`regret-to-present-commitment`](./regret-to-present-commitment/SKILL.md) — 過去の反実仮想を現在の約束へ変える
- [`future-authored-meaning`](./future-authored-meaning/SKILL.md) — 痛みへ後から意味を付与する
- [`restart-as-continuation`](./restart-as-continuation/SKILL.md) — 再始動をゼロではなく経験の続きと捉える
- [`possibility-under-uncertainty`](./possibility-under-uncertainty/SKILL.md) — 確信ではなく可能性を行動根拠にする

---

## 引用図

```mermaid
graph LR
    emotion_to_protected_value["emotion-to-protected-value"] ==>|"composes-with"| gradient_beyond_binary["gradient-beyond-binary"]
    protected_object_boundary_test["protected-object-boundary-test"] -->|"depends-on"| emotion_to_protected_value["emotion-to-protected-value"]
    purpose_impact_justice_audit["purpose-impact-justice-audit"] -->|"depends-on"| gradient_beyond_binary["gradient-beyond-binary"]
    purpose_impact_justice_audit["purpose-impact-justice-audit"] ==>|"composes-with"| protected_object_boundary_test["protected-object-boundary-test"]
    imperfect_understanding_dialogue["imperfect-understanding-dialogue"] ==>|"composes-with"| gradient_beyond_binary["gradient-beyond-binary"]
    imperfect_understanding_dialogue["imperfect-understanding-dialogue"] ==>|"composes-with"| emotion_to_protected_value["emotion-to-protected-value"]
    non_ranking_multiple_values["non-ranking-multiple-values"] -->|"depends-on"| gradient_beyond_binary["gradient-beyond-binary"]
    non_ranking_multiple_values["non-ranking-multiple-values"] ==>|"composes-with"| adaptive_continuity["adaptive-continuity"]
    adaptive_continuity["adaptive-continuity"] -.->|"contrasts-with"| restart_as_continuation["restart-as-continuation"]
    regret_to_present_commitment["regret-to-present-commitment"] ==>|"composes-with"| future_authored_meaning["future-authored-meaning"]
    restart_as_continuation["restart-as-continuation"] ==>|"composes-with"| future_authored_meaning["future-authored-meaning"]
    possibility_under_uncertainty["possibility-under-uncertainty"] ==>|"composes-with"| restart_as_continuation["restart-as-continuation"]
    regret_to_present_commitment["regret-to-present-commitment"] -.->|"contrasts-with"| possibility_under_uncertainty["possibility-under-uncertainty"]
```

- `-->` depends-on
- `-.->` contrasts-with
- `==>` composes-with

---

## 推奨学習順

1. `gradient-beyond-binary` — 二択を解除する基礎
2. `emotion-to-protected-value` — 感情から価値を読む
3. `imperfect-understanding-dialogue` — 不完全な理解で接続する
4. `protected-object-boundary-test` — 自己犠牲と境界を判定する
5. `purpose-impact-justice-audit` — 正しさの運用を監査する
6. `non-ranking-multiple-values` — 複数価値を保持する
7. `future-authored-meaning` — 過去の意味を更新する
8. `regret-to-present-commitment` — 後悔を現在の約束へ変える
9. `adaptive-continuity` — 核を守り手段を変える
10. `restart-as-continuation` — 経験を持って再開する
11. `possibility-under-uncertainty` — 不確実性の中で試行する

---

## 監査

- 段階1〜4の正本: `corpus.json` の `pipeline`
- JSON統合前の中間成果: `audit/`
- 全候補の行先: `pipeline.candidate_disposition`

## Custom skills

```mermaid
flowchart TD
```
