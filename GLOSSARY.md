# Codex CLI 用語集

出典は `SOURCE_MANIFEST.md` に固定した OpenAI 公式資料。定義は原文候補を日本語で要約し、
「区別」はこの蒸留で誤用を防ぐための境界を示す。

| 用語 | 公式資料での意味 | 重要な区別 |
|---|---|---|
| sandbox mode | Codexが技術的にread/write/networkできる範囲 | approval policyの「実行前に尋ねる時点」とは別 |
| approval policy | action実行前にCodexが確認を求める条件 | 操作自体を不可能にするsandboxではない |
| network proxy | command networkが有効な場合にtrafficをpolicyへ制限する仕組み | network能力を付与せず、web searchやMCP全体もfilterしない |
| web search | sandboxed command networkとは別のhosted search tool | cached・indexed・live modeを持ち、結果はuntrusted |
| codex exec | interactive TUIを開かずscriptからCodexを実行する入口 | CI・pipeline向けで途中対話を前提にしない |
| JSONL output | 実行中にCodexが出すeventごとのJSON Lines stream | 最終JSON一個ではなくstate change列 |
| output schema | 最終responseをJSON Schemaへ適合させる指定 | JSONL event streamとは目的が違う |
| AGENTS.md | 自動的にcontextへ読み込まれるagent向けopen-format guidance | 一回限りのpromptでなく階層化された持続instruction |
| skill | task固有のguidance・resources・scriptsをまとめた再利用workflow | 外部connectionを含むplugin全体ではない |
| plugin | skills、connectors等を含められるinstallable bundle | focused instructionだけのskillより広い配布単位 |
| Model Context Protocol (MCP) | modelをtoolsとcontextへ接続するprotocol | 静的context貼付でなくSTDIO/HTTP server経由の接続 |
| subagent | specific taskを処理するためCodexが起動するdelegated agent | main chatの追加turnではなく独立contextのbounded work |
| context pollution | 中間logや探索notesで重要情報が埋もれた状態 | context容量不足そのものではない |
| custom agent | personal/project scopeのTOMLで定義する再利用可能な専門agent | spawn時だけの一時指示と異なりmodel・sandbox・toolsも固定可能 |
| resume | IDまたは直近chatのinteractive sessionを継続する操作 | 新規chatを作らず既存transcriptを継ぐ |
| fork | 過去sessionから新しいchatへ分岐する操作 | 元transcriptを保持し代替方針を別IDへ隔離する |
| Codex cloud | isolated cloud environmentへtaskを委譲し後からdiffをreviewする実行面 | local CLIのremote shellではない |
| code review | 選択diffを読み、working treeを変えずfindingを返す専用reviewer | 実装修正と別役割・別turn |
| credential store | `file`、`keyring`、`auto`によるcached credential保存先 | login方式ではなく取得後の保存場所 |
| permission profile | workspace権限・network・domain rule等を束ねるnamed configuration | 一回限りのflagでなく再利用policy |

