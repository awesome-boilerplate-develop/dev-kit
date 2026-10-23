<!-- i18n: source=docs/en/05-setup-and-usage.md source_commit=v1.7.2 review=human -->
[English](../en/05-setup-and-usage.md) | Tiếng Việt | [简体中文](../zh-CN/05-setup-and-usage.md) | [日本語](../ja/05-setup-and-usage.md)

> Bản dịch này có thể chậm hơn bản tiếng Anh; bản tiếng Anh ([docs/en/05-setup-and-usage.md](../en/05-setup-and-usage.md)) là bản chuẩn.

# 5. Cài đặt và sử dụng

## 5.1 Yêu cầu

| Mục | Ghi chú |
|---|---|
| Agent CLI | Claude Code là CLI tham chiếu (lab dùng 2.1.296). Codex, Copilot CLI, Antigravity (`agy`), OpenCode và omp có thể nạp kit (mục 5.2) |
| `git` | Bắt buộc |
| Lệnh kiểm tra của repo | `make check`, `npm test`, … `dk:init` phát hiện và ghi lại |
| `gh` | Tùy chọn; dev-kit không bao giờ tự mở PR |
| `codegraph`, `code-review-graph` | Tùy chọn. `dk:init` kiểm tra bằng `scripts/install-graph-tools.sh`; nếu thiếu thì hỏi, rồi cài bằng chính script đó và mặc định dựng các index |

## 5.2 Cài đặt

dev-kit theo cách của Superpowers: **một bộ `skills/`, một manifest cho mỗi CLI**. Phần khác nhau giữa các CLI nằm trong [`harness/`](../../harness/README.md). Mỗi controller mở đầu bằng một đoạn **Harness**: trên CLI không thay thế `${CLAUDE_PLUGIN_ROOT}`, agent tự tìm thư mục kit (hai cấp trên `SKILL.md`, sau khi resolve symlink) và đọc ghi chú cho CLI của mình.

**Claude Code** (CLI tham chiếu):

```bash
claude plugin marketplace add awesome-boilerplate-develop/dev-kit
claude plugin install dk@dev-kit
```

Trong một session: `/plugin marketplace add awesome-boilerplate-develop/dev-kit`, rồi `/plugin install dk@dev-kit`. Để thử một bản checkout cục bộ mà không cài (ví dụ khi đang sửa kit): `claude --plugin-dir /path/to/dev-kit`.

Kiểm tra đã nạp chưa: trong một session, nhờ agent liệt kê các skill bắt đầu bằng `dk:`. Bạn phải thấy đủ 5: `dk:init`, `dk:story-runner`, `dk:bug-fixer`, `dk:code-refactor`, `dk:pre-pr-check`.

**Các CLI khác** (cài từ repo công khai ngày 2026-10-14; chi tiết và lưu ý nằm trong từng file dưới `harness/`):

| CLI | Lệnh cài | Ghi chú |
|---|---|---|
| Codex 0.160.1 | `codex plugin marketplace add awesome-boilerplate-develop/dev-kit` rồi `codex plugin add dk@dev-kit` | Codex cài một bản sao cho mỗi version ([codex.md](../../harness/codex.md)) |
| Copilot CLI 1.0.89 | `copilot plugin marketplace add awesome-boilerplate-develop/dev-kit` rồi `copilot plugin install dk@dev-kit` | Cài thẳng từ repo hoặc đường dẫn vẫn chạy nhưng được báo là đã deprecated ([copilot.md](../../harness/copilot.md)) |
| Antigravity 1.3.5 | `agy plugin install https://github.com/awesome-boilerplate-develop/dev-kit` | `agy` đăng ký cả `agents/` lẫn `rules/*.md` ([antigravity.md](../../harness/antigravity.md)) |
| omp 18.10.4 | `omp plugin marketplace add awesome-boilerplate-develop/dev-kit` rồi `omp plugin install dk@dev-kit` | omp đọc plugin của Claude Code; hai agent review xuất hiện dưới dạng named task agent ([omp.md](../../harness/omp.md)) |
| OpenCode 1.18.35 | clone repo, liên kết từng thư mục `skills/<name>` vào `~/.config/opencode/skills/` | Cho phép đọc thư mục kit bằng `permission.external_directory` ([opencode.md](../../harness/opencode.md)) |

Không hỗ trợ:
- **Gemini CLI:** từ 2026-06-18 Google đã chuyển người dùng gói miễn phí và Google One sang Antigravity CLI.
- **Cursor (bỏ từ 1.2.3):** chưa từng kiểm chứng được, vì `cursor-agent` cần đăng nhập.
- **pi (tạm gác):** pi 1.0.2 cài và nạp được kit, nhưng lõi pi không có công cụ subagent, nên mọi vai trò review sẽ phải chạy trong session chính; chế độ đó chưa được đo.

