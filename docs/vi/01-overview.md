<!-- i18n: source=docs/en/01-overview.md source_commit=v1.7.3 review=human -->
[English](../en/01-overview.md) | Tiếng Việt | [简体中文](../zh-CN/01-overview.md) | [日本語](../ja/01-overview.md)

> Bản dịch này có thể chậm hơn bản tiếng Anh; bản tiếng Anh ([docs/en/01-overview.md](../en/01-overview.md)) là bản chuẩn.

# 1. Tổng quan

## 1.1 dev-kit là gì

dev-kit là một plugin Claude Code với **5 skill**:

| Skill | Vai trò |
|---|---|
| `dk:init` | Chuẩn bị môi trường cho một máy và một repo |
| `dk:story-runner` | Làm một thẻ story/feature từ đầu đến cuối |
| `dk:bug-fixer` | Sửa một thẻ bug, kèm test ngăn tái phát |
| `dk:code-refactor` | Tái cấu trúc mà không đổi hành vi |
| `dk:pre-pr-check` | Kiểm tra cuối trước khi mở PR |

Bốn skill cuối là **controller**: các skill điều phối, tự chọn các bước và gọi các "part" (sub-skill) khi cần. Kit còn có 2 persona agent để review: `dk:security-auditor` và `dk:test-engineer`.

## 1.2 Vấn đề

Làm việc với agent hằng ngày, ba vấn đề cứ lặp lại:

1. **Mỗi lần một kiểu.** Với cùng một loại thẻ, lần này agent viết test trước, lần sau thì không; lần này có báo cáo, lần sau thì không. Người đọc khó kiểm tra.
2. **Cài nhiều bộ skill gây xung đột.** Superpowers, Matt Pocock, agent-skills... mỗi bộ mạnh ở một mảng. Cài chung thì:
   - tên skill đụng nhau (ví dụ hai skill `test-driven-development`);
   - bootstrap của bộ này tranh quyền chọn skill với bộ kia;
   - nhiều skill "chỉ người dùng gọi" làm đứt luồng tự động.
3. **Không biết bộ nào thật sự giúp ích.** Các bộ hứa hẹn nhiều; chưa ai đo chúng trên công việc của chính mình.

## 1.3 Ý tưởng

1. **Một controller cho mỗi loại thẻ:** một skill điều phối cho mỗi loại việc, gọi đúng sub-skill ở đúng bước.
2. **Sao chép và gộp thành một bộ:** không cài các plugin gốc. Sao chép các part cần dùng, sửa tên và tham chiếu, ghi lại nguồn. Bạn sở hữu toàn bộ nội dung nên không có xung đột.
3. **Chỉ giữ thứ có bằng chứng:** mọi lựa chọn (chạy bước nào, bao nhiêu reviewer, bật rule nào) đều được đo trong lab trước. Thứ gì tốn chi phí mà không giúp ích thì bị loại khỏi đường mặc định.

## 1.4 Lấy gì từ bộ nào

| Nguồn | Lấy gì | Dùng cho |
|---|---|---|
| Superpowers v6.4.2 | planning, worktree, subagent-driven development (SDD), TDD, systematic debugging, xác minh trước khi nói "xong", nhận review, kết thúc một branch | Thực thi việc lớn, debug |
| mattpocock/skills v1.3.1 | grilling (hỏi làm rõ), domain-modeling, codebase-design, code-review hai trục, pr, diagnosing-bugs | Làm rõ yêu cầu, thiết kế module, review, nội dung PR, bug hiệu năng |
| agent-skills 0.6.12 | constraint-driven-development, các persona `security-auditor` và `test-engineer` | Chặn việc hạ tiêu chuẩn, review bảo mật và test |

Chi tiết về nguồn, commit và những gì đã sửa: [`UPSTREAM.md`](../../UPSTREAM.md).

## 1.5 Tóm tắt các phép đo

Từ lab (chi tiết ở [06](06-evidence.md)):
- **Chất lượng:** ngang với để model tự làm, không có controller. Đo trên các thẻ trong một ứng dụng mẫu và 13 tác vụ SWE-bench Verified (Django).
- **Chi phí:** khoảng **2×** so với để model tự làm. Phiên bản đầu (gộp hết mọi thứ nặng vào) từng tốn 3–13×.
- **Giá trị nằm ở:**
  - báo cáo và artifact nhất quán cho người đọc;
  - lớp review cuối;
  - một bộ rule ngắn có bằng chứng;
  - không xung đột giữa các bộ.

  Phần điều phối nặng (SDD, nhiều reviewer) **không** làm code đúng hơn trong lab.

## 1.6 dev-kit không làm gì

- Nó không push code hay mở PR thay bạn. Kết quả là một commit trên branch hiện tại, kèm nội dung PR đã soạn sẵn.
- Nó không thay quyết định của bạn về yêu cầu. Khi thẻ mơ hồ, skill sẽ hỏi bạn; chỉ khi chạy không có người (headless) thì nó mới tự chọn và đánh dấu lựa chọn đó là giả định.
- Nó không cài công cụ hay đổi cấu hình ngoài repo mà không hỏi.
- Nó chưa kết nối với tracker (GitHub Issues, Jira...) hay công cụ code-graph (codegraph, code-review-graph). Xem [08](../en/08-roadmap.md).
