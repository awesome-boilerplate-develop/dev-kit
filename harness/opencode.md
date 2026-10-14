# OpenCode

Checked on opencode 1.18.35.

- **Install:** OpenCode plugins are JS modules; skills come from skill folders ([skills](https://opencode.ai/docs/skills/)): `.opencode/skills/`, `.agents/skills/`, `.claude/skills/` in the project, or `~/.config/opencode/skills/`, `~/.agents/skills/`, `~/.claude/skills/`. Link each folder under `<dev-kit>/skills/` there, keeping its name (`ln -s <dev-kit>/skills/pre-pr-check ~/.config/opencode/skills/pre-pr-check`).
- **Allow the kit folder.** Reads outside the project need `external_directory`, which defaults to `ask`; non-interactive `opencode run` rejected them in a probe. Add to `opencode.json` ([permissions](https://opencode.ai/docs/permissions/)):

  ```json
  { "permission": { "external_directory": { "<dev-kit>/**": "allow" } } }
  ```
- **Kit folder:** OpenCode gives the agent the link path; resolve symlinks (`realpath`) before going two levels up. `${CLAUDE_PLUGIN_ROOT}` is not replaced.
- **Skills:** no namespace; names must be unique across all skill folders.
- **Subagents:** the `task` tool with `subagent_type: general`. For `dk:security-auditor` / `dk:test-engineer`, tell it to read and follow `agents/<name>.md` in the kit folder.
