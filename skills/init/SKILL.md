---
name: init
description: Sets up dev-kit for this machine and repo, including the standards checklist by topic. Use once before first using dev-kit controllers, to re-check the setup, or to re-run one part (index, baseline, standards). Not for working a card (use the dk controllers for that).
---

# init

## Before you start

**Harness.** Written for Claude Code, which replaces the plugin-root variable below with the dev-kit folder. If you see `${CLAUDE_PLUGIN_ROOT}` literally, your harness did not replace it: the dev-kit folder is two levels above this SKILL.md after resolving symlinks (the folder that contains `rules/RULES.md`). Read every `${CLAUDE_PLUGIN_ROOT}/…` below as a path in that folder, and first read `harness/<your harness>.md` there (`codex`, `copilot`, `opencode`, `antigravity`, `omp`): it maps `dk:<skill>`, subagents and the review agents to your tools.

Prepare, never run controller logic. Re-running only checks and fills gaps; never overwrite existing files. dev-kit is personal (rule O1): nothing it creates is committed, and it never edits a tracked file.

**Parts of a run.** `dk:init` runs everything below. `dk:init index` runs step 5 only (for example in a new worktree), `dk:init baseline` step 6 (the known-failure list may only shrink), `dk:init standards [rules|review]` step 7 (both passes, or the one named), asking the quick-or-detailed question of step 5 first.

## How to ask

**How to ask: probe first, then one question at a time, in order.** Before each question, find out what you can from the code, the graph and the files, and show that evidence with the question. Ask **one question per message**, in the order of the steps below, each with a default and short options, and wait for the answer before moving on. Number them ("Question 3 — commands"). "default" and "skip" are always valid answers. Never ask what the code already answers, and never batch questions. Ask only the questions the steps name: never ask permission to run a step or to continue (the baseline runs without asking; after an answer, go straight to the next step). If nobody can answer (headless run), take the defaults and list them as assumptions in the report.

**Every question ends with choices plus Other.** After the evidence, list lettered choices, at most 4:
- `A` is the recommended answer, marked "(Recommended)" and spelled out in full, so the user sees exactly what it does (for example "A. (Recommended) base `release-2`, test `npm run test-headless`, build `npm run build`, no lint");
- `B`, `C`, `D` are the real alternatives (another branch, "skip", "stop"); no filler choices;
- the last line is always "Other: type your own answer" (a change, a value, item IDs, free text).

**A choice that names item IDs explains them.** Write what each ID is in a few words, in the label or its description, for the IDs kept and for the IDs switched off: "Keep U2 (block a write while one is in flight); off: U1 error messages, U3 loading and error states, U4 reset after a write, U5 labels and keyboard", never "Keep U2, turn off U1/U3/U4/U5". When the tool shows its question text, put the group's items there too, one per line (ID and a few words). The user must be able to choose from the form alone.

"default" or Enter means `A`. If your harness gives you a tool that asks the user with choices (Antigravity `ask_question`, Copilot `ask_user`, omp `ask`), use it with the same choices, `A` first with its "(Recommended)" label; add "Other" as a choice only if the tool does not offer free text itself. If the tool comes back skipped or empty (a headless run auto-skips it), nobody can answer: take `A` and list it as an assumption, as for any headless run; do not ask the same question again. Without such a tool, write the choices as text. Never end a question with only "type default or a value".

**The tool is only the last line of the question, never the whole question.** Before calling it, write a normal reply the user can read on screen with everything the step asks you to show: the evidence, the group's list in detail (every item: what it asks, why, where this repo hits it, with counts), the drafted items of a read-back, the explanation the `CONSTRAINTS.md` step requires, and the "how it fits this repo" part of a confirmation. A choice label is a short summary of that reply, not a replacement for it. Your reasoning does not count as a reply: text that appears only in a thinking block or a tool log is not seen by the user (in one run the agent wrote the evaluation of three kit groups in a row only as reasoning, and the user saw forms like "Keep U2, turn off U1/U3/U4/U5" with no idea what those IDs were). This holds for every group of a run, the last as much as the first.

## Machine (skipped when already done)

1. **Graph tools.** Run `bash ${CLAUDE_PLUGIN_ROOT}/scripts/install-graph-tools.sh --check`. Only if a tool is missing, **ask** whether to install it (default: yes). On yes, run `bash ${CLAUDE_PLUGIN_ROOT}/scripts/install-graph-tools.sh --install` (pinned versions; tools already present are left alone) and use the absolute path it prints if the tool is not on PATH. On no, continue and note "rule G1 off: <tool> not installed". Never run `codegraph install` or `code-review-graph install`: they register MCP servers, hooks and instruction files.
2. **Personal settings.** None for now: dev-kit is set up one repo at a time, and every standard `dk:init` writes belongs to this repo. Standards shared across repos (`standards.team`) are not offered yet; a path the user sets there by hand is still loaded by the controllers.

## Repo

3. **Probe, no questions.** Record `git status --porcelain`. Detect the test/lint/build commands (`Makefile`, `package.json`, `pyproject.toml`, …), the stack, the linters and type checkers with their configs (what they already enforce), files the repo already tracks under `.dev-kit/`, and the project's own `GLOSSARY.md`, `docs/adr/`, `CONSTRAINTS.md`. List the enabled plugins and remind the user to invoke `dk:<controller>` by name.
   - **Base branch:** `origin/HEAD` alone is not enough (it can point at a branch nobody merges into any more). Compare it with the remote branch that recent pull requests merge into (the newest merge commits, such as "Merged PR …", across `refs/remotes`) and with the current branch's upstream; for each candidate note its last commit date and how many commits it is ahead of the others. If they agree, propose that branch; if not, step 4 asks it as a choice with that evidence.
