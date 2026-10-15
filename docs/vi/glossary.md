<!-- i18n: source=docs/en/glossary.md source_commit=v1.4.3 review=human -->
[English](../en/glossary.md) | Tiếng Việt | [简体中文](../zh-CN/glossary.md) | [日本語](../ja/glossary.md)

> Bản dịch này có thể chậm hơn bản tiếng Anh; bản tiếng Anh ([docs/en/glossary.md](../en/glossary.md)) là bản chuẩn.

# Thuật ngữ

Các thuật ngữ như controller, part, rule, skill, subagent, harness, finding, certain/suspect, verdict, GO/NO-GO, backtest, baseline, worktree, artifact, report-only, self-review, blast radius, plugin, marketplace được giữ nguyên tiếng Anh trong mọi ngôn ngữ.

| Thuật ngữ | Ý nghĩa trong dev-kit |
|---|---|
| **Controller** | Skill điều phối một loại thẻ (`dk:story-runner`, `dk:bug-fixer`, `dk:code-refactor`, `dk:pre-pr-check`): quyết định các bước, đọc part, áp dụng rule, viết báo cáo |
| **Part** | Sub-skill sao chép từ một bộ upstream, giữ trong `parts/`, không đăng ký thành skill; controller đọc file khi cần |
| **Rule** | Một chỉ dẫn ngắn trong `rules/RULES.md`, có trạng thái bật/tắt và bằng chứng |
| **Baseline** | Cùng model nhưng không cài bộ skill nào; điểm tham chiếu để so sánh trong lab |
| **SDD** (subagent-driven development) | Cách làm của Superpowers: chia một plan thành các task, sinh một subagent cho mỗi task và một subagent để review từng task; một sổ ghi (ledger) cho phép chạy tiếp được |
| **Worktree** | Một thư mục làm việc git riêng cho một branch, để việc lớn không đụng vào thư mục chính |
| **Grilling** | Cách làm rõ yêu cầu của Matt Pocock: hỏi từng câu một, đi theo cây các quyết định thiết kế |
| **Characterization test** (test đặc tả hành vi) | Test cố định hành vi hiện tại trước khi refactor, kể cả hành vi trông như bug |
| **Pre-PR / final gate** (chốt chặn cuối) | Bước kiểm tra trước khi mở PR: chạy các lệnh kiểm tra, tìm dấu hiệu hạ tiêu chuẩn, review, và đưa ra verdict GO/NO-GO |
| **Lowered standard** (hạ tiêu chuẩn) | Lối tắt "cho qua nhanh": bỏ qua một test, thêm `noqa`/`ts-ignore`, xóa một assert, hạ một ngưỡng |
| **Artifact** | File mà agent để lại cho người đọc: spec, plan, báo cáo, nội dung PR, trong `.dev-kit/` |
| **Headless** | Chạy khi không có người trả lời (`claude -p`), như trong lab |
| **Overfit** | Rule viết từ một tác vụ cụ thể, chỉ giúp tác vụ đó chứ không giúp các tác vụ mới cùng loại |
| **Upstream** | Các bộ gốc: Superpowers, mattpocock/skills, agent-skills |
| **Dogfood** | Dùng dev-kit trên công việc thật của chính bạn và ghi nhật ký |
