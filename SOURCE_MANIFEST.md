# Codex CLI公式資料コーパス

- **取得日**: 2026-08-17
- **提供者**: OpenAI
- **起点**: https://learn.chatgpt.com/docs/codex/cli
- **収録規則**: 起点ページ本文と、同ページ本文から直接リンクされたCodex CLI関連の公式詳細ページ。二段階目以降のリンク先は含めない。

| # | 資料 | 取得形式 | 文字数 | SHA-256 |
|---:|---|---|---:|---|
| 1 | `https://learn.chatgpt.com/docs/codex/cli.md` | Markdown | 6,650 | `4592869a38de248eef8c623816032bc34787c7797fcf7a64e41d860da83d1a5e` |
| 2 | `https://learn.chatgpt.com/docs/developer-commands.md?surface=cli` | Markdown | 48,995 | `1257cd53d15c2a2f3293d4e59eeb3f7ac33cfa6a1b62675fff890dab308e9b00` |
| 3 | `https://learn.chatgpt.com/docs/auth.md` | Markdown | 15,024 | `04400cae9aa4d0671bd8960e6935c38ded38d988f70cc2c01acec1754276ead5` |
| 4 | `https://learn.chatgpt.com/guides/best-practices` | HTML本文抽出 | 341,330 | `825a3e52ca7d81030dd728400ccfda94b28ad294793dbdbb2dcf135f070647c2` |
| 5 | `https://learn.chatgpt.com/docs/configuration.md?surface=cli` | Markdown | 5,875 | `2da49e5820a94b99d862609020ddc4f8daa9e8a638859e7db525a9cd5c328f30` |
| 6 | `https://learn.chatgpt.com/docs/non-interactive-mode.md` | Markdown | 14,784 | `b4792bedcfec440b81a27f2ce43a75a893d2a3bfdfa55e016b53e4cc4db32111` |
| 7 | `https://learn.chatgpt.com/docs/skills-and-plugins.md?surface=cli` | Markdown | 4,812 | `0ad76146f66f6239da09714f0731c48d8f4132f7d377e879e79d3aca79c1e7e7` |
| 8 | `https://learn.chatgpt.com/docs/code-review.md?surface=cli` | Markdown | 1,232 | `0a9b272a61053dd26a682aa3d7ce68e0649b2eedc870cd7a9bcb8d9f53c3acd0` |
| 9 | `https://learn.chatgpt.com/docs/image-inputs.md?surface=cli` | Markdown | 1,505 | `8195d27ea41db23f03ae7ef9f15efc784f7393e8c135c5ac22e2cdcb4d76c4fd` |
| 10 | `https://learn.chatgpt.com/docs/agent-configuration/subagents.md` | Markdown | 21,893 | `af1e8dd56122dd3695f403ab338ac38a9aa567f4cb0abe80954021627879f472` |
| 11 | `https://learn.chatgpt.com/docs/web-search.md?surface=cli` | Markdown | 2,545 | `3a9bb0b8188e76809c2d0ab3518b639951538d5a92967cffc5d3f2c85397ffd0` |
| 12 | `https://learn.chatgpt.com/docs/cloud.md` | Markdown | 3,770 | `8c1150eb061138b05655ce4cc7f8341e254f13582285d50c7ec9c4b2482fb898` |
| 13 | `https://learn.chatgpt.com/docs/extend/mcp.md?surface=cli` | Markdown | 9,091 | `df26c56146409dd902f6bc3d86fcc9f27d09519424cd0278f159258b4ea9fd0b` |
| 14 | `https://learn.chatgpt.com/docs/agent-approvals-security.md` | Markdown | 32,014 | `28996f6ab862cfdb01b85b18edf2d9646023e53eb20ae82d90c277c61f4f2df6` |
| 15 | `https://learn.chatgpt.com/docs/cli-customization.md` | Markdown | 1,638 | `7f59bf08264c63061b59a6a0050376c4633d22c9e96915ec1d565e85a032b382` |

## 監査上の注意

- `Configuration` は詳細設定そのものではなく、設定領域へのナビゲーションページである。
- `Developer commands` の対話テーブルはMarkdown中でコンポーネント参照になっている箇所があり、本文に展開されない全フラグ値はコーパス外とする。
- `Best practices` はMarkdown版が取得できなかったため、公式HTMLから本文部分を読み取った。
- 取得後に公式ページが更新される可能性がある。再蒸留時はハッシュを取り直す。
