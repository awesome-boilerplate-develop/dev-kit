English | [Tiếng Việt](../vi/06-evidence.md)

# 6. Evidence

All numbers in this document come from the dev-kit lab (private). The result of each run, together with the code the agent produced, is kept in private demo repos.

## 6.1 What the lab measures

| Item | Method |
|---|---|
| Model, host | Haiku 5.5 (`claude-haiku-5-5`), Claude Code 2.1.296, run headless (`claude -p`) |
| Isolation | `--setting-sources project,local`, empty MCP with `--strict-mcp-config`, only the plugin under test loaded via `--plugin-dir`. Checked that the agent sees no plugin, hook, MCP or CLAUDE.md from the host machine |
| Compared against | **baseline**: same model, no kit installed; the 3 original kits used alone; the versions of the mixed kit |
| Tasks | 9 cards on a sample shopping-cart app (story, bug, perf, refactor, 3 pre-PR cards with planted defects) and 13 SWE-bench Verified tasks (Django 4.0–5.0) |
| Grading | Hidden tests (the agent does not see them). Pre-PR: Sonnet 5.5 compares the report against the list of planted defects. SWE: as in the SWE-bench harness (reset the test files, apply the tests of the real fix, run FAIL_TO_PASS and the related test modules) |
| Task validation | Every SWE task: the original code fails, the real fix passes. Sample-app cards: the reference solution passes, the original code fails |

Total: 265 runs, about 12.4 USD (cost as reported by Claude Code in the transcript).

## 6.2 Main results

**Comparing ways of running** (USD per run is the average over tasks in the same group):

| Way of running | Quality vs baseline | Cost vs baseline |
|---|---|---|
| Superpowers | Equal | ~1.5–14× |
| Matt Pocock | Equal; one run where the controller stopped midway (bug B3) | ~1.5–3× |
| agent-skills | Equal | ~1.4–3× |
| Mixed kit v0.2 (all heavy parts merged) | Equal | ~3–13× |
| Mixed kit v0.3 | Equal | ~3× |
| **v0.4.1 = dev-kit 0.5.x** | **Equal** (mean score 0.864 vs 0.848) | **~2×** |

**v0.4.1 by task group:**

| Group | baseline | v0.4.1 | Ratio |
|---|---|---|---|
| Bug (3 cards) | 0.023 | 0.041 | 1.8× |
| Pre-PR (3 cards) | 0.031 | 0.089 | 2.8× |
| Refactor | 0.012 | 0.029 | 2.4× |
| Story (2 cards) | 0.032 | 0.067 | 2.1× |
| SWE (13 tasks) | 0.223 | 0.429 | 1.9× |

## 6.3 Tests with Sonnet 5.5 and on real repos (dev-kit 0.5.1)

**Sonnet 5.5, 5 hard SWE tasks, 2 runs each:**

| Task | baseline | dev-kit |
|---|---|---|
| 15916 | 1/2 | 1/2 |
| 16256 | 1/2 | 0/2 |
| 16263 | 0/2 | 0/2 |
| 16560 | 2/2 | 2/2 |
| 16631 | 2/2 | 2/2 |
| **Total** | **6/10** | **5/10** |
| USD per run | 0.129 | 0.165 |

- **Quality:** equal; a difference of 1 task is within random variation.
- **Cost:** with Sonnet, the extra cost of dev-kit is much smaller than with Haiku (about 1.3×, versus about 2× for Haiku).
- **Sonnet solves** 16560 and 16631 on its own; Haiku often fails both.

**Repeating the 9 cards with Haiku (0.5.1):** all passed, total cost 0.221 USD versus 0.226 for 0.4.1, so no regression.

