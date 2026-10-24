# Step 7: standards interview

Read at step 7 (and `dk:init standards [rules|review]`), before the probe, in both quick and detailed setup.

## Contents

- [Principle 0](#principle-0)
- [Probe first, no questions, graph first](#probe-first-no-questions-graph-first)
- [How each question looks](#how-each-question-looks): the list in detail, Recommended, answers, items the user adds, read-backs, numbering
- [Pass 1: rules for writing code](#pass-1-rules-for-writing-code-design-implement)
- [Pass 2: review checklist](#pass-2-review-checklist-review-do-not-flag-severity)
- [Question limit and headless runs](#question-limit-and-headless-runs)

## Principle 0

Rules are written only for what the agent **cannot know by itself** or has been seen to get wrong (principle 0, `docs/en/09-init-and-standards.md`). Never ask about naming or style: the agent reads it from neighbouring code, and the linter checks the rest.

## Probe first, no questions, graph first

When step 5 built the indexes (`graph.codegraph` / `graph.crg` true), find the structure with the graph before reading files (rule G1, `${CLAUDE_PLUGIN_ROOT}/rules/graph-playbook.md`); grep and file reads are for what the graph cannot answer. Run once, in this order:

1. Freshness: `codegraph sync` and `code-review-graph update -q`.
2. **Areas of the code:** `code-review-graph architecture --detail-level minimal`: the communities (name, size) and warnings are the starting list for the architecture group.
3. **Central pieces, by topic:** `codegraph explore "<topic>" --max-files 5` for each of: how the backend is called (HTTP or data access), permission or role checks, configuration and environment values, shared base classes or helpers, personal or medical data.
   - Its "Blast radius" lines give symbols with caller counts (for example "`<permission key map>` — 93 callers"): use those counts as evidence.
   - Follow one symbol with `codegraph callers <symbol>` or `codegraph node <symbol>`; these work on symbols defined in the repo, not on framework classes (`codegraph callers HttpClient` finds nothing).
4. **Then files and grep, only for what the graph does not hold:**
   - what the linter and compiler already enforce (their configs; reviewers must not report it again);
   - in-house libraries: internal-scope packages in `package.json` (old and new versions), how many files import each, template tag prefixes against framework controls (`mat-*` and similar), which one recent files use, and the component list from the package's `public-api.d.ts` / `index.d.ts`;
   - what the repo exposes to others (public API, federated remotes, events) when the graph did not show it.

Without indexes, do steps 2–4 with files and grep. In `init-report.md`, list the graph commands you ran.

## How each question looks

One **group** per question, like a brainstorm: one question per message, multiple choice where possible, wait for the answer.

### The list in detail

- Every item with its ID, what it asks of the code, why, and where this repo hits it (a count or a file from a command you ran).
- Say for each item whether it applies to this stack (the stack found in step 3: a web front end, a mobile app, a back-end service): a kit file is offered when its `applies_to` matches the repo, whatever the platform, so mark an item that does not fit (a server-side check in a client app) as "does not apply here" with the reason, and name the stack's equivalent of a platform term (`localStorage` is `AsyncStorage` in React Native).
- Mark each kit file `validated` or `experimental`.
- A claim such as "X replaces Y" needs usage evidence (recent files use X, or X is used more than Y); otherwise it becomes a choice (`A: shared/services` / `B: services`).

### Recommended

One line the user can accept as is, one reason per part from the probe.
- Recommend an `experimental` kit file when the probe found the situations its items cover; leave out items the linter or compiler already checks or nothing in the repo triggers (for example an item about server-side checks in a front-end repo); recommend a repo item only when usage shows a clear direction and no fact is still needed from the user; prefer a lint rule when a linter could enforce it.
- "All items" is a choice, not a default: recommend it only when the list above shows repo evidence for every item.
- The line is one decision, never "if I had to pick"; with nothing qualifying, write `Recommended: nothing` and why.
- Before sending, check the line against the text above it: every item the text recommends is in the line, and nothing else.

### Answers

- "default" (`A`) accepts the Recommended line exactly as shown; "skip" takes nothing from the group; "Other" takes items one by one (letters or IDs, `<id>#<item>` to switch off one kit item) or free text.
- Never enable a file or keep an item that was not on the screen.
- Never ask whether an item is for the project or a team: everything kept belongs to this repo.

### Items the user adds

**Confirm every item the user adds in their own words** (a convention, a review check, a Do-not-flag line), in any group or loop, before keeping it. Make it its own question, then continue where you were:
- **How you understood it,** drafted as the item will be written: the trigger ("When X, …"), what it asks, where it applies (folders, kinds of file, new code only or existing code too), exceptions, the severity;
- **How it fits this repo,** from commands you ran: how many places follow it today and how many do not, with one example of each; anything it conflicts with (a kept rule, a framework or library default, a neighbouring pattern such as a second base class); whether a linter, the compiler or a kept rule already covers it (name the config), or whether the agent already sees it in neighbouring code (principle 0); and whether a reviewer can check it at all: `dk:pre-pr-check` sees the diff, the spec and the graph summary, not the PR description, CI results or screenshots, so say so when the item depends on them;
- **The question:** "Is this what you mean?" with choices: `A` yes, as drafted; `B` narrower (a concrete proposal, for example "new master tables only", or a version a reviewer can check from the diff); `C` wider (a concrete proposal); or a correction in their words. When the evidence shows no gap (it matches the code and nothing conflicts), say so in one line, and keep the choices.

Keep the item only after the answer, under the ID shown in the confirmation (never renumber it when writing); on a correction, draft and confirm again.

### Read-backs

- Read-backs are their own message and show what will be written: every drafted repo item in full (ID, trigger, what it asks, severity, file), the kit files kept and the items switched off. Never "as above" without the list.
- Nothing else is asked in it (not the next group, not `CONSTRAINTS.md`).
- Wait for the answer and write only after a yes. Never decide an answer for the user: no reply is not a "no".

### Numbering

Skip a group with nothing to show. Number the questions ("Question 9 — rules: coding").

## Pass 1: rules for writing code (`## Design`, `## Implement`)

Used by `dk:story-runner`, `dk:bug-fixer` and `dk:code-refactor` while writing code. Groups, in order:

1. **Architecture**, from the probe: the kit has no architecture file (principle 0: it depends on the repo), so the probe is the standard list.
   - Present the structure as items to confirm: layers and where new code goes, how data is reached, the module system, exposed contracts, config and environment values, permission keys. Each item is a candidate rule with its evidence.
   - Keep out of Recommended what an agent sees by reading neighbouring code (where an existing kind of file already lives, a pattern every file follows); recommend placement only when two places compete or recent files moved.
2. **One group per kit file** with `## Design` or `## Implement` items whose `applies_to` matches the repo: `coding/review-basics`, `testing/basics`, `security/basics`, `ui/forms-and-actions`. Show the items of those sections only.
   - **Not offered when the trigger is absent:** before listing a file's items, look for each item's trigger (its "When …" condition) in the repo with a command (graph or grep), for example server handlers for a server-side check, HTML, URL or WebView sinks and shell or query calls for an injection check, a test runner for the testing items.
   - An item whose trigger a command shows to be absent is not a row and not part of Recommended: list it in one line under the table, "Not offered, no trigger in this repo: S1 (no server handler: `<command>`, 0 files), …", and it goes to `standards.disable` if the file is kept.
   - Keep an item as a row when its trigger needs reading code (what an error message shows, what is stored where, whether a secret ships) or the command is not conclusive: a grep finding nothing is not proof there.
   - The user brings a not-offered item back through Other. A kit file with no offered item is skipped with that one line.
3. **In-house libraries**, one group each: draft the rule from the probe (Implement, Review, Do not flag, with the component list) and ask only what the code cannot show: is the old version still allowed in new code, and which framework controls stay allowed (the `Do not flag` exceptions).
4. **Your own conventions (loop):** list the other repo suggestions the probe supports, each with its evidence, as choices, plus free text. Ask again after every answer, "default" included (it takes the Recommended line), until "no" or "skip". Never ask a bare "anything else?"; build each loop question from the context, in the user's language:
   - one line on what was just added (or "nothing added");
   - what the kept rules cover so far, by area, in a few words;
   - at most 3 new areas of this repo that no kept rule touches yet, each with its evidence from the probe (a folder, a dependency, a flow with its file count); areas offered before are listed by letter only;
   - **one question sentence** that names those areas, for example: "Rules so far cover permission keys, environment values and translations; nothing yet on date handling (`<date library>` in N files) or the report screens (N files under `<folder>`). Is there a convention there, or anywhere else, the agent should follow when writing code?";
   - how to end ("no"). Any claim that a linter or the compiler already covers something names the config that shows it.

   When the probe has no uncovered area left, say so and ask once whether the team has a convention the code does not show.

Then **read the pass-1 rules back** (drafted repo rules and kit choices) as their own question; write only after the user confirms.

## Pass 2: review checklist (`## Review`, `## Do not flag`, `## Severity`)

Used by `dk:pre-pr-check` and its reviewers. Do not ask again about items kept in pass 1: each one is checked in review at its severity. Open with one line saying so, and that `review/finding-quality` (the finding gate, R1–R7 and the certain/suspect tiers) is always on. Groups, in order:

1. **Severity:** a table of the rules kept in pass 1, each with its severity (kit items show theirs; propose one for each repo rule from the probe: blocker when data is written wrongly or a contract breaks, major when a user sees wrong behavior, minor otherwise). The user may change a repo rule's severity; a kit item's severity changes only through a project rule that overrides it (`docs/en/09-init-and-standards.md` 9.3).
2. **Review-only checks:** what a reviewer checks that is not a rule for writing code, found in the probe as "when the diff touches X, check Y", for example: version pins that must match another file, generated or vendored files that must not be hand-edited, a migration that needs a rollback, a changed public contract whose consumers must be told.
   - Leave out any check that restates a rule kept in pass 1 (an environment value in every file, a translation key in every language): that rule is already checked.
   - Show each with the file count or path.
3. **Do not flag:** what the linter, compiler and CI already enforce (from the probe), the `## Do not flag` lines of the enabled kit files, and repo patterns that would only be noise (for example a legacy folder the team does not touch). The user adds or removes items.
4. **Your own checks (loop):** as in pass 1, built from the context, never a bare "anything else?": what reviewers will now check, by area; 2–3 kinds of change the checklist does not cover yet, with evidence (for example "changes under `<folder>`, N files; to the pipeline files"); then ask whether reviewers should check something there, or leave something alone. Ask again after every answer, "default" included; only "no" or "skip" ends the loop.

Then **read the pass-2 checklist back** as its own question; write only after the user confirms.

## Question limit and headless runs

There is no question limit; the loops end when the user says no. In a headless run, take each Recommended line, end the loops at once, and list the choices as assumptions in the report.
