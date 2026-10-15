<!-- i18n: source=README.md source_commit=v1.4.0 review=machine -->
[English](README.md) | [Tiếng Việt](README.vi.md) | 简体中文 | [日本語](README.ja.md)

> 本译文可能滞后于英文版；以英文版为准：[README.md](README.md)。

# dev-kit

[![Release](https://img.shields.io/github/v/release/awesome-boilerplate-develop/dev-kit)](https://github.com/awesome-boilerplate-develop/dev-kit/releases) [![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE) [![docs](https://github.com/awesome-boilerplate-develop/dev-kit/actions/workflows/docs.yml/badge.svg)](https://github.com/awesome-boilerplate-develop/dev-kit/actions/workflows/docs.yml)

用于处理 kanban 卡片的 agent skill：story、bug、重构，以及开 PR 之前的检查。这些 skill 遵循的每一条 rule，都只有在测量过的 lab 中确实有帮助时才被保留。

适用于 **Claude Code**（参考）、**Codex**、**GitHub Copilot CLI**、**Antigravity**、**OpenCode** 和 **omp**。

## Skills

| Skill | 使用场景 |
|---|---|
| `dk:init` | 在仓库中首次运行：检查工具、写入 `.dev-kit/config.yml`、记录测试 baseline |
| `dk:story-runner` | 功能或 story 卡片：澄清、写 spec、带测试地实现，然后运行 `dk:pre-pr-check` |
| `dk:bug-fixer` | bug 卡片，包括性能回归：找出根因、写回归测试、修复 |
| `dk:code-refactor` | 技术债卡片：在不改变行为的前提下重构 |
| `dk:pre-pr-check` | 一个完成的分支：运行检查、按风险决定 review 深度、写报告和 PR 文本 |

plugin 的名称是 `dk`。有些 CLI 显示 skill 时不带 `dk:` 前缀。

## 安装

### Claude Code

```bash
claude plugin marketplace add awesome-boilerplate-develop/dev-kit
claude plugin install dk@dev-kit
```

在 session 中，等效的做法是 `/plugin marketplace add awesome-boilerplate-develop/dev-kit` 和 `/plugin install dk@dev-kit`。

### Codex

```bash
codex plugin marketplace add awesome-boilerplate-develop/dev-kit
codex plugin add dk@dev-kit
```

### GitHub Copilot CLI

```bash
copilot plugin marketplace add awesome-boilerplate-develop/dev-kit
copilot plugin install dk@dev-kit
```

### Antigravity

```bash
agy plugin install https://github.com/awesome-boilerplate-develop/dev-kit
```

### omp

```bash
omp plugin marketplace add awesome-boilerplate-develop/dev-kit
omp plugin install dk@dev-kit
```

### OpenCode

OpenCode 从文件夹加载 skill，因此需要克隆仓库并链接到你的用户 skill 文件夹：

```bash
git clone https://github.com/awesome-boilerplate-develop/dev-kit ~/dev-kit
mkdir -p ~/.config/opencode/skills
for s in ~/dev-kit/skills/*; do ln -s "$s" ~/.config/opencode/skills/; done
```

然后在 `~/.config/opencode/opencode.json` 中让 OpenCode 读取 kit 目录：

```json
{ "permission": { "external_directory": { "~/dev-kit/**": "allow" } } }
```

### 其他 CLI

- **不支持：** Gemini CLI（Google 已把免费层用户迁移到 Antigravity）、pi（pi 核心没有 subagent 工具）、Cursor（从未验证，已移除）。

各 CLI 的详情（安装位置、subagent 工具、已知注意事项）：[`harness/`](harness/README.md)。

## 快速开始

1. 用 agent 打开你的仓库，让它 **使用 `dk:init`**。它会先探查仓库，然后一次问一个问题（命令、graph 索引、按 topic 的 standards 清单，以及它根据你的代码建议的 rule），创建 `.dev-kit/` 并记录当前的测试 baseline。
2. 按名称把卡片交给它：

   ```text
   Use dk:bug-fixer for this card: "Checkout total drops to 0 when two promotions apply."
   ```

3. 完成后，你会得到一个 commit、`.dev-kit/reports/` 中的一份简短报告，以及来自 `dk:pre-pr-check` 的 GO / NO-GO verdict。

## 工作方式

- **精简的 controller。** 每个 controller 都是一个简短的 skill，直接在当前 session 中工作。它借用的较长 playbook（TDD、调试、规划、review……）放在 `parts/` 中，只有当某个步骤需要时才会读取，因此在 session 开始时不占用上下文。
- **有证据的 rule。** [`rules/RULES.md`](rules/RULES.md) 列出每条 rule、它是否开启，以及背后的 lab 结果。只有当一条 rule 在至少 5 个它没见过的任务上起到了帮助，才会被打开。
- **按风险决定 review 深度。** `dk:pre-pr-check` 会根据 diff 的大小和类型，选择 self-review、一个 reviewer 或四个 reviewer（标准、spec、安全、测试）。
- **机器检查的报告。** [`scripts/check_report.py`](scripts/check_report.py) 会拒绝一份报告，直到其中的 “certain” finding 位于被修改的代码中、不是泛泛的“缺少测试”之类的评语，并且只引用存在的 rule。
- **个人使用，从不推送。** dev-kit 写入的所有内容（配置、specs、plans、reports、你的项目标准）都放在 `.dev-kit/` 中，它会在 git 中自我忽略；dev-kit 从不修改 `.gitignore`、`CLAUDE.md`、`AGENTS.md` 或任何其他被跟踪的文件。
- **分层的标准。** kit 标准、你以任意方式共享的团队文件夹（`standards.team`），以及位于 `.dev-kit/standards/` 的你自己的项目标准；每个 reviewer 只会收到与其角色相关的主题。
- **可选的 graph 工具。** 有了 [codegraph](https://github.com/colbymchenry/codegraph) 和 code-review-graph 索引，controller 会用它们来查找代码、衡量 blast radius，并在 review 之前运行 `detect-changes`。

## 证据

- **Lab**（234 次运行，Haiku 5.5，一个示例应用和 13 个 SWE-bench Verified 的 Django 任务）：代码质量与让模型单独工作相当，成本约为其 2×。额外的开销买到的是 review 层和 artifact，而不是更正确的代码。
- **真实 bug 的 backtest**（一个私有 Angular 仓库，Sonnet 5.5）：强制执行 review 步骤后，`detect-changes` 的使用从 2/6 个 PR 提高到 6/6 个 PR；抓到真正 bug 的能力在不同运行之间仍然差异很大。
- **内部 UI 控件的项目 rule** 改变了 agent 写出的内容（有这条 rule 时为 6 和 10 个内部标签，没有时为 18 和 16 个 Material 标签）：这是最明显的收益，因为这是 agent 自己无法找到的知识。

详情与局限：[docs/en/06-evidence.md](docs/en/06-evidence.md)。

## 文档

- [文档索引](docs/zh-CN/README.md)：概览、架构、各个 skill、rule、安装与日常使用、证据、维护。
- [安装与使用](docs/zh-CN/05-setup-and-usage.md) · [Skills](docs/zh-CN/03-skills.md) · [术语表](docs/zh-CN/glossary.md)
- 翻译：越南语、简体中文、日语（见顶部的语言链接）。以英文版为准。

## 参与贡献

见 [CONTRIBUTING.md](CONTRIBUTING.md)：需要运行的检查、版本管理，以及如何翻译文档。变更记录见 [CHANGELOG.md](CHANGELOG.md)。

## 许可证

MIT，见 [LICENSE](LICENSE)。复制自 [Superpowers](https://github.com/obra/superpowers)、[mattpocock/skills](https://github.com/mattpocock/skills) 和 [agent-skills](https://github.com/addyosmani/agent-skills) 的部分，其 MIT 许可证保留在 [`LICENSES/`](LICENSES/) 中；见 [UPSTREAM.md](UPSTREAM.md)。
