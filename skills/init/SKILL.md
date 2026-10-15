---
name: init
description: Set up dev-kit for this machine and repo, including the standards checklist by topic. Use once before first using dev-kit controllers, to re-check the setup, or to re-run one part (index, baseline, standards).
---

# init

**Harness.** Written for Claude Code, which replaces the plugin-root variable below with the dev-kit folder. If you see `${CLAUDE_PLUGIN_ROOT}` literally, your harness did not replace it: the dev-kit folder is two levels above this SKILL.md after resolving symlinks (the folder that contains `rules/RULES.md`). Read every `${CLAUDE_PLUGIN_ROOT}/…` below as a path in that folder, and first read `harness/<your harness>.md` there (`codex`, `copilot`, `opencode`, `antigravity`, `omp`): it maps `dk:<skill>`, subagents and the review agents to your tools.

Prepare, never run controller logic. Re-running only checks and fills gaps; never overwrite existing files. dev-kit is personal (rule O1): nothing it creates is committed, and it never edits a tracked file.

**Parts of a run.** `dk:init` runs everything below. `dk:init index` runs step 5 only (for example in a new worktree), `dk:init baseline` step 6 (the known-failure list may only shrink), `dk:init standards [rules|review]` step 7 (both passes, or the one named).

**How to ask: probe first, then one question at a time, in order.** Before each question, find out what you can from the code, the graph and the files, and show that evidence with the question. Ask **one question per message**, in the order of the steps below, each with a default and short options, and wait for the answer before moving on. Number them ("Question 3 — commands"). "default" and "skip" are always valid answers. Never ask what the code already answers, and never batch questions. If nobody can answer (headless run), take the defaults and list them as assumptions in the report.

## Machine (skipped when already done)

1. **Graph tools.** Run `bash ${CLAUDE_PLUGIN_ROOT}/scripts/install-graph-tools.sh --check`. Only if a tool is missing, **ask** whether to install it (default: yes). On yes, run `bash ${CLAUDE_PLUGIN_ROOT}/scripts/install-graph-tools.sh --install` (pinned versions; tools already present are left alone) and use the absolute path it prints if the tool is not on PATH. On no, continue and note "rule G1 off: <tool> not installed". Never run `codegraph install` or `code-review-graph install`: they register MCP servers, hooks and instruction files.
2. **Personal settings.** Read `~/.dev-kit/config.yml` if it exists (the team standards folder chosen in an earlier repo). Write it only in step 7, when the user names a team folder.

## Repo