Các rule và bằng chứng lab của dev-kit được đo trên Claude. Với các CLI trong bảng, việc nạp kit đã được kiểm chứng; chất lượng review mới có một backtest, trên Codex, còn các CLI khác chưa đo ([06](06-evidence.md)).

## 5.3 Cài cho mọi project hay theo từng project

| Cách | Phạm vi | Ghi chú |
|---|---|---|
| `claude --plugin-dir /path/to/dev-kit` | Chỉ session đó | Nạp một bản checkout cục bộ; không đụng cấu hình; hợp khi đang sửa kit |
| `claude plugin install dk@dev-kit` | User (mọi project) theo mặc định | Lần cài báo `scope: user` (2026-10-14); tùy chọn chỉ cho project chưa được kiểm chứng ❓ |

Gợi ý: cài cho user của bạn, và chỉ chạy `dk:init` ở những repo bạn thực sự dùng. Đừng bật dev-kit trong `.claude/settings.json` dùng chung của một repo: đây là bộ công cụ cá nhân (rule O1).

## 5.4 Dùng cùng các plugin khác (Superpowers, code-review…)

**Không đụng tên:**
- Skill của một plugin luôn mang tên plugin làm tiền tố (`superpowers:…`, `code-review:…`, `dk:…`).
- Sub-skill của dev-kit nằm trong `parts/` và không được đăng ký thành skill.

**Bạn không cần tắt các plugin khác.** Lab đã chạy 3 thẻ (B1, S1, P2) với cấu hình global thật: 17 plugin, gồm Superpowers và `code-review` chính thức.
- **Chỉ các skill `dk:*` được gọi;** chất lượng giữ nguyên (3/3, 8/8, 5/5 defect).
- **Chi phí cao hơn khoảng 15–50%** so với chạy cô lập, vì mỗi plugin được bật đều thêm mô tả skill và hook vào context.

**Nên biết:**
- **Bài test đó gọi skill theo tên** (`Use skill dk:…`). Nếu bạn chỉ nói chung chung ("fix this bug"), Superpowers có thể thắng ở khâu chọn skill nhờ hook `SessionStart` (`using-superpowers`). Chưa đo ❓. Gọi controller theo tên là cách an toàn.
- **Để tiết kiệm context,** chỉ bật các plugin bạn cần trong project đó.

## 5.5 Cài công cụ graph bằng script

```bash
bash /path/to/dev-kit/scripts/install-graph-tools.sh --check    # see what is already installed
bash /path/to/dev-kit/scripts/install-graph-tools.sh --install  # install the pinned version of whatever is missing
```

| Công cụ | Version được ghim | Cài bằng |
|---|---|---|
| codegraph | v1.5.0 | `install.sh` chính thức của codegraph, ghim theo tag; đặt vào `~/.codegraph/` và `~/.local/bin/codegraph` |
| code-review-graph | 2.3.9 | `pipx`; chuyển sang `uv tool` nếu thiếu pipx |

**Lưu ý:**
- **Công cụ đã cài thì để nguyên.** Script không bao giờ nâng hay hạ version, vì `install.sh` của codegraph xóa các version khác khi cài.
- **Script không đăng ký MCP server hay hook nào** (nó không bao giờ chạy `… install`).
- **`dk:init` gọi script này** sau khi hỏi bạn. Bạn cũng có thể tự chạy.

## 5.6 Nếu bạn không cài công cụ graph

**Việc chạy không bị ảnh hưởng:** mọi controller vẫn làm đủ các bước. Chỉ rule G1 tắt:
- agent tìm code bằng grep và đọc file thay vì `codegraph`;
- `pre-pr-check` không có bản tóm tắt CRG về rủi ro và test còn thiếu.

Lab đã đo 17 tác vụ SWE Django (Haiku): có và không có index đều giải được 10/17, với cùng chi phí. Thay đổi duy nhất là agent dùng grep ít hơn khoảng một nửa. Lợi ích có thể rõ hơn ở repo lớn hoặc lạ, nơi việc tìm code là phần khó; điều này chưa được đo ❓.

## 5.7 Lần đầu trên một repo

```text
Use skill dk:init for this repo.
```

Agent probe repo trước, rồi hỏi từng câu một, theo thứ tự: lệnh và base branch, index graph, thiết lập nhanh hay chi tiết (nhanh thì lấy các dòng Recommended và chỉ hỏi một lần ở cuối, bằng một checklist đã tick sẵn các mục Recommended để bạn thêm hoặc bỏ), baseline (chỉ khi nó đỏ), tiêu chuẩn theo hai lượt (rule khi viết code, rồi checklist review; mỗi lượt là một danh sách các nhóm và một vòng lặp cho quy ước riêng của bạn), và `CONSTRAINTS.md` tùy chọn. Mỗi câu hỏi cho thấy bằng chứng và một dòng Recommended; hãy trả lời "default", "skip" hoặc câu trả lời của bạn. Nó tạo `.dev-kit/` (được git bỏ qua, không có gì để commit). Để làm lại một phần sau này: `dk:init index`, `dk:init baseline`, `dk:init standards [rules|review]`.

