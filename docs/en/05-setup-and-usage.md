English | [Tiếng Việt](../vi/05-setup-and-usage.md) | [简体中文](../zh-CN/05-setup-and-usage.md) | [日本語](../ja/05-setup-and-usage.md)

# 5. Setup and usage

## 5.1 Requirements

| Item | Notes |
|---|---|
| Agent CLI | Claude Code is the reference CLI (the lab used 2.1.296). Codex, Copilot CLI, Antigravity (`agy`), OpenCode and omp can load the kit (section 5.2) |
| `git` | Required |
| The repo's check command | `make check`, `npm test`, … `dk:init` detects and records it |
| `gh` | Optional; dev-kit never opens a PR itself |
| `codegraph`, `code-review-graph` | Optional. `dk:init` checks with `scripts/install-graph-tools.sh`; if they are missing it asks, then installs them with that script and builds the indexes by default |

## 5.2 Install

dev-kit follows the Superpowers approach: **one `skills/` set, one manifest per CLI**. What differs between CLIs lives in [`harness/`](../../harness/README.md). Each controller opens with a **Harness** paragraph: on a CLI that does not substitute `${CLAUDE_PLUGIN_ROOT}`, the agent finds the kit directory itself (two levels above `SKILL.md`, after resolving symlinks) and reads the notes for its CLI.

**Claude Code** (reference CLI):

```bash
claude plugin marketplace add awesome-boilerplate-develop/dev-kit
claude plugin install dk@dev-kit
```

Inside a session: `/plugin marketplace add awesome-boilerplate-develop/dev-kit`, then `/plugin install dk@dev-kit`. To try a local checkout without installing (for example while changing the kit): `claude --plugin-dir /path/to/dev-kit`.

Check that it loaded: in a session, ask the agent to list the skills that start with `dk:`. You must see all 5: `dk:init`, `dk:story-runner`, `dk:bug-fixer`, `dk:code-refactor`, `dk:pre-pr-check`.

**Other CLIs** (installed from the public repo on 2026-10-14; details and caveats are in each file under `harness/`):

| CLI | Install command | Notes |
|---|---|---|
| Codex 0.160.1 | `codex plugin marketplace add awesome-boilerplate-develop/dev-kit` then `codex plugin add dk@dev-kit` | Codex installs a copy per version ([codex.md](../../harness/codex.md)) |
| Copilot CLI 1.0.89 | `copilot plugin marketplace add awesome-boilerplate-develop/dev-kit` then `copilot plugin install dk@dev-kit` | Installing straight from a repo or path still works but is reported as deprecated ([copilot.md](../../harness/copilot.md)) |
| Antigravity 1.3.5 | `agy plugin install https://github.com/awesome-boilerplate-develop/dev-kit` | `agy` registers both `agents/` and `rules/*.md` ([antigravity.md](../../harness/antigravity.md)) |
| omp 18.10.4 | `omp plugin marketplace add awesome-boilerplate-develop/dev-kit` then `omp plugin install dk@dev-kit` | omp reads Claude Code plugins; the two review agents appear as named task agents ([omp.md](../../harness/omp.md)) |
| OpenCode 1.18.35 | clone the repo, link each `skills/<name>` directory into `~/.config/opencode/skills/` | Allow reading the kit directory with `permission.external_directory` ([opencode.md](../../harness/opencode.md)) |

Not supported:
- **Gemini CLI:** since 2026-06-18 Google has moved free-tier and Google One users to the Antigravity CLI.
- **Cursor (dropped in 1.2.3):** never verified, because `cursor-agent` needs a login.
- **pi (set aside for now):** pi 1.0.2 installs and loads the kit, but core pi has no subagent tool, so every review role would have to run in the main session; that mode has not been measured.

dev-kit's rules and lab evidence were measured on Claude. On the CLIs in the table, loading the kit has been verified; review quality has had only one backtest, on Codex, and the other CLIs are unmeasured ([06](06-evidence.md)).

## 5.3 Install for all projects or per project

| Method | Scope | Notes |
|---|---|---|
| `claude --plugin-dir /path/to/dev-kit` | That session only | Loads a local checkout; touches no configuration; useful while changing the kit |
| `claude plugin install dk@dev-kit` | User (all projects) by default | The install reported `scope: user` (2026-10-14); a project-only option is not verified ❓ |

Suggestion: install for your user, and run `dk:init` only in repos where you use it. Do not enable dev-kit in a repo's shared `.claude/settings.json`: it is a personal kit (rule O1).

## 5.4 Using it with other plugins (Superpowers, code-review…)

**No name collisions:**
- A plugin's skills always carry the plugin name as a prefix (`superpowers:…`, `code-review:…`, `dk:…`).
- dev-kit's sub-skills live in `parts/` and are not registered as skills.

**You do not need to turn other plugins off.** The lab ran 3 cards (B1, S1, P2) with a real global configuration: 17 plugins, including Superpowers and the official `code-review`.
- **Only the `dk:*` skills were invoked;** quality held (3/3, 8/8, 5/5 defects).
- **Cost was about 15–50% higher** than in isolation, because every enabled plugin adds skill descriptions and hooks to the context.

**Good to know:**
- **That test invoked the skill by name** (`Use skill dk:…`). If you only say something general ("fix this bug"), Superpowers may win the skill choice through its `SessionStart` hook (`using-superpowers`). Not measured ❓. Invoking the controller by name is the safe way.
- **To save context,** enable only the plugins you need in that project.

## 5.5 Installing the graph tools with the script