**A real repo** (Node monorepo, real Postgres, run on a copy), model Sonnet 5.5:
- **`dk:init`:**
  - read-only first, then printed a plan and asked 4 questions before acting;
  - recognized the monorepo correctly (no `package.json` at the root) and recorded the test command for both packages;
  - green baseline (65 + 8 tests);
  - created `.dev-kit/`, `.gitignore`, and ran `codegraph init` according to the answers;
  - warned that the Superpowers plugin was installed.

  One oddity: the Postgres tests passed although the person answering had said "no Postgres yet". The agent noted this in the report without inventing a reason. On checking, the machine did have Postgres running via OrbStack.
- **`dk:story-runner`** (card "record publish time + filter by status"):
  - noticed the first half already existed and did not redo it;
  - added an admin filter with 4 tests (checked that the tests go red when the code is removed);
  - pre-pr-check self-reviewed, GO;
  - the spec has a Decisions section, the PR body has Evidence and Merge Danger.

  Because it ran under `claude -p`, the agent did not stop to ask; it decided on its own and marked 3 assumptions. How `grilling` questions a real person is still untested.

**Rule-application bug fixed in 0.5.2:** on P3 (10 files, 170 lines), the agent self-reviewed although rule C2 requires 1 reviewer. From 0.5.2, pre-pr-check measures the diff with `git diff --shortstat` before choosing the review level.

### Graph tools (dev-kit 0.7.0, rule G1)

17 SWE Django runs per side, Haiku 5.5. The indexed side had codegraph and code-review-graph indexes built in advance:
- **Result:** 10/17 solved on both sides; cost 0.034 vs 0.033 USD per run.
- **How the agent finds changed code:** it really used the graph (27 codegraph commands, 33 CRG commands) and grepped about half as much (31 vs 58).
- **Task 16560:** CRG pointed out that `__repr__` and `__eq__` had no tests; with the index it solved 2/2, without it 1/2. Too few runs to conclude.
- **0.8.0 (playbook):** 12/17, 0.031 USD per run.
  - Most used commands: `detect-changes` 21 times, `codegraph sync` 14, `tests_for` 4; the others a few times.
  - The 3 cards R1, B3, P3 with an index all passed.
  - Finding: `codegraph affected` does not find Python tests, so it was replaced by `tests_for`.

### Test on a real private repo at work (dev-kit 0.8.x, Sonnet 5.5)

Run in a separate git worktree, no commit, no push. The repo is a private Angular micro-frontend, about 1,500 files and about 9,500 specs.
- **`dk:init`:**
  - found the headless test script by itself, built two indexes (135 MB and 497 MB), green build;
  - red baseline (290 specs); on re-checking, the base branch was also red (303 specs). This produced rule B1 and `templates/baseline.md`.
- **`pre-pr-check`** (report-only mode) on the diff of an already merged PR (22 files, +1,569 lines):
  - **0.8.1:** read the `../../rules/` path wrongly (resolved against the current directory), so it skipped `detect-changes`; picked 1 reviewer; 1 major, 9 minor; 0.42 USD.
  - **0.8.2:** path changed to `${CLAUDE_PLUGIN_ROOT}`, and C2 now names medical data explicitly. The agent ran the full `sync`/`update`/`detect-changes`, used 4 reviewers, and produced 2 majors (including a weak test: it passes even when the error handling is removed) and one security risk that needs backend confirmation; 0.87 USD.
  - **Baseline check:** the 290 failures match the list exactly, 0 new failures, so it passes.
- **Whether each finding is right or wrong:** not yet checked by a human ❓.

### Backtest of `pre-pr-check` on real bugs (private repo at work, Sonnet 5.5)

8 fixed bugs; for each, find the PR or commit that introduced it. Review that PR again in report-only mode, then Sonnet grades whether the report points out the bug.

| | 0.8.2 | 0.8.4–0.8.5 |
|---|---|---|
| 6 PRs, 1 run each: caught / partial | 1 / 3 | 0 / 2 |
| PR C (the clearest bug), repeated: caught | 3/4 | 1/4 (the one catch was at the suspect tier, score 70) |
| PR D (3 form UI bugs), repeated | almost all missed | almost all missed |
| `detect-changes` ran | 2/6 | **6/6** |
| Report passes `check_report` | – | **6/6** |
| Precision of the "certain" tier (self-checked by an agent, 0.8.4; the user delegated the decision to the agent, not confirmed by a human) | – | 5/9; without the "missing test" items, 2/6 |

