# dev-kit changelog

## 1.7.4 (2026-10-24)
- **`check_report.py` requires a location:** every finding, certain or suspect, must give `file:line` (rule R1: located). A finding with no file at all skipped the `--base` check, and one with a file but no line passed it whenever the file was in the diff.
- **`check_report.py` reads a blocker's state from its Status cell only:** a blocker counted as fixed when "fixed" appeared anywhere in its row, so a Status of `unfixed` or a finding about a "fixed-size buffer" let a GO verdict pass.
- **`check_report.py` checks the table schema:** a certain row has the template's 6 cells and a suspect row 5, severity is `blocker` / `major` / `minor` (rule S1), and a certain Status is `fixed` / `open` / `pushed back`.
- **Report tied to a diff:** Review setup has a `Diff: <merge-base sha>...<HEAD sha>` line; with `--base`, `check_report.py` requires it and fails when it no longer matches the repo (a commit after the review makes the report stale; commits that change only `.dev-kit/` are allowed). `pre-pr-check` step 6 writes the report after the last commit of the work.
- **`story-runner` step 4 runs `dk:pre-pr-check` for a small diff too:** in 2 of 2 Sonnet 5.5 runs of the lab story card the agent reviewed the small diff itself, so `check_report.py` never ran.
- **Tests:** `scripts/test_check_report.py` covers these cases and runs in CI; on 1.7.3 four of the location and Status tests fail.
- **Checked** in the lab sample app, one run each, headless, report-only pre-PR cards P1–P3 on Haiku 5.5, Sonnet 5.5, Opus 5.5 and Fable 5.1 (12 runs): every report's Diff line matched `git merge-base`/`git rev-parse HEAD` (Fable once with short SHAs) and passed `check_report.py --base main`; the new checks failed two reports that the agents then fixed (a certain finding naming a file without a line, a row moved up from suspect without a Status cell); verdict NO-GO on all 12. Fable 5.1 needed 2.0–3.5 USD per card. P1 with the base branch named `develop`, no `main` branch and `base_branch: develop` in `config.yml` (Sonnet): the agent used `develop` for the diff, the Diff line and `--base`; OK. Story card S1: Haiku ran `dk:pre-pr-check` after its 2 commits, Diff matched HEAD, OK; after the step-4 change Sonnet ran `check_report.py` in 2 of 2 runs (one through `dk:pre-pr-check`, one inline), both OK at the time, but both then committed the report and the lab's `LAB_DECISIONS.md`, so a later recheck reports them stale.

## 1.7.3 (2026-10-24)
- **Tick forms show what a tick does:** each item's label starts with a colored icon and a word for the action, `🔴 Remove · S4 …` for an item that is on and `🟢 Add · S1 …` for one that is off, instead of its state (`on · S4 …`), which read as the opposite next to an empty checkbox. The `Keep this group as shown` option comes after every item, or first where the choice tool asks for the recommended option first (agy's `ask_question` does).
- **Checked** on agy 1.4.6 (Gemini 3.8 Flash), this skill copied over the installed 1.7.2, `dk:init standards` (quick, forms) on the Angular clone, choices made by a driver script: labels read `🔴 Bỏ · C1 …` for items that are on and `🟢 Thêm · S1 …` for the one that is off, aligned in agy's form; unticking C1 gave one line `☐ C1 … (coding/review-basics)` before the write question; `standards.disable` gained C1, `check_standards.py` OK, `git status` unchanged; 8 questions, ~9 min.

## 1.7.2 (2026-10-23)
- **Quick setup, after the tick forms:** the lines whose mark changed are shown again in a reply, one checklist line each with its new mark and file (`☐ C5 … (coding/review-basics)`), only those lines; a rerun on omp (Opus 5.5) showed only the sentence "C5 goes from on to off" and repeated an unchanged item, and a run with a first wording of this fix put "☐ C5 tắt" in parentheses in the question text, next to unchanged items.
- **Quick setup has one read-back:** a gap noticed after the approved checklist is noted in `init-report.md` for a detailed run, not asked as a new item; in the same rerun the agent asked for a new color check after writing. The rerun confirmed the 1.7.0/1.7.1 fixes: S1–S3 as their own `☐` lines, `file#ID` on repeated IDs in the checklist and the form labels, the file named on the new Do-not-flag line, `check_standards.py` OK.
- **Checked** on omp (Opus 5.5) with this skill copied over the installed 1.7.1, interactive `dk:init standards` (quick) on the React Native clone with its earlier standards in place, choices made by a driver script. With the form path (`B`, untick C5, keep the other groups): after the forms the agent wrote one line, `☐ C5 … (coding/review-basics)`, then asked to write; `standards.disable` gained C5, `init-report.md` named C5 as changed by the user, `check_standards.py` OK, `git status` unchanged. In this and two more runs (one with `A`) no question came after the write; checks the earlier rerun asked about afterwards (hex colors against theme tokens) were drafted into the read-back. One run put `Keep this group as shown` first instead of last.

## 1.7.1 (2026-10-23)
- **Quick setup, repeated IDs:** item IDs are unique only within a file, and repo checks are often all `V1` (three files did so in the 1.7.0 run), so a bare `-V1` was ambiguous. Lines whose ID repeats in another file now show the file, changes to them are given as `file#ID` (`-ops/environment#V1`, the form `standards.disable` uses), and the agent asks back when a bare ID matches more than one line.
- **Tick forms on timeout:** the `Keep this group as shown` option is marked Recommended, because omp picks the Recommended option when a question times out; a timeout now changes nothing instead of switching the first item.

## 1.7.0 (2026-10-16)
- **Quick setup read-back is a pre-ticked checklist:** one line per item, `☑` for each Recommended item that will be written or kept, `☐` for items switched off, not offered or drafted but not recommended, each with its ID and reason. You add or remove with `+ID`/`-ID` (for example `-S5 +S1`) or choose `B` for one multiple-choice form per kit file plus one for the repo rules and checks. The CLIs' choice tools cannot pre-tick options (omp's `ask` has `multi` and one `recommended` index; agy's `ask_question` has `is_multi_select`), so in a form a tick switches an item's state, the label carries the current state as a word (`on · S4 …`) rather than ☑/☐ next to the form's own checkbox, and a `Keep this group as shown` option makes "no change" an explicit answer (a form sent with nothing ticked is not a clear answer; omp's RPC clients show a Done row only after a tick, while its TUI ticks with `␣` and submits with `⏎`). The lines whose mark changed are shown again before writing; each Do-not-flag line names its file in the read-back; nothing is written before `A`; `init-report.md` records each mark the user changed.
- **Checked** on omp (Opus 5.5) before release, with this skill copied over the installed 1.6.0, two interactive `dk:init standards` runs on the React Native clone with the standards removed. Run 1 (`A`, ~7 min, 2 questions): the read-back was a checklist of ☑/☐ lines with evidence, written as ticked, `check_standards.py` OK, `git status` unchanged. Run 2 (`B`): one form per kit file and one for repo rules, labels `bật · C1 …` / `tắt · S1 …`, the keep option last and pre-selected as Recommended; unticking C5 and keeping the other groups gave a question naming "C5 đã tắt", then `standards.disable` holding C5 with S1–S3 and U4, `check_standards.py` OK, `init-report.md` naming C5 as changed by the user. Two gaps fixed in the skill after the runs: run 1 grouped S1–S3 into a not-offered note instead of `☐` lines (run 2 had the lines), and a ticked Do-not-flag line with no file led the agent to create `coding/baseline.md` after approval. omp's multiple-choice form uses `␣` to tick and `⏎` to submit.

