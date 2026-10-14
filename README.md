English | [Tiếng Việt](README.vi.md) | [简体中文](README.zh-CN.md) | [日本語](README.ja.md)

# dev-kit

[![Release](https://img.shields.io/github/v/release/awesome-boilerplate-develop/dev-kit)](https://github.com/awesome-boilerplate-develop/dev-kit/releases) [![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE) [![docs](https://github.com/awesome-boilerplate-develop/dev-kit/actions/workflows/docs.yml/badge.svg)](https://github.com/awesome-boilerplate-develop/dev-kit/actions/workflows/docs.yml)

Agent skills for kanban-card work: stories, bugs, refactors, and a check before you open a PR. Every rule the skills follow was kept only if it helped in a measured lab.

Works with **Claude Code** (reference), **Codex**, **GitHub Copilot CLI**, **Antigravity**, **OpenCode** and **omp**.

## Skills

| Skill | Use it for |
|---|---|
| `dk:init` | First run in a repo: check tools, write `.dev-kit/config.yml`, record a test baseline |
| `dk:story-runner` | A feature or story card: clarify, spec, implement with tests, then `dk:pre-pr-check` |
| `dk:bug-fixer` | A bug card, including performance regressions: root cause, regression test, fix |
| `dk:code-refactor` | A tech-debt card: restructure without changing behavior |
| `dk:pre-pr-check` | A finished branch: run the checks, review at a depth set by risk, write the report and PR text |

The plugin is named `dk`. Some CLIs show the skills without the `dk:` prefix.

## Install

### Claude Code

```bash
claude plugin marketplace add awesome-boilerplate-develop/dev-kit
claude plugin install dk@dev-kit
```

Inside a session, the same with `/plugin marketplace add awesome-boilerplate-develop/dev-kit` and `/plugin install dk@dev-kit`.

### Codex

```bash
codex plugin marketplace add awesome-boilerplate-develop/dev-kit
codex plugin add dk@dev-kit
```

### GitHub Copilot CLI

```bash
copilot plugin marketplace add awesome-boilerplate-develop/dev-kit
copilot plugin install dk@dev-kit
```

### Antigravity

```bash
agy plugin install https://github.com/awesome-boilerplate-develop/dev-kit
```

### omp

```bash
omp plugin marketplace add awesome-boilerplate-develop/dev-kit
omp plugin install dk@dev-kit
```

### OpenCode

OpenCode loads skills from folders, so clone the repo and link the skills:

```bash
git clone https://github.com/awesome-boilerplate-develop/dev-kit ~/.dev-kit
mkdir -p ~/.config/opencode/skills
for s in ~/.dev-kit/skills/*; do ln -s "$s" ~/.config/opencode/skills/; done
```

Then let OpenCode read the kit folder, in `~/.config/opencode/opencode.json`:

```json
{ "permission": { "external_directory": { "~/.dev-kit/**": "allow" } } }
```

### Other CLIs

- **Cursor:** a manifest is included but not verified yet.
- **Not supported:** Gemini CLI (Google moved free-tier users to Antigravity), pi (no subagent tool in pi core).

Per-CLI details (where the install lives, the subagent tool, known caveats): [`harness/`](harness/README.md).

## Quick start

1. Open your repo with the agent and ask it to **use `dk:init`**. It checks your tools, detects the test and build commands, asks before installing anything, and records the current test baseline in `.dev-kit/`.
2. Hand it a card by name:

   ```text
   Use dk:bug-fixer for this card: "Checkout total drops to 0 when two promotions apply."
   ```

3. When it finishes you get a commit, a short report in `.dev-kit/reports/`, and a GO / NO-GO verdict from `dk:pre-pr-check`.

## How it works

- **Thin controllers.** Each controller is a short skill that works directly in the session. The longer playbooks it borrows (TDD, debugging, planning, review…) live in `parts/` and are read only when a step needs them, so they cost no context at session start.
- **Rules with evidence.** [`rules/RULES.md`](rules/RULES.md) lists every rule, whether it is on, and the lab result behind it. A rule is turned on only if it helped on at least five tasks it had not seen.
- **Review depth by risk.** `dk:pre-pr-check` picks self-review, one reviewer or four (standards, spec, security, tests) from the size and kind of the diff.
- **Machine-checked reports.** [`scripts/check_report.py`](scripts/check_report.py) rejects a report until a "certain" finding sits in the changed code, is not a generic missing-test remark, and cites only rules that exist.
- **Layered standards.** Kit, team and project standards (`.dev-kit/standards/`); each reviewer gets only the topics of its role.
- **Optional graph tools.** With [codegraph](https://github.com/colbymchenry/codegraph) and code-review-graph indexes, controllers locate code, measure blast radius and run `detect-changes` before review.

## Evidence

- **Lab** (234 runs, Haiku 5.5, a sample app and 13 SWE-bench Verified Django tasks): code quality on par with the model working alone, at about 2× the cost. The extra spend buys the review layer and the artifacts, not more correct code.
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
