---
name: code-refactor
description: Restructure code without changing behavior. Use when a tech-debt card asks to split or move modules.
---

# code-refactor

## Before you start

**Harness.** Written for Claude Code, which replaces the plugin-root variable below with the dev-kit folder. If you see `${CLAUDE_PLUGIN_ROOT}` literally, your harness did not replace it: the dev-kit folder is two levels above this SKILL.md after resolving symlinks (the folder that contains `rules/RULES.md`). Read every `${CLAUDE_PLUGIN_ROOT}/…` below as a path in that folder, and first read `harness/<your harness>.md` there (`codex`, `copilot`, `opencode`, `antigravity`, `omp`): it maps `dk:<skill>`, subagents and the review agents to your tools.

**Parts.** Steps name *parts*: playbooks at `${CLAUDE_PLUGIN_ROOT}/parts/<name>/SKILL.md` (absolute path). Read a part only when a step names it; relative paths inside a part resolve against that part's folder, so `../../rules/…` inside a part means `${CLAUDE_PLUGIN_ROOT}/rules/…`. Parts are not skills.

**Rules.** Apply the rules marked **on** in `${CLAUDE_PLUGIN_ROOT}/rules/RULES.md` (F1 flow ownership, F2 finish in this turn, C1 direct path, C2 review depth, G1 graph tools, T1 standards, S1 severity scale, O1 output home).

**Commands.** If `.dev-kit/config.yml` exists (written by `dk:init`), use its `commands.check` (else `commands.test`) and `base_branch` in place of `make check` and `main` below; otherwise `make check` or the repo's documented test command, and `main`. If `.dev-kit/baseline.md` lists known failures, a check passes when no test fails outside that list; report new failures as blockers and newly passing tests separately.

**Graph (rule G1).** If `.codegraph/` or `.code-review-graph/` exists, follow `${CLAUDE_PLUGIN_ROOT}/rules/graph-playbook.md`: §1 once per session, then the sections the steps name. Summaries only (`jq -r '.summary'`). No index → skip.

**Standards (rule T1).** Load the standards that apply: kit files listed in `.dev-kit/config.yml` → `standards.kit` (each `<id>` is `${CLAUDE_PLUGIN_ROOT}/standards/<id>.md`), every `*.md` under the team folder `standards.team` and under `.dev-kit/standards/`; skip ids in `standards.disable`, and skip files whose `applies_to` matches none of the files you will touch. On conflict: project > team > kit. While planning apply `## Design`; while writing code apply `## Implement`. List the standards you applied in the report. An id in `standards.kit` or `standards.disable` that matches no file (a renamed or removed kit file) is named under the standards in the report, not skipped silently. No config or no files → skip.

## Output

**Outputs** (rule O1). Everything this skill writes goes under `.dev-kit/`. Finish with `.dev-kit/reports/<short-name>.md` filled from `${CLAUDE_PLUGIN_ROOT}/templates/report.md`; keep it short, it is for a human reader. Severities use the dev-kit scale `blocker` / `major` / `minor` (rule S1). Run subagents in the foreground and wait for them in this turn; never schedule wakeups, loops or background waits (rule F2). End the final reply with: what was done, the verdict, and the report path.

## Steps

### 1. New interface
Decide the new interface (Read part `codebase-design` if the boundary is unclear).
- With G1: playbook §3 for what you will move (record the blast radius in the report); §5 large-functions if the target is not yet chosen.

### 2. Characterization tests
Characterization tests at the public interface first (G1: playbook §5 — every public symbol you move without tests gets one), pinning current behaviour for any input — including behaviour that looks wrong (record it in the report as a suspected bug; never fix it here).

### 3. Move in small steps
Rule C1 (G1: playbook §5 rename preview lists every edit site; check dead code before deleting):
- move code in small steps here, check after each, commit each step;
- large work → the SDD parts as in story-runner.

### 4. Pre-PR check
Run skill `dk:pre-pr-check`.