## 1.6.0 (2026-10-15)
- **Quick or detailed setup:** right after the graph indexes (and first in `dk:init standards`), `dk:init` asks one question. `A` quick (Recommended): the agent probes and drafts every standards group as in detailed mode, takes each Recommended line itself, runs no own-convention loop and no `CONSTRAINTS.md` question (default no), then sends one read-back of everything it will write and asks once: write all, go through it group by group, stop, or changes in your own words. `B` detailed: the existing group-by-group questions. A red baseline is asked in both modes. `init-report.md` records which mode was used and the Recommended lines taken.
- **Kit items not offered when their trigger is absent:** before a kit group, each item's "When …" trigger is looked for with a command; an item whose trigger is shown absent (a server-side check with no server handler, an injection check with no HTML, URL, WebView, shell or query sink, testing items with no test runner) is not asked, listed in one line with the command and count, and switched off if the file is kept. Items whose trigger needs reading code (secrets, personal data, error text) stay asked: on the React Native clone a grep found no raw-server-error toast, while the agent found one by reading the error helper.
- **Checked** on omp (GPT-6.1 Sol) with the released 1.6.0, a full interactive `dk:init` on a fresh clone of a React Native (Expo) app, choosing quick: 5 questions in ~15 minutes (commands, indexes, quick or detailed, red baseline, one read-back) against 8 standards questions alone in the 1.4.11 detailed run. The read-back listed every kept item with its evidence, the switched-off U4 with its reason, and S1–S3 as not offered (no server handler, no role-based UI check, no injection sink found, with a note that a search finding nothing does not prove the repo safe), plus three review-only checks to write. After "write all": 3 repo files (`ops/environment`, `ops/generated-types`, `ui/locales`), `standards.disable` holding S1–S3 and U4, `check_standards.py` OK, `init-report.md` naming quick setup and the Recommended lines taken, no `CONSTRAINTS.md`, `git status` unchanged.

## 1.5.0 (2026-10-15)
**Breaking: a kit standard id changed.**
- **`security/web` is now `security/basics`** (`standards/security/basics.md`): the file is not about the web only (it covers client apps of any platform; its items 1.4.11 already mapped to mobile equivalents), and `basics` matches `testing/basics` and `coding/review-basics`. Item IDs `S1`–`S6` and their text are unchanged. This replaces 1.4.11's decision to keep the old id: the name kept confusing users (a React Native app was offered "web" security), so the rename is done once, now, with every reference in the kit moved (skill `init`, docs 03 and 09 in four languages); entries below this one keep the old name as history.
- **Action needed in a repo initialized before 1.5.0:** in `.dev-kit/config.yml`, change `security/web` to `security/basics` in `standards.kit`, and `security/web#<item>` to `security/basics#<item>` in `standards.disable`. Reports that cite `security/web#…` no longer pass `check_report.py` (the id is not found), as for any removed id.
- **An id with no file is named, not skipped silently:** controllers (rule T1) now name an id in `standards.kit` or `standards.disable` that matches no file in the report. Without this, the rename would have dropped the security standards from an old config without a word.
- **Checked:** no `security/web` left outside the changelog and past evidence; `check_standards.py` OK on the kit; `check_report.py` rejects a report citing `security/web#S2` and accepts the same report citing `security/basics#S2`; the two initialized clones on this machine had their `config.yml` migrated.

## 1.4.11 (2026-10-15)
Fixes from an interactive `dk:init` run on omp against a React Native app.
- **A choice form must be readable on its own:** the run's kit questions after the first two showed the agent's evaluation only as reasoning, and forms such as "Keep U2, turn off U1/U3/U4/U5" with no hint of what those IDs are. The skill now says: reasoning is not a reply (the list and evidence are written as a normal reply before every group, the last as much as the first); a choice that names item IDs says in a few words what each kept and each switched-off ID is, and the group's items go in the tool's question text too.
- **Stack fit per item:** `security/web` is offered to any repo whose `applies_to` matches (`**/*`), so a React Native app got it. Each item now says whether it applies to the stack found in step 3, with the reason when it does not (server-side checks in a client app), and names the stack's equivalent of a platform term. In that run the agent judged S1–S3 not applicable and S5/S6 violated, so the file was useful; the name was the confusing part. The id `security/web` is kept (renaming it would break `standards.kit` in every initialized repo and the cited reports).
- **Kit wording:** `security/web` S4 mentions "an app build" next to a web bundle, and S5 names unencrypted device storage such as `AsyncStorage` next to `localStorage`. No new requirement.
- **Checked** on omp (GPT-6.1 Sol) with the released 1.4.11, `dk:init standards` on a fresh clone of a React Native (Expo) app, interactive (8 questions, ~12 minutes): every kit group (`coding`, `testing`, `security`, `ui`) came with a normal reply holding an item table (6–8 rows) with evidence, and the form's question text listed each ID with a few words; the `security/web` reply said the name says "web" but the file covers mobile apps, mapped `localStorage` to `AsyncStorage`, and the agent recommended keeping S4–S6 and switching off S1–S3. Option labels still named IDs ("Keep S4, S5, S6; off S1, S2, S3"), with the meaning in the description line.