**Reading the results:**
- **Forcing compliance works.**
- **Bug-catching ability varies strongly between runs;** the gate was not seen to cause a bug to be lost.
- **False findings in the certain tier** are mostly pre-existing code or intentional changes.
- **Half of the bugs** need knowledge of runtime behavior or of the contract with the backend, so they are hard to catch by reviewing the diff.
- **One false finding came from how the diff was built** for a PR merged with two parents (it pulled in code from another PR). The backtest was fixed; results in the next section.

**Two-parent merge PRs, diff rebuilt to the correct scope (dev-kit 0.8.7):** the worktree is placed at the merge commit itself, the base is the first parent, so the diff contains only the PR's own changes (PR A: 12 files; PR B: 26 files). Each PR was run once.

| PR | Bug | 0.8.2 (wide diff) | 0.8.4 (wide diff) | 0.8.7 (correct diff) |
|---|---|---|---|---|
| PR A | A sort request sent UI column names in `SortString`, which the backend rejects | missed | missed | **caught**, at the suspect tier (score 70) |
| PR B | Double submit: pressing Submit several times while a request is in flight | partial | missed | missed |

- **"Certain" tier (self-checked by an agent, not confirmed by a human):**
  - PR A no longer has any certain finding; the false findings were gone because the other PR's code was gone.
  - PR B has 3/3 correct findings: RBAC hard-coded to `true` (the most valuable, already seen at 0.8.4), a filter test using `every()` on an array that can be empty, and `en.json` with 62/48 lines changed only in whitespace. The last two are correct but low value.
  - The three "missing test" items that 0.8.4 put in the certain tier now sit in the suspect tier, as the R1 gate requires.
- **Both reports pass `check_report --base`** (0.87 and 1.09 USD).
- **New compliance gap:** on PR A, the agent only ran `ls .dev-kit .codegraph`, then wrote "no .code-review-graph/ index" and skipped `detect-changes`, although the index had been built before the run. `check_report` only checks that the Graph line is present, not that its content is true.
- **Fix in 0.8.8, PR A re-run once:** the agent checked with `test -d`, ran `detect-changes` (risk 0.85, 17 test gaps), and the report passed `check_report`; the sort bug was still caught at the suspect tier (score 70); 0.74 USD. Remaining gap: 2 "certain" findings (scores 82 and 80) were really missing tests, but written as "No service spec covers…" and "Only 404 … is tested", so the "missing test" regex of `check_report` did not catch them.
- **0.8.9–0.8.10, blocking missing-test items in the certain tier by location and by the Rule column:**
  - 0.8.9 (FAIL when an item only points at a test file and has no rule), PR A re-run: all 6 certain items were missing tests, but the Rule column said `R1`, so they still got through.
  - 0.8.10 (only a standard id `topic/name#X` or a spec counts as a rule), PR A re-run: the agent got FAIL, moved the missing-test items down to suspect, and ran `check_report` 4 times until it passed. The certain tier was left with 1 minor item (a repeated error-handling block); the sort bug was still caught at the suspect tier (70); 0.75 USD.
  - On the 16 older reports, those that passed before still pass. The Graph-line check caught one more skipped `detect-changes` (a repeat run of PR D, 0.8.5), so 2/16 reports had this defect.
  - **Reading the results:** the agent exploits every loophole in a rule written in words (writing `R1` in the Rule column); machine checks must rely on things that are hard to game (file location, rule id format), not on wording.

### Project rule: in-house controls (dev-kit 0.8.7, rule T1)

Card "dialog form" (input, select, textarea, toggle, button), `dk:story-runner`, Sonnet, 2 runs per side:
- **With the rule:** used in-house controls (6 and 10 tags), Material only where allowed.
- **Without the rule:** used Material throughout (18 and 16 tags), 0 in-house controls.
- **Tests green in all 4 runs.** Cost rose by about 25%.

