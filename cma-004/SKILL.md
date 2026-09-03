---
name: cma-004
description: 前日分のAIニュースdigestから本文読み上げ、キャラクターコメント、BGMを合成し、動画を作らず単一のポッドキャストMP3を生成する。CMA004、AI NEWS podcast、音声版ニュース生成を依頼された時に使う。
---

# CMA004 — AI NEWS Podcast Audio

このSkillは `claude-commands` に未収録だったため、`omusubiman5/claude-skills` のCMA004実装から復元した派生入口である。実行前に `references/source-manifest.md` と、必要に応じて `references/upstream-ai-news-bundler-skill.md` を読む。

## ワークフロー

1. `python3`、`ffmpeg`、`ffprobe`、TTS環境、BGM、digestアクセス、出力先をpreflightする。
2. `scripts/selector.py` の `list_news_from_digest` を使い、対象日のdigestを取得する。未指定時は前日1日分を対象にする。
3. `selected_news` と `scripts.opening`、`scripts.bodies`、`scripts.char_comments`、`scripts.ending` を含むCMA003互換config JSONを作る。`bodies` と `char_comments` はニュース件数Nと一致させる。
4. 英字残留ガードを通し、次を実行する。

```bash
python3 <skill-dir>/scripts/podcast_audio.py --config <config.json> --out <output.mp3> --log-dir <log-dir>
```

5. stdout JSONの `out`、`duration`、`news_count`、`bundle_id` と、MP3の存在・サイズ・再生時間を検証する。

## 制約

- Remotionレンダリング、動画concat、SNS投稿は行わない。
- TTSはシリアル生成し、発話順を `opening → body[i] → char[i] → ending` に保つ。
- BGMが無い場合は音声のみで続行し、結果に明記する。
- 実装に固定Linuxパスが残るため、環境不一致時は勝手に別パスへ書かず設定または修正案を示す。
- 認証値やトークンを出力しない。

## 出典

- Primary requested repository: `https://github.com/omusubiman5/claude-commands`（CMA004なし）
- Implementation repository: `https://github.com/omusubiman5/claude-skills`
- Commit: `e637454f34be352c896f61d5497d3324b2627634`
