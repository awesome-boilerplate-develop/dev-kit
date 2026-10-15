# 9. Design for 0.9.0: merged `dk:init`, standards by topic, finding quality, enforced compliance

> Status: **approved and built** (draft 2, 2026-10-13). Built in 0.8.4–0.8.11 (9.5, 9.7), 0.8.7 (standards framework, sample team rule) and 1.2.0 (merged `dk:init` with questions asked one at a time, kit standards set). Not yet measured: the kit standards on new bugs and the init questions on 2–3 real repos (9.8). Since 1.1.0, `.dev-kit/` is personal and never committed (rule O1), so the project tier lives in an ignored folder; a shared team mode is an idea in [08](08-roadmap.md).
> Background: the `pre-pr-check` backtest on 8 real bugs caught 1/8 and partly caught 3/8; the agent skipped `detect-changes` in 4 of 6 runs and once lowered the review level on its own (see [06](06-evidence.md)).

## 9.1 Goals

1. **Enforce compliance:** the agent performs every step that was designed.
2. **Finding quality:** fewer false alarms; every finding is verifiable and states the condition under which it occurs.
3. **Standards by topic:** only what the agent **cannot know by itself**, used both when writing code and when reviewing.
4. **One-command `dk:init`:** merge the machine part and the repo part; probe with the graph first, ask afterwards.

**General principle:** start small, measure, then expand. Add no layer that has not been measured.

## 9.2 Merged `dk:init`

```text
Machine part (skipped automatically when already done)
  1. Graph tools: install-graph-tools.sh --check
     - missing: ask once; if the user agrees, --install (pinned version)
     - not on PATH: use the absolute path the script prints
  2. ~/.dev-kit/config.yml: tool paths, team standards sets (ask once, reuse)

Repo part (each repo or worktree)
  3. Detect test/lint/build commands, base branch, enabled linters → .dev-kit/config.yml
  4. Build the index (on by default)                         → .codegraph/, .code-review-graph/
  5. Baseline (if red, ask whether to accept)                → .dev-kit/baseline.md
  6. Standards by topic (section 9.6)                        → .dev-kit/standards/, config.yml
  7. Report                                                  → .dev-kit/init-report.md
```

- **No reload needed after install:** checked; dev-kit uses CLIs, not MCP.
- **Re-run a single part:** `dk:init index` (new worktree), `dk:init baseline` (the list may only shrink), `dk:init standards [rules|review]`.

## 9.3 Standards

### Principle 0: do not write rules for what the agent already knows

A rule is written only when:
- **(a) the agent cannot know it** from the surrounding code, for example which control set the team uses, which service API calls go through, where RBAC keys come from; or
- **(b) there is evidence the agent fails repeatedly:** the lab, a backtest, or the dogfood log.

Anything the agent can discover from neighbouring code (naming, file structure, style), or that the linter and compiler already check, is **not written as a rule**. In the Review section it is only listed under `Do not flag`.

### Tiers (three tiers first)

| Tier | Lives in | Written by | Notes |
|---|---|---|---|
| kit | `dev-kit/standards/<topic>/` | dev-kit drafts, **kit owner approves**, lab measures | Common practice, kept short |
| team | `<team directory>/<topic>/` | The team | Example: a team that writes its own UI controls |
| project | `.dev-kit/standards/<topic>/` | Whoever works on the project | Specific to one repo |
| *(user)* | `~/.dev-kit/standards/` | An individual | **Later**, only when there is real demand |

- **On conflict:** project > team > kit.
- **Users do not edit the content of kit rules.** To adjust one, there are three ways:
  1. enable or disable the whole file;
  2. disable single items in `config.yml` (`disable: [coding/review-basics#C5]`);
  3. override with a team or project rule.

  If a kit rule looks wrong, give feedback so it is fixed in the kit.

### Topics

`architecture`, `coding`, `testing`, `security`, `ui`, `api`, `data`, `ops`, `process`. **Create a topic directory only when it has content.** A topic with no rules does not exist, and nobody has to read it.

### File format

```markdown
---
id: coding/review-basics            # <topic>/<short-name>, kebab-case
scope: kit                           # kit | team | project
status: experimental                 # experimental | validated
applies_to: ["**/*"]
references: Google Engineering Practices; Fowler – code smells   # optional, one line
---
## Design        # when writing a spec or plan (if any)
- …
## Implement     # when writing code
- C1 …           # every item has an ID: topic letter + number
## Review        # when reviewing
- …
## Do not flag   # what must not be reported for this topic
- …
## Severity      # blocker / major / minor thresholds for this topic
- …
```

