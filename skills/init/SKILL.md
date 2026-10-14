---
name: init
description: Set up dev-kit for this machine and repo, including the standards checklist by topic. Use once before first using dev-kit controllers, to re-check the setup, or to re-run one part (index, baseline, standards).
---

# init

**Harness.** Written for Claude Code, which replaces the plugin-root variable below with the dev-kit folder. If you see `${CLAUDE_PLUGIN_ROOT}` literally, your harness did not replace it: the dev-kit folder is two levels above this SKILL.md after resolving symlinks (the folder that contains `rules/RULES.md`). Read every `${CLAUDE_PLUGIN_ROOT}/…` below as a path in that folder, and first read `harness/<your harness>.md` there (`codex`, `copilot`, `cursor`, `opencode`, `antigravity`, `omp`): it maps `dk:<skill>`, subagents and the review agents to your tools.

Prepare, never run controller logic. Re-running only checks and fills gaps; never overwrite existing files. dev-kit is personal (rule O1): nothing it creates is committed, and it never edits a tracked file.

**Parts of a run.** `dk:init` runs everything below. `dk:init index` runs step 5 only (for example in a new worktree), `dk:init baseline` step 6 (the known-failure list may only shrink), `dk:init standards [topic]` step 7 (one topic if named).

**How to ask: probe first, then one question at a time, in order.** Before each question, find out what you can from the code, the graph and the files, and show that evidence with the question. Ask **one question per message**, in the order of the steps below, each with a default and short options, and wait for the answer before moving on. Number them ("Question 3 — commands"). "default" and "skip" are always valid answers. Never ask what the code already answers, and never batch questions. If nobody can answer (headless run), take the defaults and list them as assumptions in the report.

## Machine (skipped when already done)

1. **Graph tools.** Run `bash ${CLAUDE_PLUGIN_ROOT}/scripts/install-graph-tools.sh --check`. Only if a tool is missing, **ask** whether to install it (default: yes). On yes, run `bash ${CLAUDE_PLUGIN_ROOT}/scripts/install-graph-tools.sh --install` (pinned versions; tools already present are left alone) and use the absolute path it prints if the tool is not on PATH. On no, continue and note "rule G1 off: <tool> not installed". Never run `codegraph install` or `code-review-graph install`: they register MCP servers, hooks and instruction files.
2. **Personal settings.** Read `~/.dev-kit/config.yml` if it exists (the team standards folder chosen in an earlier repo). Write it only in step 7, when the user names a team folder.

## Repo

3. **Probe, no questions.** Record `git status --porcelain`. Detect the test/lint/build commands (`Makefile`, `package.json`, `pyproject.toml`, …), the base branch, the stack, the linters and type checkers with their configs (what they already enforce), files the repo already tracks under `.dev-kit/`, and the project's own `GLOSSARY.md`, `docs/adr/`, `CONSTRAINTS.md`. List the enabled plugins and remind the user to invoke `dk:<controller>` by name.
4. **Question: commands and base branch.** Show what you detected; the user confirms or corrects. Then create `.dev-kit/` with `specs/`, `plans/`, `reports/`, and `.dev-kit/.gitignore` containing `*` (git ignores the whole folder; do not touch the repo's `.gitignore`; `sdd/` comes later), and write `.dev-kit/config.yml` from `${CLAUDE_PLUGIN_ROOT}/templates/config.yml`.
5. **Question: graph indexes** (default: yes; for a large repo state the expected size, about 150 MB for codegraph and 600 MB for code-review-graph per ~3,000 files). On yes, run `codegraph init` and `code-review-graph build`. For each index folder that `git status --porcelain` lists (codegraph keeps its own `.gitignore` visible), append it to `.git/info/exclude`. Set `graph.codegraph` / `graph.crg` in `config.yml`. Build the index before step 7: the standards probe uses it.
6. **Baseline.** Run the test and build commands once. Green → record it. Red → report the counts and main failing groups, then **ask**: stop (fix the baseline first) or accept the current failures as known. If accepted, write `.dev-kit/baseline.md` from `${CLAUDE_PLUGIN_ROOT}/templates/baseline.md`: date, commit, command, totals, and the failing test names, one per line, exactly as the runner prints them. Never fix or skip tests here.
7. **Standards by topic** (below).
8. **Question: `CONSTRAINTS.md`** (optional, default: no), asked on its own after the standards are written, never folded into another question. On yes: `.dev-kit/CONSTRAINTS.md` via part `constraint-driven-development` (`${CLAUDE_PLUGIN_ROOT}/parts/`). If the project has its own `CONSTRAINTS.md`, say that it will be read and skip the question.
9. **Report.** Write `.dev-kit/init-report.md`: found, created, missing, the answers and assumptions, the standards enabled, commands run with output. Compare `git status --porcelain` with step 3: it must be unchanged; fix anything new by adding it to `.git/info/exclude` (never `.gitignore`), or report it.

## Step 7: standards by topic

Rules are written only for what the agent **cannot know by itself** or has been seen to get wrong (principle 0, `docs/en/09-init-and-standards.md`). Never ask about naming or style: the agent reads it from neighbouring code, and the linter checks the rest.

**Probe first, no questions.** Use the graph and the files to find what the code cannot tell a newcomer:
- what the linter and compiler already enforce (reviewers must not report it again);
- in-house libraries: internal-scope packages in `package.json` (old and new versions), how many files import each, template tag prefixes against framework controls (`mat-*` and similar), which one recent files use, and the component list from the package's `public-api.d.ts` / `index.d.ts`;
- central services (`codegraph callers` on the HTTP client or data layer), where permission keys come from, how personal or medical data is handled.

**Then go topic by topic, in this order:** `architecture`, `coding`, `testing`, `security`, `ui`, `api`, `data`, `ops`, `process`. Skip a topic that has neither a kit file fitting the stack nor probe evidence. For each remaining topic, ask **one question** (two at most), built from:
1. **Kit checklist:** the files in `${CLAUDE_PLUGIN_ROOT}/standards/<topic>/`, each with its status and **every item** (ID and a one-line summary), so the user can switch off single items (`<id>#<item>`). `validated` files come pre-ticked, `experimental` files unticked.
2. **Suggested project or team rules, with evidence** from the probe, for example: "68 files use `<ui-…>`, 4 use `mat-input`, recent files use `<ui-…>`: should new code use the in-house controls?" For each rule the user keeps, ask its scope: project or team.
3. **Always the option "add another convention for this topic"** (free text; it costs no question unless chosen).

At most 12 standards questions in total. After the last topic, ask **one open question** (not counted): "Besides the above, does the team or project have other conventions the agent should know?"

**Write, after confirmation.**
- Turn kept suggestions and free-text answers into rule items in `${CLAUDE_PLUGIN_ROOT}/templates/standard.md` format: sort them into topic and scope, one idea per item with an ID, a trigger ("When X, …"), a one-line why and a severity. Say so when an answer breaks principle 0 (the agent already knows it, or a linter checks it) and suggest not writing it.
- **Read the drafted rules back** as their own question and write them only after the user confirms.
- Project rules → `.dev-kit/standards/<topic>/<name>.md`. Team rules → the team folder (`standards.team`): if none is known, ask once for a path (outside the repo, shared however the team likes) and save it to `~/.dev-kit/config.yml` for the next repos. Ticked kit files → `standards.kit`; switched-off kit items → `standards.disable`.
