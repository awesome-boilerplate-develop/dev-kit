<!-- i18n: source=docs/en/README.md source_commit=v1.2.0 review=human -->
[English](../en/README.md) | Tiếng Việt | [简体中文](../zh-CN/README.md) | [日本語](../ja/README.md)

> Bản dịch này có thể chậm hơn bản tiếng Anh; bản tiếng Anh ([docs/en/README.md](../en/README.md)) là bản chuẩn.

# Tài liệu dev-kit

dev-kit (tên plugin `dk`) là bộ skill giúp agent làm các thẻ kanban: story, bug, refactor và bước kiểm tra trước khi mở PR. Claude Code là CLI tham chiếu; Codex, Copilot CLI, Antigravity, OpenCode và omp nạp cùng một bộ skill. Kit gộp ba bộ có sẵn (Superpowers, Matt Pocock, agent-skills) và đã được đo trong một lab riêng trước khi phát hành.

Các tài liệu này có bằng tiếng Anh, tiếng Việt (tầng 1–2), tiếng Trung giản thể và tiếng Nhật (tầng 1). Bản tiếng Anh là bản chuẩn; các bản dịch có thể chậm hơn.

> Phiên bản tài liệu: dev-kit **1.2.0** (2026-10-14). 1.0.0 là bản public đầu tiên; các số version cũ hơn trong tài liệu (0.x) là các vòng lab riêng tư. Các số liệu đến từ lab của dev-kit (riêng tư) (chủ yếu Haiku 5.5, một phần Sonnet 5.5, Claude Code 2.1.296) và từ các backtest trên một repository Angular riêng tư ở công ty (Sonnet 5.5; một lần chạy trên Codex). Những gì chưa đo được đánh dấu ❓.

## Thứ tự đọc

| # | Tài liệu | Trả lời |
|---|---|---|
| 1 | [Tổng quan](01-overview.md) | dev-kit là gì, giải quyết vấn đề nào, ý tưởng đến từ đâu, những gì nó không làm |
| 2 | [Kiến trúc](02-architecture.md) | Cấu trúc thư mục, cơ chế controller/part/rule, artifact, cấu hình |
| 3 | [Skills](03-skills.md) | Mỗi skill làm gì: các bước, đầu vào, đầu ra, điểm dừng, ví dụ |
| 4 | [Rules](04-rules.md) | Rule nào đang bật, vì sao, bằng chứng, cách thêm rule mới |
| 5 | [Cài đặt và sử dụng](05-setup-and-usage.md) | Cài trên từng CLI, chạy `dk:init`, dùng hằng ngày, dùng cùng các plugin khác |
| 6 | [Bằng chứng](06-evidence.md) | Lab đã đo gì, kết quả, giới hạn của các phép đo |
| 7 | [Bảo trì](07-maintenance.md) | Cập nhật từ upstream, kiểm tra tham chiếu, đánh version |
| 8 | [Roadmap và câu hỏi mở](../en/08-roadmap.md) (tiếng Anh) | Còn thiếu gì, sẽ làm gì, cần quyết định gì |
| 9 | [Thiết kế 0.9.0: init và standards](../en/09-init-and-standards.md) (tiếng Anh) | **Thiết kế đang chờ duyệt (bản nháp 2):** `dk:init` hợp nhất, standards theo chủ đề, chất lượng finding, buộc tuân thủ |
| - | [Thuật ngữ](glossary.md) | Định nghĩa các thuật ngữ dùng trong tài liệu |

Tài liệu 8 và 9 (tầng 3) chỉ có bằng tiếng Anh.

## Lối tắt

- **Muốn dùng ngay:** [05](05-setup-and-usage.md), rồi phần đầu của [03](03-skills.md).
- **Muốn hiểu vì sao thiết kế như vậy:** [01](01-overview.md), [04](04-rules.md), [06](06-evidence.md).
- **Muốn sửa hoặc mở rộng kit:** [02](02-architecture.md), [07](07-maintenance.md).
