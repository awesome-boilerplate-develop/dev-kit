---
name: init
description: Set up dev-kit for this machine and repo. Use once before first using dev-kit controllers, or to re-check the setup.
---

# init

**Harness.** Written for Claude Code, which replaces the plugin-root variable below with the dev-kit folder. If you see `${CLAUDE_PLUGIN_ROOT}` literally, your harness did not replace it: the dev-kit folder is two levels above this SKILL.md after resolving symlinks (the folder that contains `rules/RULES.md`). Read every `${CLAUDE_PLUGIN_ROOT}/…` below as a path in that folder, and first read `harness/<your harness>.md` there (`codex`, `copilot`, `cursor`, `opencode`, `antigravity`, `omp`): it maps `dk:<skill>`, subagents and the review agents to your tools.

Prepare, never run controller logic. Re-running only checks and fills gaps; never overwrite existing files. dev-kit is personal (rule O1): nothing it creates is committed, and it never edits a tracked file.

First print **one plan with defaults** and wait for a single approval: what will be created or run, the graph indexes (with the expected size for a large repo), and the optional `CONSTRAINTS.md` (default: no). The user approves as is or names what to change; ask a separate question only when a step below says so (a missing tool, a red baseline).

1. Machine: check `git`, `gh`, `make`; check the graph tools with `bash ${CLAUDE_PLUGIN_ROOT}/scripts/install-graph-tools.sh --check`. List enabled plugins (they add context to every session) and remind the user to invoke `dk:<controller>` by name (plugin skills are namespaced, so there is no name clash).
   - If a graph tool is missing, say so in the plan and ask once whether to install it. On yes, run `bash ${CLAUDE_PLUGIN_ROOT}/scripts/install-graph-tools.sh --install` (pinned versions; tools already present are left alone) and show its final status lines. On no, continue and note "rule G1 off: <tool> not installed" in the report — everything else works the same.
   - Never run `codegraph install` or `code-review-graph install` yourself: they register MCP servers, hooks and instruction files. dev-kit uses the CLI only.
2. Detect test/lint/build commands from `Makefile`, `package.json`, `pyproject.toml`; show them in the plan; write `.dev-kit/config.yml` from `${CLAUDE_PLUGIN_ROOT}/templates/config.yml` (`base_branch`, `commands`, `tracker`, `graph`).
3. Create `.dev-kit/` with `specs/`, `plans/`, `reports/`, and `.dev-kit/.gitignore` containing `*` so git ignores the whole folder, the `.gitignore` included (`sdd/` is created later by subagent-driven development). Do not ask what to commit and do not touch the repo's `.gitignore`. If the repo already tracks files under `.dev-kit/`, report them and leave them alone.
4. Optional, only if the user asked for it in the plan: `.dev-kit/CONSTRAINTS.md` via part `constraint-driven-development` (`${CLAUDE_PLUGIN_ROOT}/parts/`). If the repo has its own `CONSTRAINTS.md`, read it instead and do not create one.
5. Graph indexes, **on by default**: `codegraph init` (adds `.codegraph/`) and `code-review-graph build` (adds `.code-review-graph/`). Never edit the repo's `.gitignore`. Each tool writes a `.gitignore` in its folder, but codegraph's keeps itself visible (`!.gitignore`), so the folder can still show in git: for each index folder that `git status --porcelain` lists, append it (`.codegraph/`, `.code-review-graph/`) to `.git/info/exclude`, which is local and never pushed. For a large repo (thousands of files) the plan states the expected size — about 150 MB for codegraph and 600 MB for code-review-graph per ~3,000 files. Set `graph.codegraph` / `graph.crg` in `config.yml`.
6. Baseline: run the test and build commands once.
   - Green → record it in the report.
   - Red → report the counts and the main failing groups, then ask the user: **stop** (fix the baseline first) or **accept the current failures as known**. If accepted, write `.dev-kit/baseline.md` from `${CLAUDE_PLUGIN_ROOT}/templates/baseline.md`: date, commit, command, totals, and the list of failing test names (one per line, exactly as the runner prints them). Never fix or skip tests here.
7. Write `.dev-kit/init-report.md`: found, created, missing, commands run with output. Compare `git status --porcelain` with its output before step 1: it must be unchanged. Anything new is a bug to fix by adding the path to `.git/info/exclude` (never `.gitignore`) or to report.
