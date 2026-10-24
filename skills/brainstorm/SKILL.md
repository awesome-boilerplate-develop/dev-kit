---
name: brainstorm
description: Shape an idea into an agreed spec before any code. Use when the user wants to explore an idea, compare approaches or design a feature before there is a clear card; ends with a spec for dk:story-runner and never writes code.
---

# brainstorm

## Before you start

**Harness.** Written for Claude Code, which replaces the plugin-root variable below with the dev-kit folder. If you see `${CLAUDE_PLUGIN_ROOT}` literally, your harness did not replace it: the dev-kit folder is two levels above this SKILL.md after resolving symlinks (the folder that contains `rules/RULES.md`). Read every `${CLAUDE_PLUGIN_ROOT}/…` below as a path in that folder, and first read `harness/<your harness>.md` there (`codex`, `copilot`, `opencode`, `antigravity`, `omp`): it maps `dk:<skill>`, subagents and the review agents to your tools.

**Parts.** Steps name *parts*: playbooks at `${CLAUDE_PLUGIN_ROOT}/parts/<name>/SKILL.md` (absolute path). Read a part only when a step names it; relative paths inside a part resolve against that part's folder, so `../../rules/…` inside a part means `${CLAUDE_PLUGIN_ROOT}/rules/…`. Parts are not skills.

## Output

**Outputs** (rule O1). The only file this skill writes is `.dev-kit/specs/<feature>.md`. It never writes code, commits, or edits a tracked file, and writes no report: there is no diff yet. Run subagents in the foreground and wait for them in this turn (rule F2). When no one can answer (headless run), choose the most reasonable option, mark it as an assumption in Decisions and leave the spec at `Status: draft`.

## Steps

### 1. Context
Look at what the idea touches: the files, docs and recent commits it would change. If it spans several independent subsystems, say so and agree with the user which one comes first; brainstorm one at a time.

### 2. Clarify
Read part `grilling` and settle purpose, constraints and success criteria with the user. If the idea introduces new domain terms, also Read part `domain-modeling`.

### 3. Approaches
Propose 2–3 approaches with their trade-offs, the recommended one first with its reason, and wait for the user's choice. Drop what the goal does not need.

### 4. Design by section
Present the design in sections sized to their complexity (behaviour rules, interface, edge cases, how it will be tested). After each section ask whether it looks right; revise until it does.

### 5. Spec
Write the spec to `.dev-kit/specs/<feature>.md` from `${CLAUDE_PLUGIN_ROOT}/templates/spec.md`:
- `Card:` is the card, or the idea's name when there is none; `Status: draft`.
- The chosen approach is a Decisions row: question "Which approach?", the answer with its reason and the options rejected.
- What was cut goes under Out of scope.

### 6. Self-review
Re-read the spec and fix it in place: no placeholders (TBD, TODO, vague rules), no sections that contradict each other, one card's worth of work (split it otherwise), no rule that reads two ways (pick one and record it in Decisions).

### 7. User review
Ask the user to review the file. Changes → edit, then step 6 again. On approval set `Status: agreed` and offer `dk:story-runner` with this spec; do not start it yourself.