## 1.4.10 (2026-10-15)
- **`dk:init` probes with the graph first:** when step 5 built the indexes, the standards probe runs `codegraph sync` and `code-review-graph update -q`, then `code-review-graph architecture --detail-level minimal` for the areas of the code, then `codegraph explore "<topic>" --max-files 5` for backend calls, permission checks, configuration, shared base classes and personal data, using the caller counts it returns as evidence, and `codegraph callers`/`node` on symbols defined in the repo. grep and file reads cover only what the graph does not hold (linter configs, package imports, template tags). The graph commands run are listed in `init-report.md`.
- **Removed a dead example:** the skill named `codegraph callers` on the HTTP client; `codegraph callers HttpClient` finds nothing, because framework classes are not in the graph.
- **Measured** (A/B on one private repo, agy, headless `dk:init standards`, 2 complete runs a side, docs 06): graph queries 0 → 6–8, grep/find down about a third; 370 s and 277k tokens against 434 s and 314k, which is "not slower" given A's spread (360–507 s); B added details only the graph showed. One extra B run stopped after its first question (a headless-mode variation) and is not counted.

## 1.4.9 (2026-10-15)
- **IDs follow the topic letter, and `check_standards.py` enforces it:** `## Design`/`## Implement` IDs are the topic's letter and a number (`A` architecture, `C` coding, `T` testing, `S` security, `U` ui including in-house component libraries, `P` api, `D` data, `O` ops, `R` process or review); a Review line that defines its own item uses `V` or the topic's letter. The agent decides an item's topic file when it first shows it. A date convention is coding, not data. The "own prefix for in-house libraries" allowance is gone. The kit's own standards already follow this.
- **Placement examples:** environment, pipeline, deployment and dependency files go to `ops/`, translation files to `ui/`, exposed module contracts to `architecture/`.
- **Checked** with an interactive agy rerun from an empty `.dev-kit/` (21 questions, ~34 minutes with index and baseline). The 1.4.8 index estimate counted 843 code files (~135 + ~506 MB; measured 137 + 529 MB). Both Write-in items were confirmed before being kept, and the environment check's confirmation said the reviewer reads the spec, not the PR description. All three review-only checks went to `ops/deployments-and-deps.md`; IDs `A1`–`A5`, `U1`, `U6`, `V1`–`V3`; the agent ran `check_standards.py` (OK, in `init-report.md`). Left: the toast confirmation gave code examples but no follow / not-follow counts.

## 1.4.8 (2026-10-15)
Fixes from running `dk:pre-pr-check` on a real branch with the standards `dk:init` wrote.
- **`check_report.py --base`:** suspect findings must also sit in the changed lines; pre-existing code is dropped (R1), not moved to suspect. The old message said "move to suspect or drop", which contradicted R1; the end-to-end run listed two repo-rule findings on code the agent itself marked as outside the diff. The new check fails exactly those two; 31 earlier backtest reports give the same result as before when run without `--base`.
- **`scripts/check_standards.py` (new), run by `dk:init` after writing:** frontmatter (`id` equals the path, `topic` is a template topic and matches its folder, `scope`, `status`), every `applies_to` glob matches a tracked file, only the five section names and each at most once, item IDs of one to three capital letters and a number, unique, and every ID a Review line names is defined. The agent fixes the files until it prints OK (at most 3 tries) and puts the output in `init-report.md`. On files from earlier runs it caught a duplicated `## Do not flag`, an `id`/folder mismatch, and IDs such as `DATE-1` or `R_CHK1`. CI runs it on the kit's own standards (`--no-files`); it found `review/finding-quality` missing `topic`, now added.
- **IDs and placement:** the topic's letter plus a number (`V` for review-only checks), never changed after they are shown; pass-2 items go to the topic file of what they check (pipeline and dependency checks to `ops/`).
- **Index size:** counts code files only, not templates or styles (the previous estimate counted ~1,450 files under `src/` for ~850 indexed).
- **Docs 05:** a table for starting `dk:init` on each CLI (first message, interactive questions, headless behavior), from the 2026-10-15 runs. Docs 03 no longer mentions a scope in the confirmation (removed in 1.4.3).
- **Checked** with agy (Gemini 3.8 Flash), headless `dk:init standards` on the same clone (~6.5 minutes): the agent ran `check_standards.py` (seen 3 times in its steps) and reported OK in `init-report.md`; the 3 files pass it; IDs `A1`–`A5`, `V1`, `V2`, `D1`, `I1`, `I2`, all `experimental`. Not followed: the environment-file check went to `architecture/` instead of `ops/`, and the date rule in `coding/` used `D` instead of `C`; the script checks format, not these choices.

## 1.4.7 (2026-10-15)
Fixes from an interactive `dk:init` run with agy (Gemini 3.8 Flash), driven through its real UI.
- **The choice tool is only the last line of a question:** before calling it, the agent writes a message the user can read with the evidence, the group's list in detail, the drafted items of a read-back, the `CONSTRAINTS.md` explanation and the "how it fits this repo" part of a confirmation. In the run before the fix, every question was a bare form whose labels were the only information.
- **"All items" is a choice, not a default:** recommended only when every item has repo evidence (before: every kit group recommended all items, including a server-side check in a front-end repo).
- **Read-backs show what will be written:** every drafted repo item in full (ID, trigger, severity, file), kit files kept and items switched off; never "as above" without the list.
- **Repo rule files** keep `status: experimental` and the `id` and item IDs shown in the read-back (before: `validated`, and a renamed file id).
- **Checked** with an interactive rerun (19 questions, ~16 minutes): every form came after a message with the list and evidence; `security/web` recommended without S1 with the reason, and `config.yml` disabled `security/web#S1`; the read-back listed each file and item; the `CONSTRAINTS.md` question explained itself; a confirmation showed "66 files use luxon, 0 use moment"; files written as `experimental` with the read-back ids. The Write-in path was not exercised in the rerun.

## 1.4.6 (2026-10-15)
- **Choice tools:** Antigravity's `ask_question` joins Copilot `ask_user` and omp `ask`. The "(Recommended)" choice goes first; "Other" is added only when the tool has no free-text line of its own (Antigravity adds "Write-in..."). A tool answer that comes back skipped or empty (headless runs auto-skip) means nobody can answer: take `A`, list it as an assumption, never ask again.
- **Harness note (Antigravity):** questions use `ask_question`; interactive `agy -i` shows them as a numbered list with "Write-in..."; headless `agy -p` auto-skips them, so `dk:init` takes every default.
- **Checked** on a real Angular repo with agy 1.3.5 (Gemini 3.8 Flash). Interactive: question 1 showed `1. (Recommended) Base master-p2b, test npm run test-headless, build npm run build, no lint`, three alternatives and `5. Write-in...`. Headless: 19 questions were auto-skipped and the agent ran the whole setup with defaults in one turn (~15 minutes), with the choices also written as text.
- **Rerun headless on 1.4.6** (same repo, fresh worktree, ~12 minutes): 12 questions went through `ask_question`, each surfaced once and auto-skipped, none asked again; the agent took every `A` and listed them under "Assumptions" in `init-report.md`. Base branch `master-p2b`, only `.codegraph/` added to the exclude file, baseline output in `.dev-kit/baseline-*.log`, `git status` unchanged.

