<!-- i18n: source=docs/en/05-setup-and-usage.md source_commit=v1.4.4 review=machine -->
[English](../en/05-setup-and-usage.md) | [Tiếng Việt](../vi/05-setup-and-usage.md) | 简体中文 | [日本語](../ja/05-setup-and-usage.md)

> 本译文可能滞后于英文版；以英文版为准：[05-setup-and-usage.md](../en/05-setup-and-usage.md)。

# 5. 安装与使用

## 5.1 要求

| 项目 | 说明 |
|---|---|
| Agent CLI | Claude Code 是参考 CLI（lab 使用 2.1.296）。Codex、Copilot CLI、Antigravity（`agy`）、OpenCode 和 omp 可以加载该 kit（5.2 节） |
| `git` | 必需 |
| 仓库的检查命令 | `make check`、`npm test`、…… `dk:init` 会检测并记录它 |
| `gh` | 可选；dev-kit 自己从不开 PR |
| `codegraph`、`code-review-graph` | 可选。`dk:init` 用 `scripts/install-graph-tools.sh` 检查；如果缺失，它会询问，然后用该脚本安装，并默认构建索引 |

## 5.2 安装

dev-kit 沿用 Superpowers 的做法：**一套 `skills/`，每个 CLI 一个 manifest**。各 CLI 之间的差异放在 [`harness/`](../../harness/README.md) 中。每个 controller 都以一段 **Harness** 开头：在不替换 `${CLAUDE_PLUGIN_ROOT}` 的 CLI 上，agent 会自己找到 kit 目录（`SKILL.md` 往上两级，解析 symlink 之后），并读取针对其 CLI 的说明。

**Claude Code**（参考 CLI）：

```bash
claude plugin marketplace add awesome-boilerplate-develop/dev-kit
claude plugin install dk@dev-kit
```

在 session 中：`/plugin marketplace add awesome-boilerplate-develop/dev-kit`，然后 `/plugin install dk@dev-kit`。如果想在不安装的情况下试用本地 checkout（例如在修改 kit 的时候）：`claude --plugin-dir /path/to/dev-kit`。

检查是否已加载：在一个 session 中，让 agent 列出以 `dk:` 开头的 skill。你必须看到全部 5 个：`dk:init`、`dk:story-runner`、`dk:bug-fixer`、`dk:code-refactor`、`dk:pre-pr-check`。

**其他 CLI**（于 2026-10-14 从公开仓库安装；详情和注意事项见 `harness/` 下的各个文件）：

| CLI | 安装命令 | 说明 |
|---|---|---|
| Codex 0.160.1 | `codex plugin marketplace add awesome-boilerplate-develop/dev-kit` 然后 `codex plugin add dk@dev-kit` | Codex 按版本安装一份副本（[codex.md](../../harness/codex.md)） |
| Copilot CLI 1.0.89 | `copilot plugin marketplace add awesome-boilerplate-develop/dev-kit` 然后 `copilot plugin install dk@dev-kit` | 直接从仓库或路径安装仍然可用，但据报告已被标记为 deprecated（[copilot.md](../../harness/copilot.md)） |
| Antigravity 1.3.5 | `agy plugin install https://github.com/awesome-boilerplate-develop/dev-kit` | `agy` 同时注册 `agents/` 和 `rules/*.md`（[antigravity.md](../../harness/antigravity.md)） |
| omp 18.10.4 | `omp plugin marketplace add awesome-boilerplate-develop/dev-kit` 然后 `omp plugin install dk@dev-kit` | omp 读取 Claude Code plugin；两个 review agent 以具名的 task agent 出现（[omp.md](../../harness/omp.md)） |
| OpenCode 1.18.35 | 克隆该仓库，把每个 `skills/<name>` 目录链接到 `~/.config/opencode/skills/` | 通过 `permission.external_directory` 允许读取 kit 目录（[opencode.md](../../harness/opencode.md)） |

不支持：
- **Gemini CLI：** 自 2026-06-18 起，Google 已把免费层和 Google One 用户迁移到 Antigravity CLI。
- **Cursor（自 1.2.3 起移除）：** 从未验证，因为 `cursor-agent` 需要登录。
- **pi（暂时搁置）：** pi 1.0.2 可以安装并加载该 kit，但 pi 核心没有 subagent 工具，所以每个 review 角色都得在主 session 中运行；这种模式尚未测量。

dev-kit 的 rule 和 lab 证据都是在 Claude 上测量的。对于表中的 CLI，已验证能加载该 kit；review 质量只在 Codex 上做过一次 backtest，其他 CLI 均未测量（[06](../en/06-evidence.md)，英文）。

## 5.3 为所有项目安装，还是按项目安装

| 方式 | 范围 | 说明 |
|---|---|---|
| `claude --plugin-dir /path/to/dev-kit` | 仅该 session | 加载本地 checkout；不改动任何配置；适合在修改 kit 时使用 |
| `claude plugin install dk@dev-kit` | 默认为用户（所有项目） | 安装结果显示 `scope: user`（2026-10-14）；仅项目的选项未验证 ❓ |

建议：为你的用户安装，并且只在你使用它的仓库里运行 `dk:init`。不要在仓库共享的 `.claude/settings.json` 中启用 dev-kit：它是个人 kit（rule O1）。

## 5.4 与其他 plugin 一起使用（Superpowers、code-review……）

**没有名称冲突：**
- plugin 的 skill 总是带有 plugin 名称作为前缀（`superpowers:…`、`code-review:…`、`dk:…`）。
- dev-kit 的子 skill 放在 `parts/` 中，不注册为 skill。

