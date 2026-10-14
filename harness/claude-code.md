# Claude Code (reference harness)

Checked on Claude Code 2.1.299.

- **Install:** `claude --plugin-dir <dev-kit>` to try; `/plugin marketplace add awesome-boilerplate-develop/dev-kit` then `/plugin install dk@dev-kit`.
- **Kit folder:** `${CLAUDE_PLUGIN_ROOT}` is replaced with it inside `SKILL.md`.
- **Skills:** `dk:<skill>`, namespaced by the plugin.
- **Subagents:** the `Agent` tool; `general-purpose` is the default type. `agents/*.md` are registered as `dk:security-auditor` and `dk:test-engineer`.
