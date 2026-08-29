# Delivery manifest

## Source integrity

- Repository: `https://github.com/kangarooking/cangjie-skill.git`
- Clean base commit: `149cb39f559cafcb82910f8662b3f4e3b9ee5574`
- Public repository: `https://github.com/omusubiman5/codex-pmo-skills`
- Official source corpus: 15 documents, fixed in `SOURCE_MANIFEST.md`
- Second-level links: not used

## Build outputs

- Product: Codex Delivery Assurance
- Delivery Assurance skills: 9
- Official routing test prompts: 54
- Independent blind-test final result for official-source skills: 54/54
- Optional separate operational skill: 1 (`codex-pmo-orchestration`, not part of the Delivery Assurance package)
- PMO forward-test prompts: 7
- Independent PMO forward-test result: 7/7
- Default package/install count: 9
- Cross-skill bait result: 18/18
- INDEX: complete
- GLOSSARY: complete
- DIGEST: 9,115 characters

## Validation

- Skill directory/name correspondence: pass
- R/I/A1/A2/E/B presence: pass
- Frontmatter descriptions ≤300 characters: pass
- R quotations ≤100 English words: pass
- `test-prompts.json` parsing and case counts: pass
- Relative Markdown links: pass
- Trailing whitespace: pass

## Distribution

- Version: `0.2.0`
- Release date: `2026-08-29`
- Package: `dist/codex-delivery-assurance-0.2.0.zip`
- Package checksum: `dist/codex-delivery-assurance-0.2.0.zip.sha256`
- Payload checksum manifest: `CHECKSUMS.sha256` (also included in the ZIP)
- Status: release candidate; GO is decided only after local/remote commit, tag, package, checksum, validation, and Skill Magnet snapshot all match.
- The Delivery Assurance package comprises the 9 official-source skills that passed stage 4.
- `codex-pmo-orchestration` is distributed separately and is not selected by the Delivery Assurance package.
- Installation remains an explicit user action; the repository does not overwrite existing user skills.