3. **Probe, no questions.** Record `git status --porcelain`. Detect the test/lint/build commands (`Makefile`, `package.json`, `pyproject.toml`, …), the base branch, the stack, the linters and type checkers with their configs (what they already enforce), files the repo already tracks under `.dev-kit/`, and the project's own `GLOSSARY.md`, `docs/adr/`, `CONSTRAINTS.md`. List the enabled plugins and remind the user to invoke `dk:<controller>` by name.
4. **Question: commands and base branch.** Show what you detected; the user confirms or corrects. Then create `.dev-kit/` with `specs/`, `plans/`, `reports/`, and `.dev-kit/.gitignore` containing `*` (git ignores the whole folder; do not touch the repo's `.gitignore`; `sdd/` comes later), and write `.dev-kit/config.yml` from `${CLAUDE_PLUGIN_ROOT}/templates/config.yml`.
5. **Question: graph indexes** (default: yes; for a large repo state the expected size, about 150 MB for codegraph and 600 MB for code-review-graph per ~3,000 files). On yes, run `codegraph init` and `code-review-graph build`. For each index folder that `git status --porcelain` lists (codegraph keeps its own `.gitignore` visible), append it to `.git/info/exclude`. Set `graph.codegraph` / `graph.crg` in `config.yml`. Build the index before step 7: the standards probe uses it.
6. **Baseline.** Run the test and build commands once. Green → record it. Red → report the counts and main failing groups, then **ask**: stop (fix the baseline first) or accept the current failures as known. If accepted, write `.dev-kit/baseline.md` from `${CLAUDE_PLUGIN_ROOT}/templates/baseline.md`: date, commit, command, totals, and the failing test names, one per line, exactly as the runner prints them. Never fix or skip tests here. **Tests could not run** (restore, authentication, missing service or toolchain) is not a red baseline: report the error and **ask**: stop and fix the environment, or continue with the baseline marked "not measured" in `config.yml` and the report (controllers then treat every test failure as new until `dk:init baseline` succeeds).
7. **Standards by topic** (below).
8. **Question: `CONSTRAINTS.md`** (optional, default: no), asked on its own after the standards are written, never folded into another question. If the project has its own `CONSTRAINTS.md`, say that it will be read and skip the question. Otherwise the question must explain itself, in the user's language, filled in with what step 3 found:
   - **What it is:** a written quality bar for *how good a change must be before it ships*, as numbers, each with the command that checks it (for example "zero type errors: `tsc --noEmit`", "changed lines ≥ 80% covered", "no high security findings: `semgrep`"), plus a floor that always applies (no new suppressions such as `@ts-ignore`, no stubs, no skipped or deleted tests, no secrets) and a list of agreed exceptions.
   - **How it differs from the standards just chosen:** standards say *how code in this repo is written* (rules the agent cannot guess, used while coding and reviewing); `CONSTRAINTS.md` sets the *pass bar and the tools that measure it*, and exists so the agent cannot quietly lower the bar to get green.
   - **What the user already has without it:** `dk:pre-pr-check` already flags new skips, suppressions, deleted asserts and weakened thresholds in the diff; list the checks the repo already runs (type checker, linter, coverage, CI gates) from step 3.
   - **What it would add here:** the dimensions that are missing from that list (for example "no linter and no coverage gate today").
   - **Cost:** up to 4 more questions (which dimensions, block or warn, target numbers or "measure today and hold", slowest acceptable check); possibly installing a tool, always asked first; its benefit has not been measured in the dev-kit lab.
   - **Where and who reads it:** `.dev-kit/CONSTRAINTS.md`, personal and never committed; `dk:pre-pr-check` step 1 reads it, and a change that breaks it is a blocker.
   - **Answer:** "no" (default; nothing is lost, the floor checks above still run) or "yes".

   On yes: write `.dev-kit/CONSTRAINTS.md` via part `constraint-driven-development` (`${CLAUDE_PLUGIN_ROOT}/parts/`), keeping its one-question-at-a-time interview.
9. **Report.** Write `.dev-kit/init-report.md`: found, created, missing, the answers and assumptions, the standards enabled, commands run with output. Compare `git status --porcelain` with step 3: it must be unchanged; fix anything new by adding it to `.git/info/exclude` (never `.gitignore`), or report it.

## Step 7: standards in two passes

Rules are written only for what the agent **cannot know by itself** or has been seen to get wrong (principle 0, `docs/en/09-init-and-standards.md`). Never ask about naming or style: the agent reads it from neighbouring code, and the linter checks the rest.

**Probe first, no questions.** Use the graph and the files to find what the code cannot tell a newcomer:
- what the linter and compiler already enforce (reviewers must not report it again);
- the structure: layers and folders with file counts, how data is reached (`codegraph callers` on the HTTP client or data layer), the module system, what the repo exposes to others (public API, federated remotes, events), where config and environment values live, where permission keys come from, how personal or medical data is handled;
- in-house libraries: internal-scope packages in `package.json` (old and new versions), how many files import each, template tag prefixes against framework controls (`mat-*` and similar), which one recent files use, and the component list from the package's `public-api.d.ts` / `index.d.ts`.

**How each question looks.** One **group** per question, like a brainstorm: one question per message, multiple choice where possible, wait for the answer.
- **The list in detail:** every item with its ID, what it asks of the code, why, and where this repo hits it (a count or a file from a command you ran). Mark each kit file `validated` or `experimental`. A claim such as "X replaces Y" needs usage evidence (recent files use X, or X is used more than Y); otherwise it becomes a choice (`A: shared/services` / `B: services`).
- **Recommended:** one line the user can accept as is, one reason per part from the probe. Recommend an `experimental` kit file when the probe found the situations its items cover; leave out items the linter or compiler already checks or nothing in the repo triggers; recommend a repo item only when usage shows a clear direction and no fact is still needed from the user; prefer a lint rule when a linter could enforce it. The line is one decision, never "if I had to pick"; with nothing qualifying, write `Recommended: nothing` and why.
- **Answers:** "default" accepts the Recommended line exactly as shown; "skip" takes nothing from the group; otherwise item by item (letters or IDs, `<id>#<item>` to switch off one kit item). For each repo item the user keeps, ask its scope (project or team) in the same answer. Never enable a file or keep an item that was not on the screen.
- **Confirm every item the user adds in their own words** (a convention, a review check, a Do-not-flag line), in any group or loop, before keeping it. Make it its own question, then continue where you were:
  - **How you understood it,** drafted as the item will be written: the trigger ("When X, …"), what it asks, where it applies (folders, kinds of file, new code only or existing code too), exceptions, the severity, the scope (project or team);
  - **How it fits this repo,** from commands you ran: how many places follow it today and how many do not, with one example of each; anything it conflicts with (a kept rule, a framework or library default, a neighbouring pattern such as a second base class); whether a linter, the compiler or a kept rule already covers it (name the config), or whether the agent already sees it in neighbouring code (principle 0);
  - **The question:** "Is this what you mean?" with choices: `A` yes, as drafted; `B` narrower (a concrete proposal, for example "new master tables only"); `C` wider (a concrete proposal); or a correction in their words. When the evidence shows no gap (it matches the code and nothing conflicts), say so in one line, and keep the choices.

  Keep the item only after the answer; on a correction, draft and confirm again.
- Skip a group with nothing to show. Number the questions ("Question 9 — rules: coding").

### Pass 1: rules for writing code (`## Design`, `## Implement`)

Used by `dk:story-runner`, `dk:bug-fixer` and `dk:code-refactor` while writing code. Groups, in order:
1. **Architecture**, from the probe: the kit has no architecture file (principle 0: it depends on the repo), so the probe is the standard list. Present the structure as items to confirm: layers and where new code goes, how data is reached, the module system, exposed contracts, config and environment values, permission keys. Each item is a candidate rule with its evidence. Keep out of Recommended what an agent sees by reading neighbouring code (where an existing kind of file already lives, a pattern every file follows); recommend placement only when two places compete or recent files moved.
2. **One group per kit file** with `## Design` or `## Implement` items whose `applies_to` matches the repo: `coding/review-basics`, `testing/basics`, `security/web`, `ui/forms-and-actions`. Show the items of those sections only.
3. **In-house libraries**, one group each: draft the rule from the probe (Implement, Review, Do not flag, with the component list) and ask only what the code cannot show: is the old version still allowed in new code, and which framework controls stay allowed (the `Do not flag` exceptions).
4. **Your own conventions (loop):** list the other repo suggestions the probe supports, each with its evidence, as choices, plus free text. Ask again after every answer, "default" included (it takes the Recommended line), until "no" or "skip". Never ask a bare "anything else?"; build each loop question from the context, in the user's language:
   - one line on what was just added (or "nothing added");
   - what the kept rules cover so far, by area, in a few words;
   - at most 3 new areas of this repo that no kept rule touches yet, each with its evidence from the probe (a folder, a dependency, a flow with its file count); areas offered before are listed by letter only;
   - **one question sentence** that names those areas, for example: "Rules so far cover permission keys, environment values and translations; nothing yet on date handling (`<date library>` in N files) or the report screens (N files under `<folder>`). Is there a convention there, or anywhere else, the agent should follow when writing code?";
   - how to end ("no"). Any claim that a linter or the compiler already covers something names the config that shows it.

   When the probe has no uncovered area left, say so and ask once whether the team has a convention the code does not show.

Then **read the pass-1 rules back** (drafted repo rules and kit choices) as their own question; write only after the user confirms.

### Pass 2: review checklist (`## Review`, `## Do not flag`, `## Severity`)

Used by `dk:pre-pr-check` and its reviewers. Do not ask again about items kept in pass 1: each one is checked in review at its severity. Open with one line saying so, and that `review/finding-quality` (the finding gate, R1–R7 and the certain/suspect tiers) is always on. Groups, in order:
1. **Severity:** a table of the rules kept in pass 1, each with its severity (kit items show theirs; propose one for each repo rule from the probe: blocker when data is written wrongly or a contract breaks, major when a user sees wrong behavior, minor otherwise). The user may change a repo rule's severity; a kit item's severity changes only through a project rule that overrides it (`docs/en/09-init-and-standards.md` 9.3).
2. **Review-only checks:** what a reviewer checks that is not a rule for writing code, found in the probe as "when the diff touches X, check Y", for example: version pins that must match another file, generated or vendored files that must not be hand-edited, a migration that needs a rollback, a changed public contract whose consumers must be told. Leave out any check that restates a rule kept in pass 1 (an environment value in every file, a translation key in every language): that rule is already checked. Show each with the file count or path.
3. **Do not flag:** what the linter, compiler and CI already enforce (from the probe), the `## Do not flag` lines of the enabled kit files, and repo patterns that would only be noise (for example a legacy folder the team does not touch). The user adds or removes items.
4. **Your own checks (loop):** as in pass 1, built from the context, never a bare "anything else?": what reviewers will now check, by area; 2–3 kinds of change the checklist does not cover yet, with evidence (for example "changes under `<folder>`, N files; to the pipeline files"); then ask whether reviewers should check something there, or leave something alone. Ask again after every answer, "default" included; only "no" or "skip" ends the loop.

Then **read the pass-2 checklist back** as its own question; write only after the user confirms.

There is no question limit; the loops end when the user says no. In a headless run, take each Recommended line, end the loops at once, and list the choices as assumptions in the report.

**Write, after each read-back.**
- Turn kept items and free-text answers into items in `${CLAUDE_PLUGIN_ROOT}/templates/standard.md` format: one idea per item with an ID, a trigger ("When X, …"), a one-line why and a severity. Pass-1 items go under `## Design` or `## Implement`, pass-2 items under `## Review`, `## Do not flag` and `## Severity` of the same topic file. Say so when an answer breaks principle 0 (the agent already knows it, or a linter checks it) and suggest not writing it.
- Project items → `.dev-kit/standards/<topic>/<name>.md`. Team items → the team folder (`standards.team`): if none is known, ask once for a path (outside the repo, shared however the team likes) and save it to `~/.dev-kit/config.yml` for the next repos. Kit files kept in either pass → `standards.kit`; switched-off kit items → `standards.disable`.
