# Upstream

| Part | Source | Commit | Edits |
|---|---|---|---|
| writing-plans, using-git-worktrees, subagent-driven-development, test-driven-development, systematic-debugging, verification-before-completion, receiving-code-review, finishing-a-development-branch, requesting-code-review (needed by SDD) | obra/superpowers v6.4.2 | 8ca22dba | `superpowers:<x>` → part reference; plan/spec paths → `.dev-kit/`; SDD ledger `.superpowers/sdd` → `.dev-kit/sdd` (scripts too); severity Critical/Important → Blocker/Major in SDD, requesting- and receiving-code-review prompts; dropped references to `executing-plans` (writing-plans) and `writing-skills` (TDD) |
| grilling, domain-modeling, codebase-design, code-review, pr, diagnosing-bugs | mattpocock/skills v1.3.1 | 24fe0ef7 | code-review: spec lookup starts at `.dev-kit/specs/`, tracker setup removed, dev-kit modes (self-review / reviewer role without sub-agents), dev-kit severity. Others: none yet |
| constraint-driven-development; agents security-auditor, test-engineer | addyosmani/agent-skills 0.6.12 | a06bc63b | agents: removed link to upstream `docs/agents.md`; dev-kit severity in output format. constraint-driven-development: asks before editing CLAUDE.md/AGENTS.md |

Since 0.8.0, eight parts carry a one-line `dev-kit (G1)` hook pointing to `rules/graph-playbook.md` (systematic-debugging, diagnosing-bugs, test-driven-development, verification-before-completion, codebase-design, writing-plans, code-review, requesting-code-review). Re-apply after copying a new upstream version.

Parts are **not registered as skills**: they cost no context at session start. Controllers read `parts/<name>/SKILL.md` when a step needs it.
