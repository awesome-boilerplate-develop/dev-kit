<!-- i18n: source=docs/en/03-skills.md source_commit=v1.0.0 review=machine -->
[English](../en/03-skills.md) | [Tiếng Việt](../vi/03-skills.md) | 简体中文 | [日本語](../ja/03-skills.md)

> 本译文可能滞后于英文版；以英文版为准：[03-skills.md](../en/03-skills.md)。

# 3. Skills

四个 controller 在各自的步骤之前，共享同样的行为块：

| 块 | 含义 |
|---|---|
| **Parts** | 只有当某个步骤提到某个 part 时才去读它；part 不是 skill |
| **Rules** | 应用 `rules/RULES.md` 中开启的 rule：F1、F2、C1、C2、G1、S1、O1（[04](../en/04-rules.md)，英文） |
| **Graph** | 如果仓库有 codegraph/CRG 索引，按 rule G1 使用；没有则跳过 |
| **Commands** | 如果存在 `.dev-kit/config.yml`，从中取检查命令和基础分支；否则使用 `make check` 或仓库的测试命令，以及 `main` |
| **Outputs** | 一切都写入 `.dev-kit/`（rule O1）；最后按 `templates/report.md` 出一份报告；严重程度使用 blocker/major/minor 分级（rule S1） |

下面的示例是**示意，并未运行**在你的仓库上。真实示例在 lab 中，见 [06](../en/06-evidence.md)（英文）。

---

## 3.1 `dk:init`

**使用场景：** 在一台机器或一个仓库上首次使用 dev-kit；或者想重新检查设置时。

**原则：**
- 先打印计划，等你批准，再动手。
- 重新运行只会检查并补全缺失的部分；不会覆盖已有文件。
- 安装任何东西或修改仓库之外的任何内容，都要先询问。
- 它不包含任何 controller 逻辑。

**步骤：**
1. **机器：** 检查 `git`、`gh`、`make`、`codegraph`、`code-review-graph`（含版本）；列出已启用的 plugin，并提醒你按名称调用 `dk:<controller>`。
   - **检查 graph 工具**：使用 `scripts/install-graph-tools.sh --check`。
   - **如果缺失：** 在计划中说明并询问一次。如果你同意，运行 `scripts/install-graph-tools.sh --install`（固定版本；已有的工具不会动）。如果你拒绝，则继续，并在报告中写 “G1 off”。
   - **绝不运行** `codegraph install` 或 `code-review-graph install`：这两个命令会注册 MCP、hook 和指令文件。
2. **检测命令：** 从 `Makefile`、`package.json`、`pyproject.toml` 中检测。请你确认，然后写入 `.dev-kit/config.yml`。
3. **创建 `.dev-kit/`**（specs、plans、reports）。询问哪些部分要提交。
4. **可选：** 用 `constraint-driven-development` part 创建 `CONSTRAINTS.md`（会询问你的质量标准；有默认阈值）。
5. **Graph 索引，默认开启**（属于你批准的计划的一部分）：
   - 运行 `codegraph init` 和 `code-review-graph build`；
   - 对于大型仓库，先报告磁盘占用并询问：每约 3,000 个文件大致占用 150 MB 和 600 MB；
   - 把 `.codegraph/` 和 `.code-review-graph/` 加入 `.gitignore`，并在 `config.yml` 中写入 `graph.*`。
6. **Baseline：** 运行一次测试和构建。
   - **绿：** 记录到报告中。
   - **红：** 报告失败数量和主要的失败分组，然后请你选择：**停止**（先修复）或**接受为已知 baseline**。如果你接受，就写入 `.dev-kit/baseline.md`（按 `templates/baseline.md`），逐个按名称列出失败的测试。此后 controller 只有在此列表**之外**的测试失败时，才把一次运行算作失败（rule B1）。
7. **写入 `.dev-kit/init-report.md`。**

**输出：** `config.yml`、`.dev-kit/` 目录、init 报告，以及可选的 `CONSTRAINTS.md` 和 graph 索引。

⚠️ `dk:init` **从未在 lab 中运行过**。它是最先要试的东西（[08](../en/08-roadmap.md)，英文）。

---

## 3.2 `dk:bug-fixer`

**使用场景：** bug 工单，包括性能 bug（某次改动之后变慢了）。

**步骤：**
1. **复现并找到根因。** 对于难的 bug 或性能 bug，读取 `systematic-debugging` 或 `diagnosing-bugs` part 并照做。
2. **写一个回归测试**，使其因正确的原因而失败 → 在根因处修复 → 测试变绿。
3. **运行检查命令。** 提交；commit message 要写明根因。
4. **运行 `dk:pre-pr-check`。**

**输出：** 一个带测试的修复 commit、一份报告、pre-pr-check 的结果。

**不包含：** 单独的复现 subagent 或修复 subagent（旧版本有，lab 表明它们只会增加成本），也不使用 worktree。

```mermaid
flowchart LR
    A["Reproduce + root cause"] --> B["Red test"] --> C["Fix → green"] --> D["Checks + commit"] --> E["dk:pre-pr-check"]
```

**示例（示意）：** 工单“一个含 2 个促销的订单，其商品总额降为 0”。
- agent 发现有代码把所有促销的百分比相加，而规则是只取最高的那个促销。
- 它写了一个含两个促销（60% 和 50%）的测试（红），把代码改为 `max`，运行检查，并提交 “fix: promotions must not stack”。
- pre-pr-check：diff 很小，所以做 self-review 并写出报告。

---

## 3.3 `dk:story-runner`

**使用场景：** 功能/story 工单。

