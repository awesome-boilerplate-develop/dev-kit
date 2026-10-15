---
name: pre-pr-check
description: Final gate before a PR. Use when a branch is finished and must be verified and reviewed against main.
---

# pre-pr-check

**Harness.** Written for Claude Code, which replaces the plugin-root variable below with the dev-kit folder. If you see `${CLAUDE_PLUGIN_ROOT}` literally, your harness did not replace it: the dev-kit folder is two levels above this SKILL.md after resolving symlinks (the folder that contains `rules/RULES.md`). Read every `${CLAUDE_PLUGIN_ROOT}/…` below as a path in that folder, and first read `harness/<your harness>.md` there (`codex`, `copilot`, `opencode`, `antigravity`, `omp`): it maps `dk:<skill>`, subagents and the review agents to your tools.

**Parts.** Steps name *parts*: playbooks at `${CLAUDE_PLUGIN_ROOT}/parts/<name>/SKILL.md` (absolute path). Read a part only when a step names it; relative paths inside a part resolve against that part's folder, so `../../rules/…` inside a part means `${CLAUDE_PLUGIN_ROOT}/rules/…`. Parts are not skills.

**Rules.** Apply the rules marked **on** in `${CLAUDE_PLUGIN_ROOT}/rules/RULES.md` (F1 flow ownership, F2 finish in this turn, C1 direct path, C2 review depth, G1 graph tools, R1 finding quality, T1 standards, S1 severity scale, O1 output home).

**Commands.** If `.dev-kit/config.yml` exists (written by `dk:init`), use its `commands.check` (else `commands.test`) and `base_branch` in place of `make check` and `main` below; otherwise `make check` or the repo's documented test command, and `main`. If `.dev-kit/baseline.md` lists known failures, a check passes when no test fails outside that list; report new failures as blockers and newly passing tests separately.

**Graph (rule G1).** If `.codegraph/` or `.code-review-graph/` exists, follow `${CLAUDE_PLUGIN_ROOT}/rules/graph-playbook.md`: §1 once per session, then the sections the steps name. Summaries only (`jq -r '.summary'`). No index → skip.

**Standards (rule T1).** Load the standards that apply: kit files listed in `.dev-kit/config.yml` → `standards.kit` (each `<id>` is `${CLAUDE_PLUGIN_ROOT}/standards/<id>.md`), every `*.md` under the team folder `standards.team` and under `.dev-kit/standards/`; skip ids in `standards.disable`, and skip files whose `applies_to` matches none of the files you will touch. On conflict: project > team > kit. While planning apply `## Design`; while writing code apply `## Implement`. List the standards you applied in the report. An id in `standards.kit` or `standards.disable` that matches no file (a renamed or removed kit file) is named under the standards in the report, not skipped silently. No config or no files → skip.

**Outputs** (rule O1). Everything this skill writes goes under `.dev-kit/`. Finish with `.dev-kit/reports/<short-name>.md` filled from `${CLAUDE_PLUGIN_ROOT}/templates/report.md`; keep it short, it is for a human reader. Severities use the dev-kit scale `blocker` / `major` / `minor` (rule S1). Run subagents in the foreground and wait for them in this turn; never schedule wakeups, loops or background waits (rule F2). End the final reply with: what was done, the verdict, and the report path.

**Mode.** If the request says not to change code, run *report-only*: never edit files, skip step 5.

1. Run the check command now; keep the output as Evidence. Look at `git diff main...HEAD` for a lowered bar: new skips, suppressions, deleted asserts, weakened thresholds. If `.dev-kit/CONSTRAINTS.md` (or the project's own `CONSTRAINTS.md`) exists, also check the diff against its floor and numbered rules; a change that breaks one is a blocker.
2. **Graph first.** Check `test -d "$(git rev-parse --show-toplevel)/.code-review-graph"`; do not infer it from other listings. If it exists (rule G1): playbook §1, then §7 `detect-changes --brief --base main`. Keep the summary (risk score, test gaps, untested functions); it is a required input for every reviewer. The command errors → write "detect-changes failed: <error>" in Review setup. No index → write "no .code-review-graph/ index". `check_report.py` rejects "no index" when the directory exists.
3. **Review depth (rule C2), from numbers.** Run `git diff --shortstat main...HEAD` and list the touched files; pick the depth from those numbers and C2's triggers, not from impression. **Never lower the depth to save cost**; if you think a lower depth is enough, ask the user.
   - *Self-review*: Read part `code-review` and apply both axes yourself (its self-review mode: no sub-agents).
   - *One reviewer*: one general-purpose subagent told to Read part `code-review` and act in the reviewer role "both axes".
   - *Four reviewers* (one turn, in parallel): two general-purpose subagents with part `code-review` in the roles "Standards axis only" and "Spec axis only", plus `dk:security-auditor` and `dk:test-engineer`.

   Every reviewer (and you, in self-review) gets: the diff range, the spec (`.dev-kit/specs/…` or the issue text), the step-2 graph summary, `${CLAUDE_PLUGIN_ROOT}/standards/review/finding-quality.md` (rule R1), and the loaded standards (rule T1) whose `topic` belongs to its role, as paths, with the instruction to apply their `## Review`, `## Do not flag` and `## Severity` sections and cite rule ids:
   - Standards reviewer: coding, architecture, process · Spec reviewer: api, ui, data · `dk:security-auditor`: security · `dk:test-engineer`: testing.
   - One reviewer or self-review: all loaded topics. Reviewers return findings as `file:line | severity | confidence 0–100 | when it happens | rule id or — | finding`.
4. **Merge and gate.** Deduplicate by location and defect. Drop findings that fail any condition of `finding-quality` (R1–R7) or have confidence < 50. Split the rest into **certain** (≥ 80) and **suspect** (50–79). Map other severity labels with rule S1. Any open certain `blocker` → `Verdict: NO-GO`; otherwise `Verdict: GO`.
5. Certain blockers: Read part `receiving-code-review`, fix with evidence (or push back with reasons), back to step 1 (max 2 rounds).
6. Report from the template, including the required **Review setup** section. Then run `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/check_report.py <report path> --base main` from the repo root; if it prints FAIL lines, fix the report (move, drop or re-tier findings; fix the verdict) and run it again until it prints OK (at most 3 tries; if still failing, say so in the final reply). unless report-only, a PR body in `.dev-kit/reports/pr-body.md`, following part `pr` (Summary / Evidence / Merge Danger; Evidence = the check output from step 1).
