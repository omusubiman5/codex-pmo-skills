# Case candidates — Codex CLI

## Extraction audit

- **Stage**: 1 (case extraction only)
- **Extractor contract**: `extractors/case-extractor.md`
- **Corpus**: `https://learn.chatgpt.com/docs/codex/cli.md`
- **Corpus boundary**: Only the Markdown body returned by the URL above was examined. Linked pages were not opened or treated as source text.
- **Result**: No qualifying case candidates were found.
- **Reason**: The page is a product overview and getting-started guide. It contains feature descriptions, installation commands, suggested first prompts, and hypothetical input examples, but no event in which OpenAI or a cited third party applies a methodology and reports an observed outcome. Creating `summary`, `bound_to`, or `outcome` values for those examples would require invention beyond the source.
- **Excluded near-matches**:
  - `Tell me about this project` is an example prompt, not a documented application with a result.
  - “an error screenshot, architecture diagram, or design reference” lists possible image inputs, not a historical case.
  - The descriptions of interactive work, code review, CI, subagents, web search, cloud, MCP, and permissions state capabilities or recommended uses; they do not narrate a completed application and outcome.

```yaml
[]
```
