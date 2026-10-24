English | [Tiếng Việt](../vi/01-overview.md) | [简体中文](../zh-CN/01-overview.md) | [日本語](../ja/01-overview.md)

# 1. Overview

## 1.1 What dev-kit is

dev-kit is a Claude Code plugin with **6 skills**:

| Skill | Role |
|---|---|
| `dk:init` | Set up the environment for a machine and a repo |
| `dk:brainstorm` | Turn an idea into an agreed spec, before any code |
| `dk:story-runner` | Do a story/feature card from start to finish |
| `dk:bug-fixer` | Fix a bug card, with a test that prevents recurrence |
| `dk:code-refactor` | Restructure without changing behavior |
| `dk:pre-pr-check` | Final check before opening a PR |

The last four are **controllers**: orchestrating skills that choose their own steps and call "parts" (sub-skills) when needed. The kit also has 2 agent personas for review: `dk:security-auditor` and `dk:test-engineer`.

## 1.2 The problem

Working with agents every day, three problems keep coming back:

1. **A different style each time.** For the same kind of card, the agent writes tests first one time and not the next; produces a report one time and not the next. Readers find it hard to check.
2. **Installing several skill sets causes conflicts.** Superpowers, Matt Pocock, agent-skills... each is strong in one area. Installed together:
   - skill names collide (for example, two `test-driven-development` skills);
   - one set's bootstrap fights the other for control of skill selection;
   - many "user-invoked only" skills stop the automatic flow.
3. **No way to know which set really helps.** The sets promise a lot; nobody has measured them on their own work.

## 1.3 The idea

1. **A controller per card type:** one orchestrating skill per kind of work, calling the right sub-skill at the right step.
2. **Copy and merge into one set:** do not install the original plugins. Copy the parts you need, fix names and references, record the source. You own all the content, so there are no conflicts.
3. **Keep only what has evidence:** every choice (which steps run, how many reviewers, which rules are on) is measured in the lab first. Anything that costs without helping is removed from the default path.

## 1.4 What comes from which set

| Source | What was taken | Used for |
|---|---|---|
| Superpowers v6.4.2 | planning, worktree, subagent-driven development (SDD), TDD, systematic debugging, verifying before saying "done", receiving review, finishing a branch | Execution of large work, debugging |
| mattpocock/skills v1.3.1 | grilling (clarifying questions), domain-modeling, codebase-design, two-axis code-review, pr, diagnosing-bugs | Clarifying requirements, module design, review, PR text, performance bugs |
| agent-skills 0.6.12 | constraint-driven-development, personas `security-auditor` and `test-engineer` | Blocking lowered standards, security and test review |

Details on sources, commits and what was changed: [`UPSTREAM.md`](../../UPSTREAM.md).

## 1.5 Summary of measurements

From the lab (details in [06](06-evidence.md)):
- **Quality:** on par with letting the model work alone, with no controller. Measured on cards in a sample app and 13 SWE-bench Verified (Django) tasks.
- **Cost:** about **2×** letting the model work alone. The first version (everything heavy merged in) once cost 3–13×.
- **The value is in:**
  - consistent reports and artifacts for readers;
  - the final review layer;
  - a short rule set with evidence;
  - no conflicts between sets.

  The heavy orchestration (SDD, many reviewers) does **not** make code more correct in the lab.

## 1.6 What dev-kit does not do

- It does not push code or open PRs for you. The result is a commit on the current branch, with PR text prepared.
- It does not replace your decisions about requirements. When a card is ambiguous, the skill asks you; only when running with no human (headless) does it choose for itself and mark the choice as an assumption.
- It does not install tools or change configuration outside the repo without asking.
- It is not yet connected to a tracker (GitHub Issues, Jira...) or to code-graph tools (codegraph, code-review-graph). See [08](08-roadmap.md).