- **Length:** each section a few lines, at most about 10–15 items; a budget of about 300–500 tokens per file.
- **`references`** only points to the source. It is optional, except for `security` and `ui` (accessibility): these two topics must cite the standard they are checked against (OWASP, WCAG).

### Quality criteria for a rule

| # | Criterion | Self-check question |
|---|---|---|
| 0 | The agent does not know it, or has been seen to fail | If this rule is removed, does the agent get it wrong? |
| 1 | Checkable on code or a diff | Would two reviewers reach the same conclusion? |
| 2 | Has a trigger condition | Can it be written as "When X, check Y"? |
| 3 | Not tied to a framework (for kit tier) | If the framework changes, is the rule still true? |
| 4 | Has a one-sentence "why" | Does the agent know when an exception is reasonable? |
| 5 | Low noise | How many warnings does it produce on a normal PR? |
| 6 | One rule, one idea, own ID | Can it be disabled on its own? |
| 7 | Has a default severity | Is a violation a blocker, major or minor? |

**Lifecycle:**

```text
draft → kit owner approves → experimental → measure on NEW bugs → validated
                                          └─ no help or too noisy → fix or drop
```

For `experimental`, `dk:init` suggests the file but does not pre-tick it. For `validated` (helped on new bugs in at least 2 projects), it pre-ticks the file when the stack fits.

### Initial kit set (small)

| File | Main content |
|---|---|
| `review/finding-quality.md` | The finding gate, shared by every reviewer (section 9.5) |
| `coding/review-basics.md` | Errors are not swallowed, async operations have an in-flight state, `null`/optional values have a handling path, logic matches places that do the same thing, follow neighbouring code patterns |
| `security/web.md` | Authorization checked on the exact object (IDOR), untrusted input, secrets, personal data (including medical) kept out of logs and client-side storage. References OWASP Top 10:2025, ASVS 5.0 |
| `testing/basics.md` | A bug fix has a reproducing test that goes red then green; tests of error branches must be able to fail; test behaviour, not implementation details |
| `ui/forms-and-actions.md` | Error messages have their own conditions, validators that can actually trigger, write operations do not run concurrently, loading and error states. References WCAG 2.2 for accessibility |

**No naming file:** naming falls under principle 0.

## 9.4 Which step reads which topic

| Step | Topics | Sections |
|---|---|---|
| `story-runner`: spec, plan | architecture, api, data, security | Design |
| Writing code (`story-runner`, `bug-fixer`, `code-refactor`) | coding, testing, ui, api, security | Implement |
| `pre-pr-check`: every reviewer | `review/finding-quality` | (all) |
| `pre-pr-check`: Standards reviewer | coding, architecture, process | Review, Do not flag, Severity |
| `pre-pr-check`: Spec reviewer | api, ui, data | Review, Do not flag, Severity |
| `pre-pr-check`: `security-auditor` | security | Review, Do not flag, Severity |
| `pre-pr-check`: `test-engineer` | testing | Review, Do not flag, Severity |

Load only files that are **enabled** and whose `applies_to` matches the file being edited or the diff.

## 9.5 Finding quality (shared gate)

Learned from the Codex review rubric, the official Claude Code `code-review` plugin, and Anthropic's `claude-code-security-review`.

A finding is raised only when:
1. **This change itself causes it**, not a pre-existing defect outside the diff.
2. **It is discrete and fixable,** and the author would want to fix it if they knew.
3. **It points to the affected place** (file:line, the caller side), not a guess.
4. **It states the condition under which it occurs:** input, scenario, environment. For security, the exploit scenario.
5. **It is not an intentional change** related to the purpose of the PR.
6. **It is not in the topic's `Do not flag`**, and not something the linter, compiler or CI already catches.
7. **If based on a rule, it cites the rule ID** (`team-a/ui-controls#U1`, `coding/review-basics#C3`).

**Two tiers:**
- **Certain:** confidence score ≥ the topic's threshold. Counts toward the verdict; a blocker means NO-GO.
- **Suspect, with a reason:** below the threshold. Listed separately, does not block merge.

This keeps subtle behavioural bugs (exactly the kind the backtest is missing) without turning them into blockers.

## 9.6 `dk:init` asks about standards: probe first, ask afterwards