**步骤：**
1. **澄清。** 如果工单含糊不清，读取 `grilling` part，一次问你一个问题。如果有新的业务术语，也读取 `domain-modeling` part。只有在没有人能回答时（headless 运行），它才自己选一个合理的方案，并标记为 assumption。
2. **写 spec** `.dev-kit/specs/<feature>.md`，按 `templates/spec.md`：目标、rule、接口、验收标准、范围之外，以及一个 **Decisions** 部分（问题、答案、谁决定，或 “assumption”）。
3. **遵循 rule C1：**
   - **小型工作：** 直接在 session 中完成，测试先行，每个行为一个 commit。
   - **大型工作**（超过 3 个任务或涉及多个模块）：按顺序使用这些 part：`writing-plans` → `using-git-worktrees` → `subagent-driven-development` → `finishing-a-development-branch`（合并回你正在工作的分支；不 push/不开 PR）。
4. **运行 `dk:pre-pr-check`。**

```mermaid
flowchart TD
    A{"Ambiguous ticket?"} -- "Yes" --> G["grilling (+ domain-modeling)"] --> S
    A -- "No" --> S["Spec + Decisions"]
    S --> Z{"Large work?"}
    Z -- "No" --> D["Work in the session, tests first"]
    Z -- "Yes" --> P["writing-plans → worktree → SDD → finishing"]
    D --> PP["dk:pre-pr-check"]
    P --> PP
```

**示例（示意）：** 工单“顾客在结账时输入折扣码”。
- grilling 会问：每个订单是一个码还是多个码，在税前还是税后扣除，以及无效的码显示什么。
- spec 把答案记录在 Decisions 中。
- 这是小型工作（1 个模块），所以在 session 中完成：每条 rule 一个测试，每个行为一个 commit；最后运行 pre-pr-check。

---

## 3.4 `dk:code-refactor`

**使用场景：** 技术债工单：拆分、合并或移动模块，且**不改变行为**。

**步骤：**
1. **确定新的接口。** 如果边界不清楚，读取 `codebase-design` part。
2. **先写 characterization test**，在公共接口上，针对每种输入固定当前行为。看起来像 bug 的行为也要固定：在报告中记为 “suspect bug”，并且在重构期间**不要修复**它。
3. **遵循 rule C1：** 小型工作在 session 内小步移动，每步之后检查，每步提交。大型工作则像 story-runner 那样使用 SDD 的 part。
4. **运行 `dk:pre-pr-check`。** review 会检查“没有行为变化”以及你确定的接口。

**为什么连看起来像 bug 的行为也要固定：** 在 lab 中，一张重构工单是通过在 300 个随机输入上比较前后行为来评分的。如果你在重构期间“顺手修个 bug”，行为就变了，reviewer 无法分辨哪部分是重构，哪部分是 bug 修复。

---

## 3.5 `dk:pre-pr-check`

**使用场景：** 分支完成，即将开 PR。其他三个 controller 会在结束时自动调用它；你也可以直接对一个由人写的分支调用它。

**Report-only 模式：** 如果请求里说“不要修改代码”，它不会编辑任何文件，并跳过第 4 步。

**步骤：**
1. **立即运行检查命令**，并把输出保留为 Evidence。阅读 `git diff <base branch>...HEAD`，查找降低标准的迹象：新增被跳过的测试、添加了 `noqa`/`ts-ignore`、删除了 assert、降低了阈值。
2. **按 rule C2 选择 review 级别：**

   | 级别 | 何时 | 做什么 |
   |---|---|---|
   | Self-review | Diff ≤ 2 个文件且 < 50 行（用 `git diff --shortstat` 测量） | 读取 `code-review` part，自己应用它的两个轴；不启动 subagent |
   | 1 个 reviewer | 其他所有情况 | 1 个读取 `code-review` part 的通用 subagent |
   | 4 个 reviewer | 你要求，或 diff 涉及 auth/权限、secret、个人数据、migration、config/env | 并行：2 个 `code-review` reviewer（各负责一个轴）、`dk:security-auditor`、`dk:test-engineer` |

   每个 reviewer 都会收到 diff 范围和 spec/issue 文本，并返回 `file:line | blocker/major/minor | reason`。
3. **把结果合并**成一张按 blocker/major/minor 分级的表。只要还有任何 blocker 未解决，就是 `Verdict: NO-GO`；否则是 `GO`。
4. **如果有 blocker：** 读取 `receiving-code-review` part，用证据修复（或附理由反驳），然后回到第 1 步。最多 2 轮。
5. **附带 findings 表出报告。** 除非是 report-only 模式，否则按 `pr` part 写入 `.dev-kit/reports/pr-body.md`（Summary / Evidence / Merge Danger），其中 Evidence 是第 1 步的输出。

**示例（示意）：** 一个“部分退款”分支涉及权限和个人数据，所以运行 4 个 reviewer。结果是 NO-GO，blocker 如下：
- 非员工角色仍然可以发起退款；
- 退款可以被重复多次；
- 舍入方向是向上而不是向下；
- 客户的 email 泄露到了 audit log 中。

同时附带一张 file:line 表和一份起草好的 PR 正文。

---

## 3.6 两个 persona agent

| Agent | 检查什么 | 来源 |
|---|---|---|
| `dk:security-auditor` | OWASP、secret、认证/授权、带 CVE 的依赖 | agent-skills |
| `dk:test-engineer` | 覆盖率、边界情况、错误路径；测试是否真正检查了正确的 rule | agent-skills |

只有当 pre-pr-check 选择 4 个 reviewer 的级别时，才会启动它们。一个 persona 不会调用另一个 persona。
