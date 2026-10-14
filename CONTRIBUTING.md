# Contributing

## Before you send a change

```bash
python3 scripts/check_parts.py .       # references between controllers and parts
python3 scripts/bump_version.py --check # every manifest carries the same version
python3 scripts/check_i18n.py           # translations against their English source
```

CI runs the same three commands on every pull request.

- **Behavior changes** (controllers, parts, rules) need a `CHANGELOG.md` entry and, for a rule, evidence in `rules/RULES.md`. Edits to a copied part are recorded in `UPSTREAM.md`.
- **Version:** change it only with `python3 scripts/bump_version.py <x.y.z>`.
- **No private data:** no company, product, repo or team names, internal ticket or PR numbers, local paths or personal names in any file. Describe evidence from private repos generically ("a private Angular repository").

## Documentation languages

English is the source. Agent-facing files (`skills/`, `parts/`, `rules/`, `standards/`, `templates/`, `agents/`, `harness/`) exist only in English: the lab measured those prompts in English, so translating them would change what the agent does.

Human docs are translated by tier ([`docs/i18n.json`](docs/i18n.json)):

| Tier | Languages | Files |
|---|---|---|
| 1 | en, vi, zh-CN, ja | root README, `README.md` (docs index), `01-overview.md`, `03-skills.md`, `05-setup-and-usage.md`, `glossary.md` |
| 2 | en, vi | `02-architecture.md`, `04-rules.md`, `06-evidence.md`, `07-maintenance.md` |
| 3 | en | `08-roadmap.md`, `09-init-and-standards.md`, `CHANGELOG.md`, `harness/` |

Layout: `README.md` + `README.<lang>.md` at the root; `docs/<lang>/<same file name>`.

### Changing a doc

1. Edit the English file (`README.md` or `docs/en/…`).
2. Update the translations in the same pull request if you can. If you cannot, leave them: `check_i18n.py` reports them as stale (a warning, not a failure) until someone updates them.

### Writing or updating a translation

- First line, exactly: `<!-- i18n: source=docs/en/<file>.md source_commit=<commit> review=machine|human -->`. `source_commit` is the commit (or release tag, e.g. `v1.0.0`) of the English file you translated from (`git log -1 --format=%h -- docs/en/<file>.md`). `review=human` once a native speaker has read the whole file.
- Second line: the language switcher; then a note that the English version is authoritative.
- Copy fenced code blocks byte for byte; `check_i18n.py` compares them with the source.
- Never translate commands, paths, config keys, skill names (`dk:…`), rule IDs, numbers or section numbers.
- Keep these terms in English: controller, part, rule, skill, subagent, harness, finding, certain / suspect, verdict, GO / NO-GO, backtest, baseline, worktree, artifact. Each language's `glossary.md` lists the rest.
- Link to files, not to `#anchors` in other files (headings differ by language). A doc missing in your language links to `../en/…`.
