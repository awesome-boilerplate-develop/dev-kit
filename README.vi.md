<!-- i18n: source=README.md source_commit=v1.4.8 review=human -->
[English](README.md) | Tiếng Việt | [简体中文](README.zh-CN.md) | [日本語](README.ja.md)

> Bản dịch này có thể chậm hơn bản tiếng Anh; bản tiếng Anh ([README.md](README.md)) là bản chuẩn.

# dev-kit

[![Release](https://img.shields.io/github/v/release/awesome-boilerplate-develop/dev-kit)](https://github.com/awesome-boilerplate-develop/dev-kit/releases) [![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE) [![docs](https://github.com/awesome-boilerplate-develop/dev-kit/actions/workflows/docs.yml/badge.svg)](https://github.com/awesome-boilerplate-develop/dev-kit/actions/workflows/docs.yml)

Các skill cho agent làm việc với thẻ kanban: story, bug, refactor, và bước kiểm tra trước khi bạn mở PR. Mọi rule mà các skill tuân theo chỉ được giữ lại nếu nó giúp ích trong một lab có đo lường.

Chạy với **Claude Code** (CLI tham chiếu), **Codex**, **GitHub Copilot CLI**, **Antigravity**, **OpenCode** và **omp**.

## Skills

| Skill | Dùng khi |
|---|---|
| `dk:init` | Lần đầu chạy trong một repo: kiểm tra công cụ, ghi `.dev-kit/config.yml`, ghi lại test baseline |
| `dk:story-runner` | Thẻ feature hoặc story: làm rõ yêu cầu, viết spec, triển khai kèm test, rồi chạy `dk:pre-pr-check` |
| `dk:bug-fixer` | Thẻ bug, kể cả hồi quy hiệu năng: tìm nguyên nhân gốc, viết regression test, sửa lỗi |
| `dk:code-refactor` | Thẻ nợ kỹ thuật: tái cấu trúc mà không đổi hành vi |
| `dk:pre-pr-check` | Một branch đã làm xong: chạy các lệnh kiểm tra, review ở độ sâu tùy theo rủi ro, viết báo cáo và nội dung PR |

Plugin có tên `dk`. Một số CLI hiển thị skill mà không có tiền tố `dk:`.

## Cài đặt

### Claude Code

```bash
claude plugin marketplace add awesome-boilerplate-develop/dev-kit
claude plugin install dk@dev-kit
```

Trong một session, có thể dùng `/plugin marketplace add awesome-boilerplate-develop/dev-kit` và `/plugin install dk@dev-kit`.

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

OpenCode nạp skill từ các thư mục, nên hãy clone repo rồi liên kết các skill vào thư mục skill của user:

```bash
git clone https://github.com/awesome-boilerplate-develop/dev-kit ~/dev-kit
mkdir -p ~/.config/opencode/skills
for s in ~/dev-kit/skills/*; do ln -s "$s" ~/.config/opencode/skills/; done
```

Sau đó cho OpenCode đọc thư mục kit, trong `~/.config/opencode/opencode.json`:

```json
{ "permission": { "external_directory": { "~/dev-kit/**": "allow" } } }
```

### Các CLI khác

- **Không hỗ trợ:** Gemini CLI (Google đã chuyển người dùng gói miễn phí sang Antigravity), pi (lõi pi không có công cụ subagent), Cursor (chưa từng kiểm chứng; đã bỏ).

Chi tiết theo từng CLI (nơi cài đặt, công cụ subagent, các lưu ý đã biết): [`harness/`](harness/README.md).

## Bắt đầu nhanh

1. Mở repo của bạn bằng agent và nhờ nó **dùng `dk:init`**. Nó probe repo, rồi hỏi vài câu từng câu một (lệnh, index graph, một checklist tiêu chuẩn theo topic kèm các rule nó đề xuất từ code của bạn), tạo `.dev-kit/` và ghi lại test baseline hiện tại.
2. Giao thẻ cho nó theo tên:

   ```text
   Use dk:bug-fixer for this card: "Checkout total drops to 0 when two promotions apply."
   ```

3. Khi xong, bạn nhận được một commit, một báo cáo ngắn trong `.dev-kit/reports/`, và verdict GO / NO-GO từ `dk:pre-pr-check`.

## Cách hoạt động

- **Controller mỏng.** Mỗi controller là một skill ngắn, làm việc trực tiếp trong session. Các playbook dài hơn mà nó mượn (TDD, debugging, planning, review…) nằm trong `parts/` và chỉ được đọc khi một bước cần đến, nên không tốn context lúc bắt đầu session.
- **Rule có bằng chứng.** [`rules/RULES.md`](rules/RULES.md) liệt kê từng rule, trạng thái bật/tắt và kết quả lab đứng sau nó. Một rule chỉ được bật nếu nó giúp ích trên ít nhất 5 tác vụ chưa từng thấy.
- **Độ sâu review theo rủi ro.** `dk:pre-pr-check` chọn self-review, một reviewer hoặc bốn (standards, spec, security, tests) tùy theo kích thước và loại của diff.
- **Báo cáo được máy kiểm tra.** [`scripts/check_report.py`](scripts/check_report.py) từ chối một báo cáo cho đến khi mọi finding (certain hay suspect) nằm trong code đã đổi, finding certain không phải nhận xét chung chung kiểu thiếu test, và chỉ trích dẫn những rule có thật. [`scripts/check_standards.py`](scripts/check_standards.py) kiểm các file standards mà `dk:init` ghi ra.
- **Của riêng bạn, không bao giờ push.** Mọi thứ dev-kit ghi (config, spec, plan, báo cáo, tiêu chuẩn project của bạn) nằm trong `.dev-kit/`, thư mục này tự bị git bỏ qua; dev-kit không bao giờ sửa `.gitignore`, `CLAUDE.md`, `AGENTS.md` hay bất kỳ file nào đang được git theo dõi.
- **Tiêu chuẩn theo lớp.** Tiêu chuẩn của kit, một thư mục dùng chung (`standards.team`, hiện điền tay; `dk:init` chỉ ghi vào repo), và tiêu chuẩn project của riêng bạn trong `.dev-kit/standards/`; mỗi reviewer chỉ nhận các chủ đề thuộc vai trò của mình.
- **Công cụ graph (tùy chọn).** Với các index của [codegraph](https://github.com/colbymchenry/codegraph) và code-review-graph, controller tìm code, đo blast radius và chạy `detect-changes` trước khi review.

## Evidence

- **Lab** (234 lần chạy, Haiku 5.5, một ứng dụng mẫu và 13 tác vụ Django của SWE-bench Verified): chất lượng code ngang với để model tự làm, với chi phí khoảng 2×. Phần chi thêm dành cho lớp review và các artifact, không làm code đúng hơn.
- **Backtest trên bug thật** (một repository Angular riêng tư, Sonnet 5.5): việc buộc tuân thủ các bước review đã tăng mức dùng `detect-changes` từ 2/6 lên 6/6 PR; việc bắt được bug thật vẫn dao động mạnh giữa các lần chạy.
- **Rule của project cho control UI nội bộ** đã thay đổi những gì agent viết ra (6 và 10 tag nội bộ khi có rule, 18 và 16 tag Material khi không có): chiến thắng rõ nhất, vì đó là kiến thức agent không thể tự tìm ra.

Chi tiết và giới hạn: [docs/vi/06-evidence.md](docs/vi/06-evidence.md).

## Tài liệu

- [Mục lục tài liệu](docs/vi/README.md): tổng quan, kiến trúc, từng skill, rule, cài đặt và dùng hằng ngày, evidence, bảo trì.
- [Cài đặt và sử dụng](docs/vi/05-setup-and-usage.md) · [Skills](docs/vi/03-skills.md) · [Glossary](docs/vi/glossary.md)
- Bản dịch: tiếng Việt, tiếng Trung giản thể, tiếng Nhật (xem các liên kết ngôn ngữ ở đầu trang). Bản tiếng Anh là bản chuẩn.

## Đóng góp

Xem [CONTRIBUTING.md](CONTRIBUTING.md): các lệnh kiểm tra cần chạy, cách đặt version, và cách dịch tài liệu. Các thay đổi được liệt kê trong [CHANGELOG.md](CHANGELOG.md).

## Giấy phép

MIT, xem [LICENSE](LICENSE). Các phần sao chép từ [Superpowers](https://github.com/obra/superpowers), [mattpocock/skills](https://github.com/mattpocock/skills) và [agent-skills](https://github.com/addyosmani/agent-skills) giữ nguyên giấy phép MIT của chúng trong [`LICENSES/`](LICENSES/); xem [UPSTREAM.md](UPSTREAM.md).