**你不需要关掉其他 plugin。** lab 在真实的全局配置下运行了 3 张卡片（B1、S1、P2）：17 个 plugin，包括 Superpowers 和官方的 `code-review`。
- **只调用了 `dk:*` skill；** 质量保持不变（缺陷 3/3、8/8、5/5）。
- **成本比隔离环境高约 15–50%**，因为每个启用的 plugin 都会向上下文中添加 skill 描述和 hook。

**需要知道的：**
- **那次测试是按名称调用 skill 的**（`Use skill dk:…`）。如果你只是笼统地说（“fix this bug”），Superpowers 可能会通过它的 `SessionStart` hook（`using-superpowers`）赢得 skill 的选择。未测量 ❓。按名称调用 controller 是稳妥的做法。
- **为了节省上下文，** 在该项目中只启用你需要的 plugin。

## 5.5 用脚本安装 graph 工具

```bash
bash /path/to/dev-kit/scripts/install-graph-tools.sh --check    # see what is already installed
bash /path/to/dev-kit/scripts/install-graph-tools.sh --install  # install the pinned version of whatever is missing
```

| 工具 | 固定版本 | 安装方式 |
|---|---|---|
| codegraph | v1.5.0 | codegraph 官方的 `install.sh`，按 tag 固定；放在 `~/.codegraph/` 和 `~/.local/bin/codegraph` |
| code-review-graph | 2.3.9 | `pipx`；如果没有 pipx，则回退到 `uv tool` |

**说明：**
- **已安装的工具不会动。** 脚本从不升级或降级，因为 codegraph 的 `install.sh` 在安装时会删除其他版本。
- **脚本不注册 MCP server，也不注册 hook**（它从不运行 `… install`）。
- **`dk:init` 在询问你之后会调用这个脚本。** 你也可以自己运行它。

## 5.6 如果不安装 graph 工具会怎样

**运行不受影响：** 每个 controller 仍然会做完它的所有步骤。只有 rule G1 是关闭的：
- agent 用 grep 和读文件来查找代码，而不是用 `codegraph`；
- `pre-pr-check` 没有关于风险和缺失测试的 CRG 摘要。

lab 测量了 17 个 SWE Django 任务（Haiku）：有索引和没有索引都解决了 10/17，成本相同。唯一的变化是 agent 使用 grep 的次数大约少了一半。在大型或不熟悉的仓库中，收益可能更明显，因为那里查找代码才是难点；这一点未测量 ❓。

## 5.7 第一次在一个仓库上使用

```text
Use skill dk:init for this repo.
```

agent 会先探查仓库，然后依次一次问一个问题：命令和基础分支、graph 索引、baseline（仅在它是红的时候）、分两遍的 standards（先是写代码的 rule，再是 review 清单；每一遍都是若干组清单，外加一个收集你自己约定的循环），以及可选的 `CONSTRAINTS.md`。每个问题都会给出依据和一行 Recommended；回复 “default”、“skip” 或你自己的答案。它会创建 `.dev-kit/`（被 git 忽略，无需提交）。之后若要重做某一部分：`dk:init index`、`dk:init baseline`、`dk:init standards [rules|review]`。

## 5.8 日常使用

按卡片类型调用 controller，并把卡片贴进去：

```text
Use skill dk:bug-fixer for this card:
<card text / issue link>
```

| 卡片类型 | Skill |
|---|---|
| 功能/story | `dk:story-runner` |
| Bug、性能问题 | `dk:bug-fixer` |
| 技术债、重构 | `dk:code-refactor` |
| 已完成的分支，PR 之前的检查 | `dk:pre-pr-check` |
| 在不修改的前提下检查别人的分支 | `dk:pre-pr-check`，并加上 “report only, do not change code” 这句话 |

**想要比默认更深入的 review：** 明确说 “review with all 4 reviewers”（rule C2）。

**要查看的输出：**
- `.dev-kit/reports/<name>.md`：做了什么、为什么、运行了哪些命令以及结果；
- `.dev-kit/reports/pr-body.md`：起草好的 PR 正文；
- `.dev-kit/specs/`（story）：尤其是 **Decisions** 部分，看看 agent 敲定了什么；
- 当前分支上的 commit。dev-kit 不会 push，也不会开 PR。

## 5.9 记录试用日志

对每张卡片，在 [`templates/dogfood-log.md`](../../templates/dogfood-log.md) 的一份副本中写一行：
- 走的路径（直接做还是 SDD，review 的深度）；
- 是否需要返工；
- review 真正抓到了什么；
- 成本；
- 流程是否妨碍了工作。

在一周结束时，回答模板底部的 4 个问题。这是决定下一步的主要数据，因为 lab 无法测量“对真人是否有用”。

## 5.10 出问题时

| 症状 | 检查 |
|---|---|
| 没有出现 `dk:*` skill | plugin 是否已加载（`--plugin-dir` 或 `/plugin`）？路径是否正确？ |
| agent 调用 `superpowers:…` 而不是按 controller 执行 | 按名称调用 `dk:<controller>`；如果仍被抢占，就在该项目中关闭 Superpowers（5.4） |
| controller 中途停止 | 附上 transcript 报告；rule F1 本应防止这种情况 |
| 一个普通 diff 上运行了四个 reviewer | 检查 diff 是否涉及 auth/secret/个人数据/config/migration；如果没有，那就是应用 rule C2 时的 bug |
| 报告里没有检查命令的输出 | `.dev-kit/config.yml` 中的命令错误或缺失：重新运行 `dk:init` |