1. **Probe the stack and linter.** Record what the linter already checks, so reviewers do not report it again.
2. **Kit topics:** suggest files that fit the stack. `validated` files are pre-ticked, `experimental` files are not.
3. **Team/project rules: ask only where the agent cannot know,** using the graph to guess in advance, with evidence. Examples:
   - ui: "68 files use `<ui-…>`, 4 files use `mat-input`. Does the team prefer its own control set?"
   - api: "Every HTTP call goes through `XxxRequestService` (`codegraph callers`). Record it as a rule?"
   - security: "Authorization goes through `rbacResourceKeys`. Is there a separate policy for patient data?"
4. **Two passes since 1.4.0** (was: one question per topic, ≤ 12 in total, one open question at the end). Pass 1 asks the rules for writing code (`## Design`/`## Implement`): architecture from the probe, then each fitting kit file, then in-house libraries, then a loop of the user's own conventions. Pass 2 asks the review checklist (`## Review`/`## Do not flag`/`## Severity`): severity of the kept rules, review-only checks that do not restate a rule, the Do-not-flag list, then a loop of the user's own checks. One group per question, each with its list in detail and a Recommended line; "skip" is a valid answer. Always ask the scope: project or team.
   - **Each loop asks again after every answer** "default" included; only "no" or "skip" ends it. Since 1.4.1 the question is built from the context (what was added, what the kept rules cover, up to 3 uncovered areas with evidence, one question naming them), never a bare "anything else?". There is no question limit.
   - The agent sorts free-form answers into the right topic and scope, writes them as rule items following the quality criteria (9.3), **reads them back to the user for confirmation** before writing. Any idea that violates principle 0 (the agent already knows it, or the linter checks it) is called out, and the agent suggests not writing it.
5. **Do not ask about naming or style:** that falls under principle 0.
6. **Auto-probe in-house control sets/libraries** (tried on a real Angular repo):
   - `package.json`: packages with an internal scope (for example `@<org>/components`, with both v1 and v2);
   - count the files importing each package, the tags per prefix in templates, and the use of framework controls (`mat-*`);
   - compare recent new files to see the trend (which set new code uses);
   - take the control list from the package's `public-api.d.ts` (or `index.d.ts`); no README needed.

   From this, draft a **draft rule** (Implement, Review, Do not flag) with evidence. The agent asks only what the code cannot show:
   - scope (team or project);
   - whether the old version is still in use;
   - which framework controls are still allowed (exceptions).

## 9.7 Enforcing compliance

1. **The report must have a `Review setup` section:**
   ```text
   Depth: <self | one | four> — reason: <C2 trigger | small diff>
   Graph: <detect-changes summary> | "no .code-review-graph/ index"
   Standards applied: <list of ids>
   ```
2. **Rule C2:** the review level must not be lowered because of cost; to lower it, the agent must ask the user.
3. **`pre-pr-check`:** run `detect-changes` **first** and give the result to each reviewer as required input.

## 9.8 Measurement

| Part | How to measure | Pass when |
|---|---|---|
| Compliance | Re-run the 6 backtest PRs (worktrees `devkit-bt-*`) | `detect-changes` runs 6/6; review level follows the rule 6/6; the number of bugs caught does not drop |
| Finding quality | The same 6 PRs: you mark each finding correct or false | Correct rate in the "certain" tier ≥ 70%; no already-caught bug lost |
| Kit rules | **New** bugs, not used to draft the rules | More caught than with the rules off; noise rises only slightly |
| Team rule (a team's own control set) | One UI card, done with and without the team rule; count the places that use a framework control instead of the team control | Fewer wrong uses |
| Questions at init | 2–3 real repos | Guessed answers are mostly right. **Measured on 3 repos (1.2.0–1.2.2): ≤ 12 questions, the bar at the time; 6 of 7 checked claims right (agent-checked). Since 1.4.0 (two passes with loops) there is no question limit: 14 standards questions on one repo; see [06](06-evidence.md)** |

## 9.9 Open questions

- **Where does the team standards set live so the whole team can use it?**
- **Confidence thresholds per topic:** set provisionally, adjust from measurements.
- **Tracker link (Azure Boards):** later.

## 9.10 Order of work after approval

1. ✅ Enforced compliance (9.7) and the finding-quality gate (9.5), measured on the 6 PRs (0.8.4–0.8.11).
2. ✅ The 3-tier standards framework, file format, and the 9.4 table in the controller (0.8.7).
3. ✅ Initial kit set: the 5 files in 9.3 (1.2.0, all `experimental`; the kit owner still has to approve each one).
4. ✅ Merged `dk:init` with per-topic questions, asked one at a time (1.2.0).
5. ✅ A sample team rule for a team's own controls, measured on one UI card in a worktree (0.8.7).
6. Update docs 01–08: done along the way.