## 1.4.5 (2026-10-15)
- **Every `dk:init` question ends with choices plus Other:** at most 4 lettered choices, `A` being the recommended answer marked "(Recommended)" and spelled out in full, `B`–`D` real alternatives, and a last "Other: type your own answer" line; "default" or Enter means `A`. When the harness has a choice tool (Copilot `ask_user`, omp `ask`) the same choices go through it. No question ends with only "type default or a value".
- **Checked** on a real Angular repo with Claude Code (headless, so the choices came as text): the commands/base-branch question, the graph-index question and the architecture group all ended with `A. (Recommended) …`, alternatives and `Other`. The choice-tool path was not exercised.

## 1.4.4 (2026-10-15)
Fixes from running `dk:init` on 6 CLIs against one private repo (docs 06).
- **Base branch:** `origin/HEAD` is compared with the branch recent pull requests merge into and the current upstream (last commit date, commits ahead); when they differ, step 4 asks a choice with that evidence. Three of six CLIs had picked a branch nobody merged into any more.
- **Exclude file:** `git rev-parse --path-format=absolute --git-path info/exclude` (`.git` is a file in a worktree; the file is shared by every worktree). Index folders are added in step 5 itself, `.dev-kit/` never, no duplicates; the report claims an added line only with the command that added it. Rule O1 says the same.
- **Index size:** estimated per indexed file (about 0.16 MB codegraph, 0.6 MB code-review-graph; measured 136 MB and 529 MB for ~850 files), replacing "150 MB and 600 MB per ~3,000 files", which was about 2× low.
- **Baseline:** test and build output go to `.dev-kit/baseline-test.log` / `baseline-build.log`; counts and failing names come from those files, so the suite runs once; never a shared `/tmp`.
- **Asking:** only the questions the steps name, no "shall I continue?"; a read-back is its own message and an unanswered one is never a "no" (Codex had lost pass 2 this way); the Recommended line is checked against its own text; a confirmed item keeps its ID; the confirmation says when a check depends on what a reviewer cannot see (PR description, CI, screenshots).
- **Harness notes:** OpenCode (an auto-rejected `external_directory` ends the turn silently: deny `*` and allow the kit; loading without installing via `OPENCODE_CONFIG_DIR`/`OPENCODE_CONFIG_CONTENT`; `realpath` the skill link instead of searching the disk); Copilot (headless asks nothing; `--allow-all-tools` does not cover paths outside the working directory).
- **Checked** on the same repo after the fix: Claude Code steps 1–6 and Codex pass 2 (docs 06).

## 1.4.3 (2026-10-15)
- **No project-or-team question in `dk:init`:** dev-kit is set up one repo at a time, so everything kept goes to `.dev-kit/standards/`. `dk:init` no longer asks for or remembers a team folder (step 2 now says so); controllers still load `standards.team` when it is set by hand, and offering it in `dk:init` waits for multi-repo support. READMEs, docs 03 and docs 09 updated.
- **Checked** on a real Angular repo: the architecture group and the confirmation of a user-added rule ran with no scope question.

## 1.4.2 (2026-10-15)
- **Items the user adds in their own words are confirmed in context** (rules, review checks, Do-not-flag lines, in any group or loop), as their own question before they are kept: the agent drafts the item as it will be written (trigger, where it applies, new code only or existing code too, exceptions, severity, scope), checks it against the code (how many places follow it and how many do not, with an example of each; conflicts; whether a tool or a kept rule already covers it), then asks "Is this what you mean?" with `A` as drafted, `B` narrower, `C` wider, or a correction.
- **Checked** on a real Angular repo, one addition per pass. Pass 1, "toasts take their text from translation keys": 76 toast calls, none with a literal first argument, the calls that pass a variable named, and a narrower "new code only" choice offered. Pass 2, "PRs that change a master screen need before/after screenshots": the agent noted that `dk:pre-pr-check` reads the branch diff, not the PR description, so a reviewer cannot verify it, and offered "only when `*.html`/`*.scss` change" as the narrower choice.

## 1.4.1 (2026-10-15)
- **The loop question fits the context:** instead of a bare "anything else?", each loop turn says what was just added, what the kept rules cover so far, up to 3 new areas no rule touches yet with their evidence (earlier ones by letter only), and ends with one question naming those areas. A claim that a linter or the compiler already covers something must name the config that shows it. Pass 2's loop does the same with the kinds of change the checklist does not cover.
- **Checked** on a real Angular repo (pass-1 loop, 2 runs): the first run listed 5 areas, had no actual question sentence, and claimed the compiler checks `any` (no linter, and explicit `any` is not a compile error); after tightening, the rerun listed 3 areas with counts and asked one question naming them.

## 1.4.0 (2026-10-15)
- **`dk:init` standards in two passes:** pass 1 asks the **rules for writing code** (`## Design`/`## Implement`: architecture from the probe, each fitting kit file, in-house libraries, then the user's own conventions); pass 2 asks the **review checklist** (`## Review`/`## Do not flag`/`## Severity`: severity of the kept rules, review-only checks, the Do-not-flag list, then the user's own checks). Rules kept in pass 1 are not asked again in pass 2. Each pass is read back before it is written, into the same topic files.
- **One group per question, like a brainstorm:** each question shows its list in detail (what each item asks, why, where the repo hits it, with counts) and a Recommended line.
- **Loops for the user's own conventions** ask "anything else?" after every answer, "default" included; only "no" or "skip" ends them. The 12-question limit and the single open question are gone.
- `dk:init standards [rules|review]` reruns one pass (replaces `[topic]`).
- **Checked** with one run on a real Angular repo: 14 standards questions, 0.60 USD; three deviations found there and fixed (docs 06).

## 1.3.0 (2026-10-15)
- **`dk:init` topic questions end with a Recommended line:** the agent's best pick for the repo (kit files, items to switch off, suggested rules with scope), one reason per part from the probe. An `experimental` kit file is recommended when the probe finds the situations its items cover; items the linter or compiler already checks are left out; a suggested rule is recommended only with a clear usage direction and no fact still needed from the user; a lint rule is preferred when a linter could enforce it. With nothing qualifying it says `Recommended: nothing` and why.
- **"default" now accepts the Recommended line** (was: `validated` files only, no suggested rule, which in practice enabled nothing since every kit file is still `experimental`). "skip" enables nothing; drafted rules are still read back before writing.
- **Checked** on a real Angular repo: architecture → `Recommended: nothing` (every suggestion needed a fact from the user); coding → `coding/review-basics (experimental)` plus a subscription-cleanup project rule backed by counts; `: any` (480 uses, no linter) was not recommended. A first run recommended a rule "if I had to pick" that still needed confirmation; the rule was tightened and the rerun was clean.

