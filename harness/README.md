# Harness notes

dev-kit skills are written for Claude Code (the reference harness). Each controller starts with a **Harness** paragraph: when `${CLAUDE_PLUGIN_ROOT}` is not replaced, the dev-kit folder is two levels above the controller's `SKILL.md` after resolving symlinks, and the agent reads the file for its harness here. These files map dev-kit's vocabulary to each harness's tools; they never change what the controllers require.

| Harness | File | Install source | Verified |
|---|---|---|---|
| Claude Code | [claude-code.md](claude-code.md) | `.claude-plugin/` | yes |
| Codex | [codex.md](codex.md) | `.codex-plugin/`, `.agents/plugins/marketplace.json` | yes |
| GitHub Copilot CLI | [copilot.md](copilot.md) | `.claude-plugin/` (read as a legacy manifest) | yes |
| Antigravity (`agy`) | [antigravity.md](antigravity.md) | `.antigravity-plugin/` | yes |
| OpenCode | [opencode.md](opencode.md) | skill folders, no manifest | yes |
| Cursor | [cursor.md](cursor.md) | `.cursor-plugin/` | no (needs `cursor-agent login`) |
| omp | [omp.md](omp.md) | `.claude-plugin/` (omp reads Claude Code plugins) | yes |

"Verified" = a probe skill laid out like dev-kit was loaded on that harness and the agent read a file two levels above its `SKILL.md` and spawned one subagent, then dev-kit itself was installed and the agent resolved the kit folder and its harness notes (2026-10-14; versions in each file).

Not supported:
- **Gemini CLI:** Google moved unpaid and Google One users to Antigravity CLI on 2026-06-18.
- **pi (dropped for now):** pi 1.0.2 installed the kit and loaded the skills, but pi core has no subagent tool, so every review role would run in the main session; that path has not been measured.

## Shared vocabulary

| In the controllers | Meaning everywhere |
|---|---|
| `${CLAUDE_PLUGIN_ROOT}/…` | a path in the dev-kit folder |
| `dk:<skill>` | the skill named `<skill>` from this kit (a harness may show it with or without a `dk` prefix) |
| general-purpose subagent | your harness's default subagent, with a fresh context and the prompt the step gives |
| `dk:security-auditor`, `dk:test-engineer` | a subagent told to read and follow `agents/security-auditor.md` or `agents/test-engineer.md` in the dev-kit folder, plus the step's review inputs |
| no subagent tool | do each reviewer role yourself, one after another, and write "roles run in sequence (no subagent tool)" in Review setup |

Rule F2 holds on every harness: wait for every subagent in the same turn; never schedule background waits.
