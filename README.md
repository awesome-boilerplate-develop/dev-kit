English | [Tiếng Việt](README.vi.md) | [简体中文](README.zh-CN.md) | [日本語](README.ja.md)

# dev-kit

[![Release](https://img.shields.io/github/v/release/awesome-boilerplate-develop/dev-kit)](https://github.com/awesome-boilerplate-develop/dev-kit/releases) [![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE) [![docs](https://github.com/awesome-boilerplate-develop/dev-kit/actions/workflows/docs.yml/badge.svg)](https://github.com/awesome-boilerplate-develop/dev-kit/actions/workflows/docs.yml)

Agent skills for kanban-card work: stories, bugs, refactors, and a check before you open a PR. Every rule the skills follow is listed with the evidence behind it; rules that did not help in the lab are switched off.

Works with **Claude Code** (reference), **Codex**, **GitHub Copilot CLI**, **Antigravity**, **OpenCode** and **omp**.

## Skills

| Skill | Use it for |
|---|---|
| `dk:init` | First run in a repo: check tools, write `.dev-kit/config.yml`, record a test baseline |
| `dk:brainstorm` | An idea before there is a clear card: compare approaches, agree a spec for `dk:story-runner`; no code |
| `dk:ticket` | A Jira Cloud or Azure DevOps ticket: pull it with its images, links, attachments and comments into `.dev-kit/tickets/` as input for the skills above, then name the one to run next; read-only, no analysis |
| `dk:story-runner` | A feature or story card: clarify, spec, implement with tests, then `dk:pre-pr-check` |
| `dk:bug-fixer` | A bug card, including performance regressions: root cause, regression test, fix |
| `dk:code-refactor` | A tech-debt card: restructure without changing behavior |
| `dk:pre-pr-check` | A finished branch: run the checks, review at a depth set by risk, write the report and PR text |

The plugin is named `dk`. Some CLIs show the skills without the `dk:` prefix.

## Install

Each CLI below has its install and update commands. After an update, start a new session so the agent loads the new skills; the CLI's plugin list shows the version (see `CHANGELOG.md` for what changed).

### Claude Code

Install:

```bash
claude plugin marketplace add awesome-boilerplate-develop/dev-kit
claude plugin install dk@dev-kit
```

Update, then restart Claude Code:

```bash
claude plugin marketplace update dev-kit
claude plugin update dk@dev-kit
```

Inside a session: `/plugin marketplace add awesome-boilerplate-develop/dev-kit` and `/plugin install dk@dev-kit`; to update, `/plugin marketplace update dev-kit`, then update `dk` from `/plugin`.

### Codex

Install:

```bash
codex plugin marketplace add awesome-boilerplate-develop/dev-kit
codex plugin add dk@dev-kit
```

Update:

```bash
codex plugin marketplace upgrade dev-kit
codex plugin add dk@dev-kit
```

### GitHub Copilot CLI

Install:

```bash
copilot plugin marketplace add awesome-boilerplate-develop/dev-kit
copilot plugin install dk@dev-kit
```

Update:

```bash
copilot plugin marketplace update dev-kit
copilot plugin update dk@dev-kit
```

### Antigravity

Install:

```bash
agy plugin install https://github.com/awesome-boilerplate-develop/dev-kit
```

To update, run the same command again; it replaces its copy.

### omp

Install:

```bash
omp plugin marketplace add awesome-boilerplate-develop/dev-kit
omp plugin install dk@dev-kit
```

Update:

```bash
omp plugin marketplace update dev-kit
omp plugin upgrade dk@dev-kit
```

### OpenCode

OpenCode loads skills from folders, so clone the repo and link the skills into your user skill folder:

```bash
git clone https://github.com/awesome-boilerplate-develop/dev-kit ~/dev-kit
mkdir -p ~/.config/opencode/skills
for s in ~/dev-kit/skills/*; do ln -s "$s" ~/.config/opencode/skills/; done
```

Then let OpenCode read the kit folder, in `~/.config/opencode/opencode.json`:

```json
{ "permission": { "external_directory": { "~/dev-kit/**": "allow" } } }
```

To update, pull the clone and link again in case a skill folder was added:

```bash
git -C ~/dev-kit pull
for s in ~/dev-kit/skills/*; do ln -sfn "$s" ~/.config/opencode/skills/; done
```

The update commands were run for Codex, Antigravity and omp for each release on 2026-10-15, and for Claude Code on 2026-10-25 (1.7.5 to 1.9.1); the Copilot lines follow `copilot plugin --help` and were not run here.

### Other CLIs

- **Not supported:** Gemini CLI (Google moved free-tier users to Antigravity), pi (no subagent tool in pi core), Cursor (never verified; dropped).

Per-CLI details (where the install lives, the subagent tool, known caveats): [`harness/`](harness/README.md).

## Quick start

1. Open your repo with the agent and ask it to **use `dk:init`**. It probes the repo, then asks a few questions one at a time (commands, graph indexes, a standards checklist by topic with rules it suggests from your code), creates `.dev-kit/` and records the current test baseline.
2. Hand it a card by name:

   ```text
   Use dk:bug-fixer for this card: "Checkout total drops to 0 when two promotions apply."
   ```

3. When it finishes you get a commit, a short report in `.dev-kit/reports/`, and a GO / NO-GO verdict from `dk:pre-pr-check`.

## How it works

- **Thin controllers.** Each controller is a short skill that works directly in the session. The longer playbooks it borrows (TDD, debugging, planning, review…) live in `parts/` and are read only when a step needs them, so they cost no context at session start.
- **Rules with evidence.** [`rules/RULES.md`](rules/RULES.md) lists every rule, whether it is on, and the evidence behind it. The workflow rules (F1, F2, C1, C2) were measured in the lab; the review and output rules (B1, R1, S1, T1, O1) come from published review practice and audits; G1 measured neutral and stays because it is cheap. An experimental rule is turned on only if it helps on at least five tasks it was not written from.
- **Review depth by risk.** `dk:pre-pr-check` picks self-review, one reviewer or four (standards, spec, security, tests) from the size and kind of the diff.
- **Machine-checked reports.** [`scripts/check_report.py`](scripts/check_report.py) rejects a report until every finding (certain or suspect) gives a `file:line` in the changed code, a certain one is not a generic missing-test remark, it cites only rules that exist, and the report names the commit range it reviewed. [`scripts/check_standards.py`](scripts/check_standards.py) checks the standards files `dk:init` writes.
- **Personal, never pushed.** Everything dev-kit writes (config, specs, plans, reports, your project standards) lives in `.dev-kit/`, which ignores itself in git; dev-kit never edits `.gitignore`, `CLAUDE.md`, `AGENTS.md` or any other tracked file.
- **Layered standards.** Kit standards, a shared folder (`standards.team`, set by hand for now; `dk:init` writes only to the repo), and your own project standards in `.dev-kit/standards/`; each reviewer gets only the topics of its role.
- **Optional graph tools.** With [codegraph](https://github.com/colbymchenry/codegraph) and code-review-graph indexes, controllers locate code, measure blast radius and run `detect-changes` before review.

## Evidence

- **Lab** (265 runs, mostly Haiku 5.5, a sample app and 13 SWE-bench Verified Django tasks): code quality on par with the model working alone, at about 2× the cost. The extra spend buys the review layer and the artifacts, not more correct code.
- **Backtests on real bugs** (a private Angular repository, Sonnet 5.5): enforcing the review steps raised `detect-changes` use from 2/6 to 6/6 PRs; catching the actual bug still varies a lot between runs.
- **A project rule for in-house UI controls** changed what the agent wrote (6 and 10 in-house tags with the rule, 18 and 16 Material tags without): the clearest win, because it is knowledge the agent cannot find by itself.

Details and limits: [docs/en/06-evidence.md](docs/en/06-evidence.md).

## Documentation

- [Docs index](docs/en/README.md): overview, architecture, each skill, rules, setup and daily use, evidence, maintenance.
- [Setup and usage](docs/en/05-setup-and-usage.md) · [Skills](docs/en/03-skills.md) · [Glossary](docs/en/glossary.md)
- Translations: Vietnamese, Simplified Chinese, Japanese (see the language links at the top). English is authoritative.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md): checks to run, versioning, and how to translate the docs. Changes are listed in [CHANGELOG.md](CHANGELOG.md).

## License

MIT, see [LICENSE](LICENSE). The parts copied from [Superpowers](https://github.com/obra/superpowers), [mattpocock/skills](https://github.com/mattpocock/skills) and [agent-skills](https://github.com/addyosmani/agent-skills) keep their MIT licenses in [`LICENSES/`](LICENSES/); see [UPSTREAM.md](UPSTREAM.md).
