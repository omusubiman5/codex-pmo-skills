# Delivery manifest

## Source integrity

- Repository: `https://github.com/kangarooking/cangjie-skill.git`
- Clean base commit: `149cb39f559cafcb82910f8662b3f4e3b9ee5574`
- Public repository: `https://github.com/omusubiman5/codex-pmo-skills`
- Official source corpus: 15 documents, fixed in `SOURCE_MANIFEST.md`
- Second-level links: not used

## Build outputs

- Official-source RIA++ skills: 9
- Official routing test prompts: 54
- Independent blind-test final result for official-source skills: 54/54
- Separate operational PMO skills: 1 (`codex-pmo-orchestration`)
- PMO forward-test prompts: 7
- Independent PMO forward-test result: 7/7
- Total installable skill directories: 10
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

- Status: GitHub publication prepared.
- Installable directories comprise 9 official-source skills that passed stage 4 and 1 separately audited operational PMO skill.
- Installation remains an explicit user action; the repository does not overwrite existing user skills.
