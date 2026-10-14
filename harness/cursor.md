# Cursor

**Not verified:** cursor-agent 2026.08.11 needs `cursor-agent login` (or `CURSOR_API_KEY`) before it runs. Everything below comes from Cursor's docs and Superpowers' Cursor manifest, not from a dev-kit run.

- **Install:** `cursor-agent --plugin-dir <dev-kit>` loads a local plugin; dev-kit ships `.cursor-plugin/plugin.json` with `"skills": "./skills/"` (the shape Superpowers v7.0.0 uses).
- **Skills:** Cursor also reads `.agents/skills/`, `.cursor/skills/` and, for compatibility, `.claude/skills/` and `.codex/skills/` ([skills](https://cursor.com/docs/skills)). It walks skill roots recursively, so never link the dev-kit root itself into a skill folder: `parts/*/SKILL.md` would become skills.
- **Subagents:** started through the Task tool; custom subagents live in `.cursor/agents/` and Cursor also reads `.claude/agents/` ([subagents](https://cursor.com/docs/subagents)). For `dk:security-auditor` / `dk:test-engineer`, tell the subagent to read and follow `agents/<name>.md` in the kit folder.