**Conclusion:** a rule about something the agent cannot know by itself works clearly; a rule about something the agent already does on its own does not (see the earlier section on the general rules).

**Scope decision for the rule (2026-10-14, decided by the agent from repo data):**
- **Project scope only** (`scope: project`): only one of the three repos uses the v2 library (105 files import v2); the other two have 0 files. That is not enough basis to promote it to a team rule.
- **v1:** banned in new code when v2 has a component with the same purpose. A table skeleton loader and a form-object helper are not yet in v2, so they are still allowed.
- **Allowed Material:** the dialog service and dialog containers, tooltip, snackbar, spinner, input chips, CDK overlay. An earlier trial also exempted the datepicker, but v2 has a datepicker and datetimepicker, tab group, autocomplete, paginator and color picker, so these components moved to U1.

### Multiple CLIs (dev-kit 0.8.12)

**Probe with a dummy plugin** (same layout as dev-kit: skill in `skills/`, files to read in `rules/` two levels up; 1 run per CLI):

| CLI | Substitutes `${CLAUDE_PLUGIN_ROOT}` | Agent knows the `SKILL.md` path | Can read the file two levels up | Subagent tool |
|---|---|---|---|---|
| Claude Code 2.1.299 | yes | yes | yes | `Agent` |
| Codex 0.160.1 | no | yes (whole-tree copy in the cache) | yes | `spawn_agent` |
| Antigravity 1.3.5 | no | yes (whole-tree copy) | yes | `invoke_subagent` |
| Copilot CLI 1.0.89 | no | yes | yes when installed; with `--plugin-dir` you must add `--add-dir` | `task` |
| OpenCode 1.18.35 | no | symlink path | yes, after resolving the symlink and allowing `external_directory` | `task` (`general`) |
| Cursor | – | – | – | could not run: needs `cursor-agent login` (support dropped in 1.2.3) |
| omp 18.10.4 | no | yes | yes | `task` |
| pi 1.0.2 | no | yes | yes | none (core pi); support paused from 0.8.13 |

**Check with the real dev-kit:** install the kit, then tell the agent to load `pre-pr-check` and follow only the Harness section. Claude Code, Codex, Copilot, Antigravity, OpenCode, omp and pi all returned the correct kit directory and the first line of `rules/RULES.md`. The six non-Claude-Code CLIs all read their own `harness/<cli>.md` correctly. On omp (loaded with `--plugin-dir`), `security-auditor` and `test-engineer` show up as named task agents.

**Backtest of PR A, 1 run per side:**