4. **Question: commands and base branch.** Show what you detected; the user confirms or corrects. Then create `.dev-kit/` with `specs/`, `plans/`, `reports/`, and `.dev-kit/.gitignore` containing `*` (git ignores the whole folder; do not touch the repo's `.gitignore`; `sdd/` comes later), and write `.dev-kit/config.yml` from `${CLAUDE_PLUGIN_ROOT}/templates/config.yml`.
5. **Question: graph indexes** (default: yes). State the expected size from the number of code files the tools will index: count source code only (`.ts`, `.js`, `.py`, `.cs`, `.go`, `.java`, … tracked by git), not templates, styles, assets or dependencies; about 0.16 MB per file for codegraph and 0.6 MB per file for code-review-graph (measured: 136 MB and 529 MB for ~850 indexed files, in a repo with ~1,450 files under `src/`). On yes, run `codegraph init` and `code-review-graph build`, then fix `git status` in this step, not later: the repo's exclude file is `git rev-parse --path-format=absolute --git-path info/exclude` (in a worktree `.git` is a file, and the exclude file is shared by every worktree of the repo); append to it each index folder that `git status --porcelain` now lists (codegraph keeps its own `.gitignore` visible, so `?? .codegraph/` appears and `.codegraph/` must be added), never `.dev-kit/` (its own `.gitignore` already hides it), and never a line that is already there; then check `git status --porcelain` is back to what step 3 recorded. Set `graph.codegraph` / `graph.crg` in `config.yml`. Build the index before step 7: the standards probe uses it.
   - **Question: quick or detailed setup** for the standards (step 7) and `CONSTRAINTS.md` (step 8), asked right after the indexes, in a full run and at the start of `dk:init standards`; not in `dk:init index`. Choices: `A` quick (Recommended): the agent probes and drafts every group as in detailed mode, takes each Recommended line itself, and asks once, with one read-back of everything it will write (see `references/quick-setup.md`); `B` detailed: one question per group, with the loops for the user's own conventions; Other. The baseline question of step 6 is still asked when the tests are red, in both modes: stopping to fix tests is the user's call.
6. **Baseline.** Run the test and build commands once, writing their output to `.dev-kit/baseline-test.log` and `.dev-kit/baseline-build.log` (never a shared folder such as `/tmp`); take counts, failing groups and failing test names from those files, never by running the suite again. Green → record it. Red → report the counts and main failing groups, then **ask**: stop (fix the baseline first) or accept the current failures as known. If accepted, write `.dev-kit/baseline.md` from `${CLAUDE_PLUGIN_ROOT}/templates/baseline.md`: date, commit, command, totals, and the failing test names, one per line, exactly as the runner prints them. Never fix or skip tests here. **Tests could not run** (restore, authentication, missing service or toolchain) is not a red baseline: report the error and **ask**: stop and fix the environment, or continue with the baseline marked "not measured" in `config.yml` and the report (controllers then treat every test failure as new until `dk:init baseline` succeeds).
7. **Standards by topic.** Read in full and follow, from `${CLAUDE_PLUGIN_ROOT}/skills/init/references/`: `standards-interview.md` (probe, groups, pass 1, pass 2) always; `quick-setup.md` in quick setup or a headless run; `writing-standards.md` before writing any standards file.
8. **Question: `CONSTRAINTS.md`** (optional, default: no), asked on its own after the standards are written, never folded into another question; in quick setup it is not asked (default no, said in the read-back). If the project has its own `CONSTRAINTS.md`, say that it will be read and skip the question. Otherwise Read `${CLAUDE_PLUGIN_ROOT}/skills/init/references/constraints-question.md` and ask it as written there.

   On yes: write `.dev-kit/CONSTRAINTS.md` via part `constraint-driven-development` (`${CLAUDE_PLUGIN_ROOT}/parts/`), keeping its one-question-at-a-time interview.
9. **Report.** Write `.dev-kit/init-report.md`: found, created, missing, the answers and assumptions, the standards enabled, commands run with output. Compare `git status --porcelain` with step 3: it must be unchanged; fix anything new by adding it to the exclude file from step 5 (never `.gitignore`), or report it. Say a line was added to the exclude file only if you ran the command that added it in this run, and quote that command.

## Related files

Run, do not read:
- `${CLAUDE_PLUGIN_ROOT}/scripts/install-graph-tools.sh` — step 1, `--check` then `--install`.
- `${CLAUDE_PLUGIN_ROOT}/scripts/check_standards.py` — after writing standards (see `references/writing-standards.md`).

Read when the step says:
- `references/standards-interview.md` — step 7 and `dk:init standards`, always: probe, how each group is asked, pass 1, pass 2.
- `references/quick-setup.md` — step 7, only in quick setup or a headless run: the ticked checklist and the tick forms.
- `references/writing-standards.md` — before writing any standards file: IDs, where items go, `check_standards.py`.
- `references/constraints-question.md` — step 8, only when the question is asked: what the question must explain.

Copy, fill in:
- `${CLAUDE_PLUGIN_ROOT}/templates/config.yml` — step 4.
- `${CLAUDE_PLUGIN_ROOT}/templates/baseline.md` — step 6, when the user accepts a red baseline.
- `${CLAUDE_PLUGIN_ROOT}/templates/standard.md` — step 7, the format of every standards file.