## 1.2.4 (2026-10-15)
- **`dk:init` explains an empty kit checklist:** on a topic with no kit file (`architecture`, `api`, `data`, `ops`, `process`) it says in one line that the kit writes a rule only when the agent cannot learn it from the code or keeps failing at it (principle 0), and that this topic's rules come from the probe suggestions. Checked with one `dk:init standards` run on a real Angular repo.
- **No kit `architecture` file, by decision:** a draft (layers, adapters, contracts, config) was reviewed against principle 0 and dropped: most items are readable from neighbouring code, and no confirmed backtest bug backs them.

## 1.2.3 (2026-10-15)
- **Cursor support dropped:** removed `.cursor-plugin/plugin.json` and `harness/cursor.md`, dropped `cursor` from the Harness section of the 5 controllers and from `.version-bump.json`, and listed Cursor under "Not supported" in the READMEs, `harness/README.md` and docs 05.
- **Why:** it was never verified: `cursor-agent` needs a login that the test machine did not have. The probe results in docs 06 stay as history.

## 1.2.2 (2026-10-15)
- **`dk:init` defaults are explicit:** "default" enables `validated` kit files only, never ticks an `experimental` one, and keeps no suggested rule; a rule is written only when the user keeps it by name.
- **Evidence in suggestions:** every count comes from a command the agent ran; a direction such as "X replaces Y" without usage evidence is asked as a question.
- **Tests that cannot run** (restore, authentication, missing service) are not a red baseline: the agent asks whether to stop or continue with `baseline: not-measured` (new key in `templates/config.yml`: `green`, `known-failures`, `not-measured`).
- **Kit standards reviewed against the docs 09 criteria** (the kit owner delegated the review on 2026-10-15): each file now cites the backtest bugs behind its items, and `ui/forms-and-actions` U3 is reviewed only for async views or write actions the diff adds (less noise). All four stay `experimental` until measured on new bugs.
- **Measured:** `dk:init` on 3 real repos (two Angular micro-frontends, one .NET API): 8–10 questions (3–4 on standards), `git status` unchanged; 6 of 7 checked claims right; the deviations above were found there and fixed (docs 06).

## 1.2.1 (2026-10-14)
- **The `CONSTRAINTS.md` question explains itself:** what the file is (a pass bar as numbers with the command that checks each, a floor, exceptions), how it differs from the standards just chosen, what `dk:pre-pr-check` already flags without it, what it would add for this repo (from the probe), its cost (up to 4 more questions, maybe a tool to install) and that its benefit is unmeasured. Docs 03 gets a "`CONSTRAINTS.md` versus standards" table.
- **In-house library rules ask the design's follow-ups** (docs 09, 9.6): whether the old version is still allowed in new code and which framework controls stay allowed, in the same topic question.
- **History check:** the per-topic `dk:init` existed only in the design (docs 09) and notes before 1.2.0; no earlier `skills/init/SKILL.md` had topic questions, so nothing was lost when the public repo was created.
- **Verified:** asked alone in a real worktree, the `CONSTRAINTS.md` question listed what the repo already checks (type check, coverage run, Sonar, CI) and what is missing (no lint gate, no coverage threshold for changed lines).

