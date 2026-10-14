---
name: init
description: Set up dev-kit for this machine and repo. Use once before first using dev-kit controllers, or to re-check the setup.
---

# init

**Harness.** Written for Claude Code, which replaces the plugin-root variable below with the dev-kit folder. If you see `${CLAUDE_PLUGIN_ROOT}` literally, your harness did not replace it: the dev-kit folder is two levels above this SKILL.md after resolving symlinks (the folder that contains `rules/RULES.md`). Read every `${CLAUDE_PLUGIN_ROOT}/…` below as a path in that folder, and first read `harness/<your harness>.md` there (`codex`, `copilot`, `cursor`, `opencode`, `antigravity`, `omp`): it maps `dk:<skill>`, subagents and the review agents to your tools.

Prepare, never run controller logic. Re-running only checks and fills gaps; never overwrite existing files. First print the plan (what will be created or run) and wait for approval.

1. Machine: check `git`, `gh`, `make`; check the graph tools with `bash ${CLAUDE_PLUGIN_ROOT}/scripts/install-graph-tools.sh --check`. List enabled plugins (they add context to every session) and remind the user to invoke `dk:<controller>` by name (plugin skills are namespaced, so there is no name clash).
   - If a graph tool is missing, say so in the plan and ask once whether to install it. On yes, run `bash ${CLAUDE_PLUGIN_ROOT}/scripts/install-graph-tools.sh --install` (pinned versions; tools already present are left alone) and show its final status lines. On no, continue and note "rule G1 off: <tool> not installed" in the report — everything else works the same.
   - Never run `codegraph install` or `code-review-graph install` yourself: they register MCP servers, hooks and instruction files. dev-kit uses the CLI only.
2. Detect test/lint/build commands from `Makefile`, `package.json`, `pyproject.toml`; confirm with the user; write `.dev-kit/config.yml` from `${CLAUDE_PLUGIN_ROOT}/templates/config.yml` (`base_branch`, `commands`, `tracker`, `graph`).
3. Create `.dev-kit/` with `specs/`, `plans/`, `reports/` (`sdd/` is created later by subagent-driven development and ignores itself). Ask which parts to commit; suggest committing `config.yml` and `specs/`.
4. Optional: `CONSTRAINTS.md` via part `constraint-driven-development` (`${CLAUDE_PLUGIN_ROOT}/parts/`).
5. Graph indexes, **on by default** (they are part of the plan the user approves; skip only if the user says no or the tool is missing): `codegraph init` (adds `.codegraph/`) and `code-review-graph build` (adds `.code-review-graph/`). For a large repo (thousands of files) state the expected size first — about 150 MB for codegraph and 600 MB for code-review-graph per ~3,000 files — and ask. Add both directories to `.gitignore`; set `graph.codegraph` / `graph.crg` in `config.yml`.
6. Baseline: run the test and build commands once.
   - Green → record it in the report.
   - Red → report the counts and the main failing groups, then ask the user: **stop** (fix the baseline first) or **accept the current failures as known**. If accepted, write `.dev-kit/baseline.md` from `${CLAUDE_PLUGIN_ROOT}/templates/baseline.md`: date, commit, command, totals, and the list of failing test names (one per line, exactly as the runner prints them). Never fix or skip tests here.
7. Write `.dev-kit/init-report.md`: found, created, missing, commands run with output.