| | Claude Code (Sonnet 5.5) | Codex 0.160.1 (the account's default model) |
|---|---|---|
| Sort bug (`SortString`) | partial (4 earlier runs, 0.8.7–0.8.10: caught) | caught, at the suspect tier |
| `detect-changes` | ran (risk 0.85, 17 test gaps) | ran (risk 0.85, 17 test gaps) |
| Review depth | four reviewers | four reviewers: 4 `spawn_agent` calls with `fork_turns: "none"` (seen in the session rollout) |
| `check_report` | passed | passed |
| Cost | 0.77 USD | 1.12 million input tokens (1.04 million from cache), 4.6 thousand output tokens |

**Reading the results:**
- **The kit runs on Codex with the full flow** (graph, four reviewers, report gate) without changing any controller content.
- **The "partial" on the Claude run is a single run.** The Harness section does not change behavior on Claude Code (the variable is still substituted), so this is most likely run-to-run variation; no repeat run was done to confirm it.
- **Review quality on Copilot, Antigravity, OpenCode and omp is not measured;** only loading was checked.
- **pi paused (0.8.13):** it loads but has no subagent, so the review roles run in the main session; this way of running is not measured, so it is not supported.

**Rules on other CLIs:** the rules and evidence above were measured on Claude. On Codex there is only 1 backtest run; repeat runs are needed before treating a rule as useful on that CLI.

### `dk:init` questions on 3 real repos (dev-kit 1.2.0–1.2.2)

Fresh git worktrees of three private repositories, Claude Code with Sonnet 5.5, one answer per turn with `--resume`; every question answered "default" (the read-back confirmed). Checked against docs 09 §9.8: at most 12 questions, guessed answers mostly right.

| Repo | Questions (standards) | What the probe suggested | Cost (USD) |
|---|---|---|---|
| A: Angular micro-frontend, ~840 `.ts` files | 9 (4) | In-house component library: 110 files on v2, 7 on v1, 36 templates with framework controls; a project rule drafted and read back | 0.33 |
| B: Angular micro-frontend, ~390 `.ts` files | 10 (4) | The repo's own control set (18 controls under one folder, 11 templates using them, 77 framework form fields left); a project rule drafted and read back | 0.40 |
| C: .NET API, ~290 `.cs` files | 8 (3) | No project rule; the `ui` topic skipped (no UI). Tests could not run: package restore failed on a private feed | 0.23 |

- **≤ 12 questions:** met (3–4 standards questions, 8–10 in total). `git status` was unchanged in all three.
- **Guessed answers** (checked by the agent against the code, not confirmed by a human): repo B's suggestion made 7 claims, 6 correct; the wrong one stated that newer controls replace older ones, while the code used the older ones more (16 vs 10 and 11 vs 0). Repo A's counts match earlier manual counts on that repo.
- **Deviations, fixed in 1.2.2:**
  - "default" ticked `experimental` kit files in B and C (A kept them off), although the skill said they start unticked → "default" now never ticks an `experimental` file and keeps no suggested rule.
  - A migration direction was stated without usage evidence → every count must come from a command the agent ran, and a direction without evidence is asked as a question.
  - Tests that cannot run had no defined path; the agent improvised "not measured" → now a defined branch (`baseline: not-measured` in `config.yml`).
  - With no drafted rules, the read-back joined the open question in C → now allowed.
- **After the fix (repo B, topic questions only):** the `coding` question stated "experimental, so the default is off", and unproven ideas (`: any` in 124 files, unsubscribe style) were asked as questions. A second run also proposed `architecture` rules that the first run had skipped: what the probe finds varies between runs.


## 6.4 Findings that went into the design

| Finding | Change in dev-kit |
|---|---|
| A sub-skill registered and then hidden with `disable-model-invocation` cannot be called by the controller either | Sub-skills live in `parts/`, not registered |
| Claude Code ships built-in skills `init`, `code-review`, `security-review` | Controllers use their own names; initialization is `dk:init` |
| Copying leaves dangling references (`executing-plans`, `writing-skills`) | Fixed; `scripts/check_parts.py` added |
| A part makes the controller stop midway | Rule F1 |
| SDD and 4 reviewers do not make code more correct but cost a lot | Rules C1, C2 |
| A rule that looked like a 6/6 win turned out to be overfit | Rule-enabling procedure: must pass ≥ 5 new tasks |

## 6.5 Limits of the measurement

- **Few repetitions:** most combinations ran 1–3 times. A difference of 1 task is not enough to conclude; only large, repeated differences are used.
- **Model:** mostly Haiku 5.5. Sonnet 5.5 was only tried on 5 SWE tasks and 1 real repo; Opus not tried ❓.
- **No human:**
  - The lab runs headless: every question and approval gate is decided automatically.
  - The "asks the right question" part of `grilling` and the value of the approval gate are not measured.
- **Single-session work:** no work spanning several sessions, and no test of recovery after the context is compacted.
- **Repos:** the sample app, Django, and one real repo (a Node monorepo, run on a copy).

## 6.6 Detailed history

Per-round reports are kept in the dev-kit lab (private), which is not published:
- round 1: easy cards;
- round 2: hard cards;
- round 3: SWE-bench;
- v0.3;
- rule check on new tasks;
- v0.4.
