# AI NEWS Markdown schema

## 入力JSON

トップレベルは配列、または `items` 配列を持つオブジェクトとする。

### 必須項目

| 項目 | 型 | 内容 |
| --- | --- | --- |
| `title` | string | ニュースタイトル |
| `url` | string | 出典URL。`http` または `https` |
| `retrieved_at` | string | ISO 8601形式の取得日時 |
| `source_text` | string | 保存するsource本文。要約で置換しない |
| `summary` | string | CMA001 F列相当。日本語の `結論：` / `仕組み：` 二段構成 |
| `key_points` | string[] | CMA001 G〜I列相当。本文に基づく相互に異なる日本語3点 |
| `action` | string | CMA001 J列相当。具体的な対象・数値または期限を含む日本語の次の一手 |
| `sample_data` | boolean | 配布用サンプルVaultへの保存では必ず `true` |

### 任意項目

`published_at`、`source_kind`、`source_name`、`category`、`status`、`source_ref` を使用できる。

`source_kind` は `gmail`、`web`、`fixture` のいずれかとする。

`key_points` は文字列の配列とする。`source_ref` は拡張子を含むVault相対Markdownパスとし、Vault外参照や存在しない参照を拒否する。

## 出力frontmatter

CMA001のA〜Eを `date`、`system`、`category`、`title`、`url` として同名で出力する。`url` は正規化URLとする。加えて `news_id`、`status`、`original_source_url`、`canonical_url`、`source_kind`、`published_at`、`retrieved_at`、`content_hash`、`sample_data`、必要に応じて `source_ref` を出力する。

## IDと重複

1. URLのschemeとhostを小文字化する。
2. fragment、`utm_*`、`gclid`、`fbclid`、`mc_cid`、`mc_eid` を除去する。
3. queryをキーと値で整列する。
4. 正規化URLのSHA-256先頭12桁を `news_id` とする。
5. 正規化した内容から、生のURLに含まれる追跡パラメータと取得日時を除いてSHA-256を計算し、`content_hash` とする。

同じ `news_id` と `content_hash` はduplicateとしてskipする。同じ `news_id` で異なる `content_hash` は競合として扱い、既存ファイルを上書きしない。

## 本文構造

```markdown
# タイトル

## CMA001 digest

### F: summary

### G: kp1

### H: kp2

### I: kp3

### J: action

## Source
```

AI生成項目が無い入力はCMA001未完了として拒否する。`Source`には `source_text` をそのまま保存する。