```bash
bash /path/to/dev-kit/scripts/install-graph-tools.sh --check    # see what is already installed
bash /path/to/dev-kit/scripts/install-graph-tools.sh --install  # install the pinned version of whatever is missing
```

| Tool | Pinned version | Installed with |
|---|---|---|
| codegraph | v1.5.0 | codegraph's official `install.sh`, pinned by tag; placed in `~/.codegraph/` and `~/.local/bin/codegraph` |
| code-review-graph | 2.3.9 | `pipx`; falls back to `uv tool` if pipx is missing |

**Notes:**
- **Tools that are already installed are left alone.** The script never upgrades or downgrades, because codegraph's `install.sh` deletes other versions when it installs.
- **The script registers no MCP server and no hook** (it never runs `… install`).
- **`dk:init` calls this script** after asking you. You can also run it yourself.

## 5.6 What if you do not install the graph tools

**Running is not affected:** every controller still does all its steps. Only rule G1 is off:
- the agent finds code with grep and file reads instead of `codegraph`;
- `pre-pr-check` has no CRG summary of risk and missing tests.

The lab measured 17 SWE Django tasks (Haiku): with and without an index both solved 10/17, at the same cost. The only change was that the agent used grep about half as often. The benefit may be clearer on large or unfamiliar repos, where finding code is the hard part; this is not measured ❓.

## 5.7 First time on a repo

```text
Use skill dk:init for this repo.
```

The agent probes the repo first, then asks one question at a time, in order: commands and base branch, graph indexes, quick or detailed setup (quick takes the Recommended lines and asks once at the end, with a checklist where the Recommended items are already ticked and you add or remove), the baseline (only if it is red), the standards in two passes (rules for writing code, then the review checklist; each a list of groups and a loop for your own conventions), and the optional `CONSTRAINTS.md`. Each question shows its evidence and a Recommended line; reply "default", "skip" or your answer. It creates `.dev-kit/` (ignored by git, nothing to commit). To redo one part later: `dk:init index`, `dk:init baseline`, `dk:init standards [rules|review]`.

**Starting `dk:init` on each CLI** (dev-kit 1.4.x, runs of 2026-10-15 on one private repo; add "answer in Vietnamese" or your language to the first message if you want):

| CLI | First message | Questions in the interactive session | One prompt per turn (headless) |
|---|---|---|---|
| Claude Code | `/dk:init` (Claude Code has its own `init`) | not run with 1.4.x | `claude -p … --resume <session>`: one question per turn, choices as text (checked) |
| Codex | `$dk:init` | not run with 1.4.x | `codex exec` then `codex exec resume <id> "<answer>"`: one question per turn (checked); `resume` takes `-c sandbox_mode=…`, not `-s` |
| Copilot CLI | `/dk:init` | `ask_user` forms (checked) | `copilot -p` takes every default and asks nothing (checked) |
| Antigravity | `/dk:init`, started with `agy -i` | `ask_question` forms with a "Write-in…" line (checked) | `agy -p` auto-skips the forms and takes every default (checked) |
| OpenCode | `/init …` (skills have no namespace; in `opencode run` this loaded the skill) | not run | `opencode run` then `opencode run -c "<answer>"`: one question per turn (checked); allow the kit folder in `external_directory` first ([opencode.md](../../harness/opencode.md)) |
| omp | `/dk:init` | not run with 1.4.x | `omp -p` then `omp -p -c "<answer>"`: one question per turn (checked) |

For real use, run the interactive session and answer yourself; headless modes are for scripted checks.

## 5.8 Daily use

Call a controller by card type and paste the card in:

```text
Use skill dk:bug-fixer for this card:
<card text / issue link>
```

| Card type | Skill |
|---|---|
| Feature/story | `dk:story-runner` |
| Bug, performance problem | `dk:bug-fixer` |
| Tech debt, refactoring | `dk:code-refactor` |
| Finished branch, check before PR | `dk:pre-pr-check` |
| Check someone else's branch without changing it | `dk:pre-pr-check`, with the phrase "report only, do not change code" |

**For a deeper review than the default:** say explicitly "review with all 4 reviewers" (rule C2).

**Output to look at:**
- `.dev-kit/reports/<name>.md`: what was done, why, the commands run and their results;
- `.dev-kit/reports/pr-body.md`: the drafted PR body;
- `.dev-kit/specs/` (story): especially the **Decisions** section, to see what the agent settled;
- commits on the current branch. dev-kit does not push and does not open a PR.

## 5.9 Keeping a trial log

For each card, write one line in a copy of [`templates/dogfood-log.md`](../../templates/dogfood-log.md):
- the path taken (direct or SDD, review depth);
- whether rework was needed;
- what the review really caught;
- cost;
- whether the process got in the way.

At the end of the week, answer the 4 questions at the bottom of the template. This is the main data for deciding the next step, because the lab cannot measure "useful to a real person".

## 5.10 When something goes wrong

| Symptom | Check |
|---|---|
| No `dk:*` skills appear | Is the plugin loaded (`--plugin-dir` or `/plugin`)? Is the path correct? |
| The agent calls `superpowers:…` instead of following the controller | Invoke `dk:<controller>` by name; if it is still pre-empted, turn Superpowers off in that project (5.4) |
| A controller stops midway | Report it with the transcript; rule F1 should have prevented this |
| Four reviewers run on an ordinary diff | Check whether the diff touches auth/secrets/personal data/config/migrations; if not, that is a bug in applying rule C2 |
| The report has no check-command output | The command in `.dev-kit/config.yml` is wrong or missing: run `dk:init` again |
