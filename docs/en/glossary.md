English | [Tiếng Việt](../vi/glossary.md) | [简体中文](../zh-CN/glossary.md) | [日本語](../ja/glossary.md)

# Glossary

| Term | Meaning in dev-kit |
|---|---|
| **Controller** | A skill that orchestrates one card type (`dk:story-runner`, `dk:bug-fixer`, `dk:code-refactor`, `dk:pre-pr-check`): decides the steps, reads parts, applies rules, writes the report |
| **Part** | A sub-skill copied from an upstream set, kept in `parts/`, not registered as a skill; a controller reads the file when needed |
| **Rule** | A short instruction in `rules/RULES.md`, with an on/off status and evidence |
| **Baseline** | The same model with no skill set installed; the reference point for comparison in the lab |
| **SDD** (subagent-driven development) | The Superpowers way of working: split a plan into tasks, spawn a subagent for each task and a subagent to review each task; a ledger lets the run resume |
| **Worktree** | A separate git working directory for a branch, so large work does not touch the main directory |
| **Grilling** | Matt Pocock's way of clarifying requirements: ask one question at a time, following the tree of design decisions |
| **Characterization test** | A test that pins current behavior before a refactor, including behavior that looks like a bug |
| **Pre-PR / final gate** | The check before opening a PR: run checks, look for lowered-standard signs, review, and give a GO/NO-GO verdict |
| **Lowered standard** | A "pass quickly" shortcut: skipping a test, adding `noqa`/`ts-ignore`, deleting an assert, lowering a threshold |
| **Artifact** | A file the agent leaves for human readers: spec, plan, report, PR text, in `.dev-kit/` |
| **Headless** | Running with no human to answer (`claude -p`), as in the lab |
| **Overfit** | A rule written from one specific task that helps only that task, not new tasks of the same kind |
| **Upstream** | The original sets: Superpowers, mattpocock/skills, agent-skills |
| **Dogfood** | Using dev-kit on your own real work and keeping a log |
