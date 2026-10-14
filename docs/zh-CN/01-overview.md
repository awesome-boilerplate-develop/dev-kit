<!-- i18n: source=docs/en/01-overview.md source_commit=v1.2.2 review=machine -->
[English](../en/01-overview.md) | [Tiếng Việt](../vi/01-overview.md) | 简体中文 | [日本語](../ja/01-overview.md)

> 本译文可能滞后于英文版；以英文版为准：[01-overview.md](../en/01-overview.md)。

# 1. 概览

## 1.1 dev-kit 是什么

dev-kit 是一个包含 **5 个 skill** 的 Claude Code plugin：

| Skill | 角色 |
|---|---|
| `dk:init` | 为一台机器和一个仓库搭建环境 |
| `dk:story-runner` | 从头到尾完成一张 story/功能卡片 |
| `dk:bug-fixer` | 修复一张 bug 卡片，并附带防止复发的测试 |
| `dk:code-refactor` | 在不改变行为的前提下重构 |
| `dk:pre-pr-check` | 开 PR 之前的最终检查 |

后四个是 **controller**：编排型 skill，自行选择步骤，并在需要时调用 “part”（子 skill）。该 kit 还有 2 个用于 review 的 agent persona：`dk:security-auditor` 和 `dk:test-engineer`。

## 1.2 问题

每天与 agent 协作，有三个问题反复出现：

1. **每次风格都不同。** 对同一类卡片，agent 有时先写测试，有时不写；有时产出报告，有时不产出。读者很难检查。
2. **同时安装多套 skill 会产生冲突。** Superpowers、Matt Pocock、agent-skills……每一套都在某个方面很强。一起安装时：
   - skill 名称冲突（例如有两个 `test-driven-development` skill）；
   - 一套的 bootstrap 与另一套争夺 skill 选择的控制权；
   - 许多“仅限用户调用”的 skill 会打断自动流程。
3. **无从得知哪一套真正有帮助。** 这些集合承诺了很多；没有人在自己的工作上测量过它们。

## 1.3 思路

1. **每种卡片类型一个 controller：** 每类工作一个编排 skill，在合适的步骤调用合适的子 skill。
2. **复制并合并成一套：** 不安装原始 plugin。复制你需要的 part，修正名称和引用，记录来源。全部内容归你所有，因此没有冲突。
3. **只保留有证据的东西：** 每个选择（运行哪些步骤、几个 reviewer、开启哪些 rule）都先在 lab 中测量。凡是花费成本却没有帮助的，都从默认路径中移除。

## 1.4 什么来自哪一套

| 来源 | 采用了什么 | 用于 |
|---|---|---|
| Superpowers v6.4.2 | planning、worktree、subagent-driven development (SDD)、TDD、systematic debugging、在说“完成”之前先验证、接收 review、结束一个分支 | 大型工作的执行、调试 |
| mattpocock/skills v1.3.1 | grilling（澄清式提问）、domain-modeling、codebase-design、双轴 code-review、pr、diagnosing-bugs | 澄清需求、模块设计、review、PR 文本、性能 bug |
| agent-skills 0.6.12 | constraint-driven-development、persona `security-auditor` 和 `test-engineer` | 阻止降低标准、安全与测试 review |

关于来源、commit 以及改动了什么的详情：[`UPSTREAM.md`](../../UPSTREAM.md)。

## 1.5 测量摘要

来自 lab（详情见 [06](../en/06-evidence.md)，英文）：
- **质量：** 与让模型单独工作（不用 controller）相当。测量对象是一个示例应用中的卡片和 13 个 SWE-bench Verified (Django) 任务。
- **成本：** 约为让模型单独工作的 **2×**。第一版（把所有重型机制都合并进来）曾经花费 3–13×。
- **价值在于：**
  - 一致的报告和面向读者的 artifact；
  - 最后的 review 层；
  - 一套简短且有证据的 rule；
  - 各套之间没有冲突。

  重型编排（SDD、多个 reviewer）在 lab 中**并没有**让代码更正确。

## 1.6 dev-kit 不做什么

- 它不会替你推送代码或开 PR。结果是当前分支上的一个 commit，并备好 PR 文本。
- 它不会替代你对需求的决定。当卡片含糊不清时，skill 会问你；只有在没有人在场的情况下运行（headless）时，它才会自己选择，并把这个选择标记为 assumption。
- 它不会在没有询问的情况下安装工具或修改仓库之外的配置。
- 它尚未接入 tracker（GitHub Issues、Jira……）或代码图工具（codegraph、code-review-graph）。见 [08](../en/08-roadmap.md)（英文）。
