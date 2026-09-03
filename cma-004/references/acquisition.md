# AI NEWS acquisition

## 共通preflight

1. 取得テーマ、期間、Gmail検索条件、Web検索条件、保存先を確認する。
2. 取得元ごとに読取経路が利用可能か検査する。利用不能な経路を成功扱いしない。
3. サンプルVaultではライブ取得結果を保存せず、架空fixtureで保存経路を検証する。
4. アカウント識別子、メールアドレス、メッセージID、Cookie、トークンを成果物やログへ保存しない。

## Gmail取得

### Codexネイティブ経路

1. `gmail_search_email_ids` を、ユーザー指定の送信元、キーワード、期間と `-in:spam -in:trash` を含むqueryで実行する。
2. 応答に `next_page_token` があれば同じqueryとtokenで続行し、最後のページまでmessage IDを集める。検索結果を暗黙の件数上限で切り捨てない。
3. message IDを100件以下に分割し、`gmail_batch_read_email` でMIME本文を取得する。
4. コネクタ応答を `scripts/extract_gmail_news.py` へ渡し、記事URL単位の候補JSONへ変換する。
5. 候補をsource本文と照合し、スポンサー、配信管理、SNS、購読解除リンクを除く。本文にないsummary、key points、ACTIONを作らない。
6. 完成したニュースJSONを `write_news_markdown.py --dry-run`、通常実行の順に渡す。

`search_emails` の要約だけで本文取得済みと判定しない。検索結果のIDとMIME本文は一時処理にだけ使い、成果物や報告へ保存しない。

### Connector応答の変換

```powershell
python .agents/skills/collect-ai-news-markdown/scripts/extract_gmail_news.py gmail-response.json `
  --retrieved-at 2026-08-15T09:00:00+09:00 `
  --sample-data > gmail-candidates.json
```

`--sample-data` は架空fixtureだけに付ける。サンプルVaultへ実在メールの本文やアドレスを保存しない。

### 失敗条件

- Gmail読取ツールが利用できない、または認可されていない。
- ページングを最後まで完了できない。
- MIME本文を取得できない。
- 記事URLを持つ候補が0件である。
- sourceに基づく全候補の検証が完了していない。

上記のいずれかではMarkdown作成0件の失敗として報告する。認証開始、メールの既読化、移動、削除、返信、ラベル変更は行わない。

## Web取得

- ユーザー指定URLを優先する。検索依頼ではテーマ、期間、対象言語に合う一次情報または発行元ページを優先する。
- 各候補についてtitle、URL、公開日時、取得日時、発行元、source本文を取得する。
- redirect後の最終URLを使い、追跡パラメータを重複判定から除外する。
- paywall、認証要求、robots制限、取得失敗を迂回しない。取得できた範囲と不足を記録する。
- フォーム入力、コメント、投稿、購入、会員登録を行わない。

## 構造化と受渡し

- 取得した各ニュースへ `source_kind: gmail` または `source_kind: web` を付ける。
- `title`、記事URL、`retrieved_at`、根拠となる `source_text` が揃わない項目は保存しない。
- AI生成のsummary、key points、ACTIONをsourceから分離し、sourceにない事実を追加しない。
- 構造化JSONを `scripts/write_news_markdown.py` へ渡す。

## 完了判定

次の全件を満たした場合だけ成功とする。

- Gmail検索の全ページ取得件数を記録した。
- 対象message IDのMIME本文を全件取得した。
- メール数、抽出候補数、採用数、重複skip数、作成数を報告できる。
- 作成Markdownを再読し、source、URL、`source_kind: gmail`、content hashを検証した。
- GmailやWebへの書込みが0件である。