## 1.2.0 (2026-10-14): merged `dk:init` with the standards checklist, one question at a time
- **`dk:init` follows the approved design (docs 09, 9.2 and 9.6).** It probes first, then asks one question per message in a fixed order: graph tools (only if missing), commands and base branch, graph indexes, baseline (only if red), standards by topic, an open question, the read-back of drafted rules, `CONSTRAINTS.md` (optional). Each question carries its evidence and a default. This replaces 1.1.0's single plan-and-approve step.
- **Standards by topic:** `architecture`, `coding`, `testing`, `security`, `ui`, `api`, `data`, `ops`, `process`, skipping topics with nothing to offer. Each topic shows the kit checklist (every item, `validated` pre-ticked, `experimental` not), rules suggested from the code with evidence (in-house libraries, central services, permission sources) with a project or team scope, and an "add another convention" option. At most 12 standards questions; no naming or style questions (principle 0). Drafted rules are read back before they are written; team rules go to a team folder remembered in `~/.dev-kit/config.yml`.
- **Re-run one part:** `dk:init index`, `dk:init baseline`, `dk:init standards [topic]`.
- **Kit standards set** (all `experimental`, waiting for the kit owner's approval and for measurement on new bugs): `coding/review-basics`, `security/web` (OWASP Top 10:2025, ASVS 5.0), `testing/basics`, `ui/forms-and-actions` (WCAG 2.2), alongside `review/finding-quality`.
- **Verified (Claude Code, Sonnet 5.5, a fresh worktree of a private Angular repository, one answer per turn with `--resume`):** 9 questions, one per turn, in order; the `ui` question found the in-house component library from the code (110 files on v2, 7 on v1, 36 templates with framework controls) and proposed a project rule; the drafted rule was read back before writing; `git status` unchanged; `check_report.py` accepts the new rule ids. Two deviations fixed afterwards: a kit checklist listed only 3 of 5 items, and the `CONSTRAINTS.md` question was folded into the read-back.

## 1.1.0 (2026-10-14): `.dev-kit/` is personal, `dk:init` asks once
- **Nothing dev-kit writes is committed (rule O1).** `dk:init` creates `.dev-kit/.gitignore` containing `*`, so the whole folder stays out of git. It no longer asks what to commit and never edits the repo's `.gitignore`; index folders that still show in `git status` (codegraph keeps its own `.gitignore` visible) go to `.git/info/exclude`.
- **`dk:init` prints one plan with defaults** (commands, graph indexes, no `CONSTRAINTS.md`) and needs one approval; it asks separately only for a missing tool or a red baseline. It ends by checking that `git status` is unchanged.
- **Parts no longer write tracked files:** `domain-modeling` writes new terms and ADRs to `.dev-kit/GLOSSARY.md` and `.dev-kit/adr/`, `constraint-driven-development` writes `.dev-kit/CONSTRAINTS.md` and never edits `CLAUDE.md`/`AGENTS.md`; the project's own files are read and changes to them are proposed. `dk:pre-pr-check` step 1 checks the diff against `CONSTRAINTS.md` when one exists.
- **Worktrees:** `using-git-worktrees` ignores the worktree folder in `.git/info/exclude` instead of committing `.gitignore`, and copies `.dev-kit/` (minus `reports/`, `sdd/`) into the new worktree so config, baseline, standards, specs and plans are there.
- **Verified (Claude Code, Sonnet 5.5, a throwaway repo):** `dk:init` left `git status` unchanged and the repo's `.gitignore` untouched (a first run exposed the codegraph case, fixed above); the worktree part produced a worktree with the copied `.dev-kit/` and a clean `git status` in both checkouts.

## 1.0.0 (2026-10-14): first public release
- **Skills:** `dk:init` plus 4 controllers (`dk:story-runner`, `dk:bug-fixer`, `dk:code-refactor`, `dk:pre-pr-check`), 16 parts copied from Superpowers, mattpocock/skills and agent-skills (`UPSTREAM.md`), 2 review agents.
- **Rules with evidence** (`rules/RULES.md`), layered standards (kit, team, project), optional graph tools, and a machine check of `pre-pr-check` reports (`scripts/check_report.py`).
- **CLIs:** Claude Code (reference), Codex, Copilot CLI, Antigravity, OpenCode, omp; Cursor not verified (`harness/`).
- **Docs:** English source with Vietnamese, Simplified Chinese and Japanese translations; `scripts/check_i18n.py` and CI keep them in step.

## Pre-release lab iterations (0.2.0–0.8.14, not published)

These versions were developed in a private lab before the first public release. They are kept because the rules and docs cite them as evidence.

### 0.8.14 (2026-10-14): multilingual docs, ready to publish
- **English is the source** of every human doc: `README.md` and `docs/en/`. The docs were rewritten from Vietnamese and stripped of private data (company and repo names, internal PR and bug numbers, local paths); measured numbers and conclusions are unchanged.
- **Translations by tier** (`docs/i18n.json`): Vietnamese for tiers 1–2, Simplified Chinese and Japanese for tier 1 (`README.<lang>.md`, `docs/<lang>/`). Chinese and Japanese are machine translations (`review=machine`) until a native speaker reviews them.
- **`scripts/check_i18n.py`:** reports missing translations, a wrong or missing header, code blocks that differ from the source, broken links, and stale translations (warning; error with `--strict`). CI (`.github/workflows/docs.yml`) runs it with `check_parts.py` and `bump_version.py --check`.
- **`CONTRIBUTING.md`** (translation guide), root **`LICENSE`** (MIT).
- **Script comments and messages in English.** `check_report.py` still matches Vietnamese wording in reports ("thiếu test", "tiết kiệm"), since agents may write reports in the user's language.

### 0.8.13 (2026-10-14)
- **pi support paused:** removed `harness/pi.md` and `package.json` (the `pi` field). Dropped `pi` from the Harness section of the 5 controllers and from `.version-bump.json`.
- **Why:** pi 1.0.2 installs and loads the kit, but core pi has no subagent tool, so every review role would have to run in the main session. That way of running is not measured yet. To re-enable: restore the two files from 0.8.12, then measure with a backtest, possibly together with the `pi-subagents` package.

### 0.8.12 (2026-10-14): many CLIs, the Superpowers way
- **Harness section at the top of the 5 controllers:** if a CLI does not substitute `${CLAUDE_PLUGIN_ROOT}`, the kit directory is two levels above `SKILL.md` (after resolving symlinks); the agent reads `harness/<cli>.md`. On Claude Code the variable is still substituted, so behavior is unchanged.
- **`harness/`:** notes for Claude Code, Codex, Copilot CLI, Antigravity, OpenCode, omp, pi, Cursor. Each file records how to install, where the install lives, the subagent tool name, and how to call the two review agents.
- **New manifests:** `.codex-plugin/plugin.json`, `.agents/plugins/marketplace.json` (`local` source), `.cursor-plugin/plugin.json`, `.antigravity-plugin/plugin.json`, `package.json` (`pi` field). Copilot and omp read the existing `.claude-plugin/`.
- **`scripts/bump_version.py` + `.version-bump.json`:** change the version of every manifest in one step; `--check` reports drift.
- **No Gemini CLI support** (Google moved free-tier users to Antigravity CLI on 2026-06-18).
- **Verification:**
  - Probe with a fake plugin on 7 CLIs: only Claude Code substitutes the variable; all 7 give the agent the path of `SKILL.md` and can read files two levels above it. The subagent tools are `Agent`, `spawn_agent`, `invoke_subagent`, and `task` (Copilot, OpenCode, omp); core pi has none.
  - Real dev-kit install: all 7 CLIs find the kit directory and `rules/RULES.md`; the 6 non-Claude-Code CLIs read their own notes file correctly. Cursor not checked (needs `cursor-agent login`).
  - Backtest of a sort-bug PR (PR A): Codex ran the full flow (graph, 4 reviewer subagents, `check_report` passed) and caught the sort bug in the suspect tier; Claude Code 0.8.12 passed `check_report`, sort bug "partial" (1 run).

### 0.8.11 (2026-10-14)
- **`check_report.py` checks rule ids against real standards files:** an id cited in the certain tier (a token of the form `topic/name` or `topic/name#X`) must appear in the frontmatter `id:` of a kit standard (`dev-kit/standards/`), a project standard (`.dev-kit/standards/`) or a team standard (`standards.team` in `.dev-kit/config.yml`). If not found, FAIL (rules T1, R7). A spec counts only when it points to a specific place (`specs/…`, `§`, a section number).
- **Why:** after 0.8.10, an agent could still invent a well-formed id to keep a missing-test finding in the certain tier.
- **Verification:** 6 synthetic cases (project id, invented id, team id via config, spec path, `finding-quality#R1`, a real rule for a missing-test finding) gave the correct results; 17 existing backtest reports gave results identical to 0.8.10.

### 0.8.10 (2026-10-14)
- **`check_report.py`, the Rule column must hold a real rule:** only a standard id (form `topic/name#X`, rule T1) or a spec counts as "has a rule". Writing `R1`…`R7` or `review/finding-quality` no longer exempts a missing-test finding, because those are conditions for raising a finding, not rules that demand tests.
- **Why:** in the sort-bug PR backtest (0.8.9), all 6 "certain" findings were missing tests and the Rule column said `R1`, so `check_report` passed them.
- **Check on 16 existing reports:** that report now FAILs 5 of 6 findings; the remaining one says an existing test "does not assert" the behavior, and is correctly exempt. Reports that passed before still pass. The Graph-line check (0.8.8) also caught one skipped `detect-changes` in an iteration of another PR (PR C, 0.8.5).
- **Verification (sort-bug PR backtest, 1 run):** the agent got FAIL, moved the missing-test findings down to suspect, and fixed the report until it passed; the certain tier kept 1 minor finding; the sort bug was still caught in the suspect tier.

### 0.8.9 (2026-10-14)
- **`check_report.py`, test findings by location:** a "certain" finding that cites no rule and only points at a test file (`*.spec.*`, `*.test.*`, `tests/`, `test_*.py`) now FAILs and must move to suspect. Exempt when the finding says the existing test is wrong, that is, it passes even when the code is broken ("still passes", "never asserts", "passes vacuously", "accepts any"…).
- **R1 "Do not flag":** separates "missing test" (do not flag) from "a test exists but passes even when the code is broken" (a defect; must explain why it still passes).
- **Why:** in the sort-bug PR backtest (0.8.8), 2 missing-test findings slipped into the certain tier by wording such as "No service spec covers…", "Only 404 … is tested"; a wording-based regex missed them.
- **Check on 15 existing reports:** only those 2 findings FAIL; findings about wrong tests (the double-submit PR, PR B; the iterations of PR C) still pass.

### 0.8.8 (2026-10-14)
- **`check_report.py` checks the Graph line against reality:** when run in a repo with `.code-review-graph/`, the Graph line must contain a `detect-changes` summary or "detect-changes failed: <error>". Writing "no .code-review-graph/ index" or leaving the summary empty FAILs (rule G1).
- **`pre-pr-check` step 2:** check the index with `test -d "$(git rev-parse --show-toplevel)/.code-review-graph"`, not by inference from another listing. Added wording for when the command fails; `templates/report.md` updated to match.
- **Why:** in the sort-bug PR backtest (0.8.7), the agent only ran `ls .dev-kit .codegraph`, concluded there was no index, and skipped `detect-changes`; the old `check_report` still passed it.
- **Verification (sort-bug PR backtest, 1 run):** the agent ran `detect-changes`, the Graph line had a real summary, the report passed; the sort bug was still caught in the suspect tier.

### 0.8.7 (2026-10-14): standards framework (step 2 of the 0.9.0 design)
- **Rule T1:** the controller loads kit standards (`standards.kit` in config), team standards (`standards.team`) and project standards (`.dev-kit/standards/**`), filtered by `applies_to`, skipping ids in `standards.disable`; on conflict project > team > kit.
  - When planning it uses `## Design`, when writing code `## Implement`.
  - When reviewing, each reviewer gets the standards for its own topic (`## Review`, `## Do not flag`, `## Severity`) and cites the rule code.
- **`templates/standard.md`:** template for a standards file. `templates/config.yml` gains the `standards` key.
- **Experiment (a real Angular repo, worktree, Sonnet):** project rule "use the in-house v2 control set instead of Material", running `dk:story-runner` on one dialog-form card, 2 runs per side.

  | | With rule | Without rule |
  |---|---|---|
  | Material tags | 2 and 0 (the 2 are the allowed part: the dialog container) | 18 and 16 |
  | In-house control tags | 6 and 10 | 0 and 0 |
  | Tests | green | green |
  | USD | 0.46–0.53 | 0.37–0.39 |

  Without the rule, the agent copies neighboring components that still use Material. With the rule, it uses the right in-house controls and the report cites the rule code. **This is the first rule measured as clearly useful**, and it is the right kind: something "the agent does not know by itself" (principle 0).
- **Backtest of two PRs merged from two parents (the sort-bug PR A and the double-submit PR B), diff scoped correctly:** PR A's sort bug was caught in the suspect tier (missed before); PR B's double-submit bug was still missed. False findings caused by a broad diff are gone. PR B's certain tier was correct 3/3 (self-checked by an agent). In one run the agent wrongly concluded "no graph index" and skipped `detect-changes`; `check_report` could not catch this case yet.

### 0.8.6 (2026-10-14)
- **`check_report.py --base <base branch>`:** a certain-tier finding must point to a file in the diff, and at least one line must fall inside the changed code (±5 lines). Otherwise it may be pre-existing code (violates R1). `pre-pr-check` step 6 already passes `--base`.
- **Limit:** it cannot catch new code that reuses a pattern already present in the repo.

### 0.8.5 (2026-10-13)
- **`scripts/check_report.py`:** machine-checks a `pre-pr-check` report:
  - a Review setup section with all 3 lines; review depth is not lowered because of cost;
  - the confidence score matches the tier (certain ≥ 80, suspect 50–79, below 50 dropped);
  - no "missing test" in the certain tier when there is no rule;
  - the verdict matches the number of certain-tier blockers.
- **`pre-pr-check` step 6:** must run the script and fix the report until it passes (at most 3 times).
- **Why:** of 6 backtest reports from 0.8.4, 3 broke the R1 gate despite written guidance.

### 0.8.4 (2026-10-13): step 1 of the 0.9.0 design (enforced compliance + finding quality)
- **`standards/review/finding-quality.md`** (rule R1): 7 conditions for raising a finding (caused by the change, fixable, names the affected place, states the condition under which it happens, not intentional, not under Do not flag or something the linter already catches, cites a rule code); confidence score 0–100; **certain** (≥ 80) counts toward the verdict, **suspect** (50–79) is listed separately and does not block merge.
- **`pre-pr-check`:**
  - runs `detect-changes` **first**; the result is a required input for every reviewer;
  - measures the diff before choosing the review level; **does not lower the level for cost**;
  - when merging findings, applies the R1 gate and splits the two tiers.
- **`templates/report.md`:** a required **Review setup** section (depth with reason, graph summary, standards used); two finding tables with columns for confidence score, trigger condition, and rule code.
- **Rule C2:** added "do not lower the level for cost; to lower it, ask the user".

### 0.8.3 (2026-10-13)
- **Usable right after install, no reload.** Verified: an agent installs in one command and the next Bash command can call `codegraph` and `code-review-graph`. dev-kit uses CLIs, not MCP, so Claude Code does not need a restart.
- **`install-graph-tools.sh` also searches outside PATH:** on a fresh machine without `~/.local/bin` in PATH, the script prints the absolute path with an `export PATH` command. Playbook §1 tells the agent to call by that path.

### 0.8.2 (2026-10-13): fixes after a trial on a real repo
- **Paths in controllers:** use `${CLAUDE_PLUGIN_ROOT}/…` (Claude Code replaces it with an absolute path) instead of `../../…`. On a real repo, the agent resolved `../../rules/` against the current directory, so it could not read `RULES.md` and the playbook, and skipped `detect-changes`.
- **Rule C2:** "personal data" includes medical/patient data. An earlier review of a PR about patient prescriptions picked only 1 reviewer.

### 0.8.1 (2026-10-13): pre-existing red test baseline
- **`dk:init`:** if the baseline is red, ask whether to stop or to accept the failing tests as a known baseline. If accepted, write `.dev-kit/baseline.md` following `templates/baseline.md`.
- **All controllers:** the check fails only when a test outside that list fails (rule B1). A newly failing test is a blocker; a test that was fixed is reported separately.
- **Why:** a trial on a real repo (a private Angular micro-frontend, 9,569 specs) had 290–303 specs failing from the base branch already. Without this rule dev-kit could not run.

### 0.8.0 (2026-10-13): graph tool playbook
- **`rules/graph-playbook.md`:** gathers how to use codegraph and code-review-graph by purpose:
  - §1 update the index;
  - §2 find code;
  - §3 blast radius;
  - §4 existing tests (CRG `tests_for`);
  - §5 refactor support (large-functions, rename preview, dead-code);
  - §6 module diagram;
  - §7 review (`detect-changes`, long functions, new code nobody calls).

  Take only the summary (`jq -r '.summary'`).
- **Wired into 12 places:**
  - 4 controllers;
  - the parts: `systematic-debugging`, `diagnosing-bugs`, `test-driven-development`, `verification-before-completion`, `codebase-design`, `writing-plans`, `code-review`, `requesting-code-review`.
- **Fix:** `codegraph affected` did not find Python tests in the lab, so Python now uses CRG `query tests_for`.
- **Lab (17 SWE Django runs, Haiku, with index):**
  - 0.8.0 solved 12/17 at 0.031 USD/run;
  - 0.7 with index 10/17 at 0.034; 0.7 without index 10/17 at 0.033.
  - No extra cost; +2 problems is not enough to conclude, since results swing both ways.

### 0.7.1 (2026-10-13)
- **`scripts/install-graph-tools.sh`:**
  - `--check` reports the status of both tools;
  - `--install` installs pinned versions of whatever is missing: codegraph v1.5.0 through the official `install.sh` (pinned by tag), code-review-graph 2.3.9 through `pipx`, or `uv tool` if pipx is absent;
  - a tool that is already present is left alone, because codegraph's `install.sh` removes other versions.
- **`dk:init`:** calls this script. If a tool is missing it asks once, then runs `--install`. It never runs `codegraph install` / `code-review-graph install`.
- **`dk:init` builds both indexes by default** (part of the approved plan). On a large repo it reports the size first and asks.
- **If not installed:** everything else runs as before; only rule G1 is off (noted in the init report).

### 0.7.0 (2026-10-13): wiring in graph tools
- **Rule G1:** when the repo has `.codegraph/`, the controller runs `codegraph sync`, then uses `explore`/`callers`/`impact` to find code and `affected` to pick tests to run first. When it has `.code-review-graph/`, `pre-pr-check` runs `update` + `detect-changes --brief --base <base>` once and gives the summary (risk, test gaps, functions without tests) to the reviewers. CLI only: no MCP, no hooks, no instruction files.
- **`dk:init`:** builds the index with your consent, adds the two directories to `.gitignore`, writes `graph.*` in `config.yml`.
- **Lab measurement:** neutral.
  - 17 SWE Django runs, Haiku: 10/17 solved both with and without the index; same cost.
  - The agent used grep about half as often.
  - Kept optional (only active once an index is built).

### 0.6.0 (2026-10-13): standardized input/output
- **One place for output (rule O1):** everything dev-kit writes lives in `.dev-kit/`. The SDD ledger moved from `.superpowers/sdd/` to `.dev-kit/sdd/`. Deliberate exceptions: `GLOSSARY.md`, `docs/adr/`, `CONSTRAINTS.md` (the project's own documents).
- **One severity scale (rule S1):** blocker / major / minor for every reviewer (the SDD reviewer prompt and requesting-code-review, `code-review`, `security-auditor`, `test-engineer`); with a mapping table.
- **Templates:** `templates/spec.md`, `templates/report.md`, `templates/config.yml`; the controllers and `dk:init` use them.
- **`code-review`:**
  - looks for the spec in `.dev-kit/specs/` first;
  - dropped Matt's tracker dependency (`docs/agents/issue-tracker.md`, `/setup-matt-pocock-skills`);
  - self-review mode and the reviewer role do not spawn sub-agents (before, it always spawned 2).
- **`constraint-driven-development`:** asks before adding a line to `CLAUDE.md`/`AGENTS.md`.
- **`config.yml`:** added `commands.check`; controllers prefer `check`, then `test`.
- **Rule F2:** wait for subagents within the same turn (no ScheduleWakeup/Monitor/cron); the final answer states the work done, the verdict and the report path.

### 0.5.2 (2026-10-13)
- pre-pr-check: measure the diff with `git diff --shortstat` before choosing the review level (lab: P3 had 10 files / 170 lines but the agent self-reviewed instead of using 1 reviewer).

### 0.5.1 (2026-10-13)
- story-runner: asks the user one question at a time; records decisions in the spec's Decisions section (dropped the lab's `LAB_DECISIONS.md`); uses the `domain-modeling` part when there are new terms.
- pre-pr-check: fixes blockers following the `receiving-code-review` part; PR body follows the `pr` part.
- code-refactor: behavior suspected to be a bug goes into the report.

### 0.5.0 (2026-10-13)
- Split out of the lab as its own plugin: plugin name `dk`, repo `dev-kit`. Renamed from `devflow`: skill `devflow-init` → `dk:init`, artifact directory `.devflow/` → `.dev-kit/`.
- Controllers read `commands` and `base_branch` from `.dev-kit/config.yml` if present.

### 0.4.1 (2026-10-13)
- Rule C2: four reviewers only on request or for auth/permissions, secrets, personal data, migrations, config/env. Pricing code is no longer a trigger (v0.4.0 ran four reviewers on almost every card).

### 0.4.0 (2026-10-13)
- Thin controllers: direct path by default; parts read only when needed.
- `rules/RULES.md`: each rule with status and lab evidence. On: F1 flow ownership, C1 direct path, C2 review depth by risk. Off (experimental): Q1 sibling check (overfit), Q2 ADR-first (no measured effect).
- pre-pr-check: three review depths (self / one / four).
- Every controller writes a short human report in `.dev-kit/reports/`.


### 0.3.0 (2026-10-13)
- Lean by default: bug-fixer works in-session (no reproducer/fixer subagents); story and refactor size the work, SDD only for large work.
- pre-pr-check: lean review (1 reviewer) unless risky (auth, money, personal data, secrets, config, migrations, > 400 lines) or asked; then 4 reviewers.
- "Controller owns the flow": parts cannot stop the controller (lab round 2, Matt B3 stall).
- Sibling check for new fields/params (lab round 3, SWE 16560 `__repr__` miss).
- Story: read docs/ADRs first; newest accepted decision wins.

### 0.2.0
- Dangling references fixed; parts not registered as skills.
