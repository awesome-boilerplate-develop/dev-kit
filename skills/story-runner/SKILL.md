---
name: story-runner
description: Deliver a feature/story card. Use when a kanban story must be clarified, implemented with tests and checked.
---

# story-runner

**Harness.** Written for Claude Code, which replaces the plugin-root variable below with the dev-kit folder. If you see `${CLAUDE_PLUGIN_ROOT}` literally, your harness did not replace it: the dev-kit folder is two levels above this SKILL.md after resolving symlinks (the folder that contains `rules/RULES.md`). Read every `${CLAUDE_PLUGIN_ROOT}/…` below as a path in that folder, and first read `harness/<your harness>.md` there (`codex`, `copilot`, `opencode`, `antigravity`, `omp`): it maps `dk:<skill>`, subagents and the review agents to your tools.

**Parts.** Steps name *parts*: playbooks at `${CLAUDE_PLUGIN_ROOT}/parts/<name>/SKILL.md` (absolute path). Read a part only when a step names it; relative paths inside a part resolve against that part's folder, so `../../rules/…` inside a part means `${CLAUDE_PLUGIN_ROOT}/rules/…`. Parts are not skills.

**Rules.** Apply the rules marked **on** in `${CLAUDE_PLUGIN_ROOT}/rules/RULES.md` (F1 flow ownership, F2 finish in this turn, C1 direct path, C2 review depth, G1 graph tools, T1 standards, S1 severity scale, O1 output home).

**Commands.** If `.dev-kit/config.yml` exists (written by `dk:init`), use its `commands.check` (else `commands.test`) and `base_branch` in place of `make check` and `main` below; otherwise `make check` or the repo's documented test command, and `main`. If `.dev-kit/baseline.md` lists known failures, a check passes when no test fails outside that list; report new failures as blockers and newly passing tests separately.

**Graph (rule G1).** If `.codegraph/` or `.code-review-graph/` exists, follow `${CLAUDE_PLUGIN_ROOT}/rules/graph-playbook.md`: §1 once per session, then the sections the steps name. Summaries only (`jq -r '.summary'`). No index → skip.

**Standards (rule T1).** Load the standards that apply: kit files listed in `.dev-kit/config.yml` → `standards.kit` (each `<id>` is `${CLAUDE_PLUGIN_ROOT}/standards/<id>.md`), every `*.md` under the team folder `standards.team` and under `.dev-kit/standards/`; skip ids in `standards.disable`, and skip files whose `applies_to` matches none of the files you will touch. On conflict: project > team > kit. While planning apply `## Design`; while writing code apply `## Implement`. List the standards you applied in the report. An id in `standards.kit` or `standards.disable` that matches no file (a renamed or removed kit file) is named under the standards in the report, not skipped silently. No config or no files → skip.

**Outputs** (rule O1). Everything this skill writes goes under `.dev-kit/`. Finish with `.dev-kit/reports/<short-name>.md` filled from `${CLAUDE_PLUGIN_ROOT}/templates/report.md`; keep it short, it is for a human reader. Severities use the dev-kit scale `blocker` / `major` / `minor` (rule S1). Run subagents in the foreground and wait for them in this turn; never schedule wakeups, loops or background waits (rule F2). End the final reply with: what was done, the verdict, and the report path.

1. If the card is ambiguous, Read part `grilling` and resolve the questions with the user, one at a time. If the story introduces new domain terms, also Read part `domain-modeling`. When no one can answer (headless run), choose the most reasonable option and mark it as an assumption.
2. Write the spec to `.dev-kit/specs/<feature>.md` from `${CLAUDE_PLUGIN_ROOT}/templates/spec.md` (goal, rules, interface, acceptance criteria, out of scope, **Decisions**: each question, the answer, decided by user or "assumption").
3. Rule C1 (G1: playbook §2/§3 when the story changes existing code; §6 for large work): small work → implement here, test first, commit per behaviour. Large work → parts `writing-plans`, `using-git-worktrees`, `subagent-driven-development`, `finishing-a-development-branch` (merge back locally, no push/PR).
4. Run skill `dk:pre-pr-check`.
