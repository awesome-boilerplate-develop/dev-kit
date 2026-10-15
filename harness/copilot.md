# GitHub Copilot CLI

Checked on GitHub Copilot CLI 1.0.89.

- **Install:** `copilot plugin marketplace add awesome-boilerplate-develop/dev-kit`, then `copilot plugin install dk@dev-kit` (Copilot reads the catalog in `.claude-plugin/marketplace.json` and the legacy manifest `.claude-plugin/plugin.json`, and loads `skills/`). A direct install (`copilot plugin install <owner/repo or path>`) also works but prints a deprecation warning ("Only plugin@marketplace installs will be supported in a future release"). To try a local checkout without installing: `copilot --plugin-dir <dev-kit> --add-dir <dev-kit>`; without `--add-dir`, reads of the kit folder were denied.
- **Kit folder:** the installed copy (direct installs: `~/.copilot/installed-plugins/_direct/<source folder name>/`). `${CLAUDE_PLUGIN_ROOT}` is not replaced in `SKILL.md` (Copilot expands it only in MCP server settings: [plugin reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference)).
- **Subagents:** the `task` tool.
- **Headless runs ask nothing:** with `copilot -p`, `dk:init` follows its rule for runs nobody can answer: it takes every default and lists them as assumptions (seen in one run). To answer its questions, use the interactive session, where questions appear as `ask_user` forms.
- **Permissions:** `--allow-all-tools` does not cover paths outside the working directory. In one interactive `dk:init` run Copilot still asked to trust the folder, to use the symlinked `codegraph` and `code-review-graph` binaries, and to run some shell commands; an unanswered prompt stalls the run.
- **Review agents:** legacy plugins load agents from `agents/*.agent.md`; dev-kit's files are `agents/*.md`, so they are not registered. Spawn a `task` subagent told to read and follow `agents/<name>.md`.
