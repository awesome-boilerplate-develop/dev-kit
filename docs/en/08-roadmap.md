# 8. Roadmap and open questions

## 8.1 Next steps, in order

| # | Step | Why |
|---|---|---|
| 1 | ~~Run `dk:init` on a real repo~~ ✅ | Done on a demo copy of a private repo (see [06](06-evidence.md)) |
| 2 | Do one real card in **your own interactive session** (a human answers questions and approves) | The story was already run on the demo copy, but with `claude -p`: the agent decided on its own instead of asking. The part where a real person is asked can only be checked when you run it |
| 3 | ~~Do a few cards with Sonnet~~ ✅ (Opus not yet) | Sonnet: quality on par with baseline, cost about 1.3× (see [06](06-evidence.md)) |
| 4 | Dogfood for 1–2 weeks, record in `templates/dogfood-log.md` | Measures what the lab cannot: whether anyone reads the reports, whether review catches real bugs, whether the workflow gets in the way |
| 5 | Fix based on the log, re-measure in the lab before releasing a new version | Keeps the "evidence first" principle |

## 8.2 Features: built and not built

| Feature | Status | Notes |
|---|---|---|
| Tracker (GitHub Issues…) | Not built | Specs are currently local files in `.dev-kit/specs/` |
| Hosts other than Claude Code | Done (0.8.12) | Codex, Copilot CLI, Antigravity, OpenCode, omp load the kit; review quality measured only once on Codex ([05](05-setup-and-usage.md), [06](06-evidence.md)) |
| `CONSTRAINTS.md` read automatically by pre-pr-check | Done (1.1.0) | pre-pr-check step 1 checks the diff against `.dev-kit/CONSTRAINTS.md` (or the project's own) when it exists; not measured |
| Several repos for one developer | Not built (planned after single-repo use is solid) | 1.4.3 removed the project-or-team question from `dk:init`; see 8.5 |

## 8.3 Rules waiting for evidence

| Rule | What it needs to be enabled |
|---|---|
| Q1 Sibling check | At least 5 new tasks of the same kind where the new result is no worse than baseline. First try: 10/15 vs 11/16, not met |
| G1 Graph tools | Enabled as optional, measured neutral. Needs a measurement on a larger or less familiar repo to decide whether building an index should be encouraged |
| Q2 Read the ADR first | A task set with contradictory documents where baseline picks wrong |

## 8.4 Questions for you to decide

1. **Main host:** Claude Code or omp? This decides how codegraph is wired in and how subagents are spawned.
2. **Specs:** keep them as local files or push them to a tracker?
3. ~~**`.dev-kit/`:** which parts to commit and which to ignore?~~ Decided in 1.1.0: dev-kit is personal and nothing in `.dev-kit/` is committed. A shared team mode is an idea for later (8.5).
4. **Artifacts:** write them in Vietnamese, or in the language of the card?
5. **Cost:** do bugs need to come down below 1.5× baseline (currently 1.8×)? That would mean dropping review or the report for small bugs.

## 8.5 Ideas for later

### Several repos for one developer (planned, not built)

The current focus is one repo at a time: `dk:init` writes everything to that repo's `.dev-kit/standards/` (1.4.3). The next step, once single-repo use is solid, is to let one developer reuse rules across their own repos of the same product (for example several micro-frontends that share a control library and permission conventions).

What already exists: the five controllers load every `*.md` under `standards.team` in `.dev-kit/config.yml` (rule T1), so a folder set by hand already works; `dk:init` just does not offer it.

What it would add:
- **Label:** call the layer "shared across your repos" on screen rather than "team".
- **No per-item question:** items stay in the repo by default. At each pass's read-back, the agent points out the items that do not depend on this repo (an in-house library rule, a permission-key convention used by several repos) and asks once whether to move them to the shared folder (default: no).
- **Remembered path:** the shared folder is asked once and saved in `~/.dev-kit/config.yml`; `dk:init` in another repo writes that path into its own `standards.team` (missing today: in the test runs the field stayed `team: ""`).
- **Shown in the next repo:** the next repo's `dk:init` lists the shared rules already loaded, so they are not asked again, and its probe checks whether they fit that repo.

How to check it: write a shared rule in repo A, run `dk:init` and one controller in repo B, and confirm that B loads the rule (it appears in the report's standards list) without asking it again.

Open questions: what to do when a shared rule does not fit one repo (a project rule overrides it, project > team > kit); whether team mode (below) later replaces this folder.

### Team mode (not built)

1.1.0 made dev-kit strictly personal (rule O1). A team that wants to share its setup could later opt in to a **team mode**, chosen once in `dk:init` (for example `mode: personal | team` in `config.yml`, default `personal`).

What team mode could change:
- **Committed:** `.dev-kit/config.yml` (commands, base branch), `.dev-kit/standards/` (project rules, reviewed in PRs like code), `.dev-kit/specs/`, and possibly `baseline.md`. `.dev-kit/.gitignore` would then list only the personal parts (`reports/`, `plans/`, `sdd/`, `init-report.md`) instead of `*`.
- **Project knowledge:** `domain-modeling` and `constraint-driven-development` could write to the project's own `GLOSSARY.md`, `docs/adr/` and `CONSTRAINTS.md` at the root, as upstream does.
- **Worktrees:** the committed parts arrive with every worktree; only the personal parts would still need copying.
- **Onboarding:** a teammate's `dk:init` would read the committed config and standards instead of detecting everything again.

Open questions before building it:
- Who owns the shared standards, and how a personal override (project > team > kit) works when the project layer is committed.
- Whether a red `baseline.md` should be shared: it goes stale as tests are fixed.
- How to measure the gain: for example, the in-house controls rule (CHANGELOG 0.8.7) applied by several people from one committed file versus each person keeping a copy.
- Whether `standards.team` (a shared folder outside the repo) already covers enough of this, making team mode unnecessary.