**Khởi động `dk:init` trên từng CLI** (dev-kit 1.4.x, các lần chạy ngày 2026-10-15 trên một repo private; thêm "hỏi và trả lời bằng tiếng Việt" vào tin nhắn đầu nếu muốn):

| CLI | Tin nhắn đầu | Câu hỏi trong phiên tương tác | Mỗi lượt một lệnh (headless) |
|---|---|---|---|
| Claude Code | `/dk:init` (Claude Code có `init` riêng của nó) | chưa chạy với 1.4.x | `claude -p … --resume <session>`: mỗi lượt một câu hỏi, lựa chọn dạng chữ (đã kiểm) |
| Codex | `$dk:init` | chưa chạy với 1.4.x | `codex exec` rồi `codex exec resume <id> "<câu trả lời>"`: mỗi lượt một câu hỏi (đã kiểm); `resume` nhận `-c sandbox_mode=…`, không nhận `-s` |
| Copilot CLI | `/dk:init` | form `ask_user` (đã kiểm) | `copilot -p` lấy mọi mặc định và không hỏi gì (đã kiểm) |
| Antigravity | `/dk:init`, mở bằng `agy -i` | form `ask_question` có dòng "Write-in…" (đã kiểm) | `agy -p` tự bỏ qua các form và lấy mọi mặc định (đã kiểm) |
| OpenCode | `/init …` (skill không có namespace; trong `opencode run` lệnh này nạp được skill) | chưa chạy | `opencode run` rồi `opencode run -c "<câu trả lời>"`: mỗi lượt một câu hỏi (đã kiểm); trước đó cho phép thư mục kit trong `external_directory` ([opencode.md](../../harness/opencode.md)) |
| omp | `/dk:init` | chưa chạy với 1.4.x | `omp -p` rồi `omp -p -c "<câu trả lời>"`: mỗi lượt một câu hỏi (đã kiểm) |

Khi dùng thật, hãy chạy phiên tương tác và tự trả lời; các chế độ headless dành cho kiểm tra bằng script.

## 5.8 Dùng hằng ngày

Gọi một controller theo loại thẻ và dán thẻ vào:

```text
Use skill dk:bug-fixer for this card:
<card text / issue link>
```

| Loại thẻ | Skill |
|---|---|
| Feature/story | `dk:story-runner` |
| Bug, vấn đề hiệu năng | `dk:bug-fixer` |
| Nợ kỹ thuật, refactor | `dk:code-refactor` |
| Branch đã xong, kiểm tra trước PR | `dk:pre-pr-check` |
| Kiểm tra branch của người khác mà không sửa | `dk:pre-pr-check`, kèm câu "report only, do not change code" |

**Để review sâu hơn mặc định:** nói rõ "review with all 4 reviewers" (rule C2).

**Output cần xem:**
- `.dev-kit/reports/<name>.md`: đã làm gì, vì sao, các lệnh đã chạy và kết quả;
- `.dev-kit/reports/pr-body.md`: nội dung PR đã soạn;
- `.dev-kit/specs/` (story): đặc biệt là mục **Decisions**, để xem agent đã chốt những gì;
- các commit trên branch hiện tại. dev-kit không push và không mở PR.

## 5.9 Ghi nhật ký dùng thử

Với mỗi thẻ, ghi một dòng vào bản sao của [`templates/dogfood-log.md`](../../templates/dogfood-log.md):
- đường đi đã chọn (trực tiếp hay SDD, độ sâu review);
- có phải làm lại không;
- review thực sự bắt được gì;
- chi phí;
- quy trình có gây vướng không.

Cuối tuần, trả lời 4 câu hỏi ở cuối template. Đây là dữ liệu chính để quyết định bước tiếp theo, vì lab không đo được "có ích với người thật".

## 5.10 Khi có sự cố

| Triệu chứng | Kiểm tra |
|---|---|
| Không thấy skill `dk:*` nào | Plugin đã được nạp chưa (`--plugin-dir` hoặc `/plugin`)? Đường dẫn đúng chưa? |
| Agent gọi `superpowers:…` thay vì theo controller | Gọi `dk:<controller>` theo tên; nếu vẫn bị chen ngang, tắt Superpowers trong project đó (5.4) |
| Controller dừng giữa chừng | Báo lại kèm transcript; rule F1 lẽ ra đã ngăn việc này |
| Bốn reviewer chạy trên một diff bình thường | Kiểm tra diff có đụng tới auth/secret/dữ liệu cá nhân/config/migration không; nếu không thì đó là lỗi trong việc áp dụng rule C2 |
| Báo cáo không có output của lệnh kiểm tra | Lệnh trong `.dev-kit/config.yml` sai hoặc thiếu: chạy lại `dk:init` |
