# 8. Roadmap and open questions

## 8.1 Next steps, in order

| # | Step | Why |
|---|---|---|
| 1 | ~~Run `dk:init` on a real repo~~ ✅ | Done on a demo copy of a private repo (see [06](06-evidence.md)) |
| 2 | Do one real card in **your own interactive session** (a human answers questions and approves) | The story was already run on the demo copy, but with `claude -p`: the agent decided on its own instead of asking. The part where a real person is asked can only be checked when you run it |
| 3 | ~~Do a few cards with Sonnet~~ ✅ (Opus not yet) | Sonnet: quality on par with baseline, cost about 1.3× (see [06](06-evidence.md)) |
| 4 | Dogfood for 1–2 weeks, record in `templates/dogfood-log.md` | Measures what the lab cannot: whether anyone reads the reports, whether review catches real bugs, whether the workflow gets in the way |
| 5 | Fix based on the log, re-measure in the lab before releasing a new version | Keeps the "evidence first" principle |

## 8.2 Not in 0.7.0

| Feature | Status | Notes |
|---|---|---|
| Tracker (GitHub Issues…) | Not built | Specs are currently local files in `.dev-kit/specs/` |
| Hosts other than Claude Code (omp, Codex) | Not tried ❓ | Skill invocation syntax and subagent spawning differ |
| `CONSTRAINTS.md` read automatically by pre-pr-check | Partial | pre-pr-check looks for signs of lowered standards in the diff, but does not yet compare against the numeric thresholds in `CONSTRAINTS.md` |

## 8.3 Rules waiting for evidence

| Rule | What it needs to be enabled |
|---|---|
| Q1 Sibling check | At least 5 new tasks of the same kind where the new result is no worse than baseline. First try: 10/15 vs 11/16, not met |
| G1 Graph tools | Enabled as optional, measured neutral. Needs a measurement on a larger or less familiar repo to decide whether building an index should be encouraged |
| Q2 Read the ADR first | A task set with contradictory documents where baseline picks wrong |

## 8.4 Questions for you to decide

1. **Main host:** Claude Code or omp? This decides how codegraph is wired in and how subagents are spawned.
2. **Specs:** keep them as local files or push them to a tracker?
3. **`.dev-kit/`:** which parts to commit (config, specs) and which to ignore (reports)?
4. **Artifacts:** write them in Vietnamese, or in the language of the card?
5. **Cost:** do bugs need to come down below 1.5× baseline (currently 1.8×)? That would mean dropping review or the report for small bugs.
