<!-- i18n: source=docs/en/07-maintenance.md source_commit=v1.2.2 review=human -->
[English](../en/07-maintenance.md) | Tiếng Việt

> Bản dịch này có thể chậm hơn bản tiếng Anh; bản tiếng Anh là bản chính thức. Xem [bản tiếng Anh](../en/07-maintenance.md).

# 7. Bảo trì

## 7.1 Nguyên tắc

- **`parts/` là bản copy có sửa.** Sửa gì trong part cũng ghi vào [`UPSTREAM.md`](../../UPSTREAM.md), để lần cập nhật sau biết cần áp lại những gì.
- **Controller và rule là phần tự viết,** không phụ thuộc upstream.
- **Mỗi thay đổi hành vi** phải có một dòng trong [`CHANGELOG.md`](../../CHANGELOG.md). Nếu là rule thì kèm bằng chứng trong `rules/RULES.md`.

## 7.2 Kiểm tham chiếu sau mỗi lần sửa

```bash
python3 scripts/check_parts.py .
```

Script báo lỗi khi:
- một part hay controller nhắc tới part không tồn tại (`parts/<x>/SKILL.md`, "dev-kit part \`x\`");
- một link Markdown tương đối bị hỏng.

Link nằm trong code fence (ví dụ minh họa) được bỏ qua.

## 7.3 Cập nhật từ upstream

1. Tải bản mới của bộ gốc vào một thư mục tạm, cạnh bản đang ghim. Commit hiện tại được ghi trong `UPSTREAM.md`.
2. `diff` hai bản, chỉ cho các part dev-kit đang dùng.
3. Với mỗi part có thay đổi:
   - **Part "giữ nguyên"** (cột Edits ghi "none yet"): copy đè lên.
   - **Part có sửa:** copy đè lên, rồi áp lại các sửa đã ghi.
   - **SDD** (sửa nhiều nhất): đọc diff và tự chọn phần lấy.
4. Chạy `scripts/check_parts.py`.
5. Chạy lại lab (ít nhất các ticket trên app mẫu và vài bài SWE) và so với lần chạy trước. Nếu kém đi thì không phát hành.
6. Cập nhật `UPSTREAM.md` (commit mới), `CHANGELOG.md`, và version bằng `python3 scripts/bump_version.py <x.y.z>`.

## 7.4 Thêm một part mới

1. Copy nguyên thư mục skill từ bộ gốc vào `parts/<name>/`.
2. Đổi các tham chiếu dạng `<kit>:<skill>` thành "dev-kit part \`<skill>\` (parts/<skill>/SKILL.md)". Copy thêm part được trỏ tới, hoặc bỏ tham chiếu.
3. Thêm một dòng vào `UPSTREAM.md` và LICENSE của nguồn (nếu là nguồn mới) vào `LICENSES/`.
4. Gắn part vào một bước của controller. Đừng copy part mà không ai dùng.
5. Chạy `check_parts.py`, rồi đo bằng lab.

## 7.5 Đánh version

| Thay đổi | Version |
|---|---|
| Sửa câu chữ, docs, sửa lỗi không đổi hành vi | patch (1.0.x) |
| Đổi luồng controller, bật/tắt rule, thêm part | minor (1.x.0) |
| Đổi tên skill, đổi chỗ để artifact, đổi schema config | major (x.0.0); mô tả cách chuyển đổi trong CHANGELOG |

Version nằm ở nhiều manifest (Claude Code, Codex, Cursor, Antigravity), được liệt kê trong `.version-bump.json`. Luôn đổi bằng `python3 scripts/bump_version.py <x.y.z>`; `--check` báo lỗi khi các manifest lệch nhau. Codex, Copilot và `agy` cài một bản copy, nên sau khi sửa kit bạn phải cài lại; Codex lưu bản copy theo thư mục từng version (`~/.codex/plugins/cache/dev-kit/dk/<version>/`), nên bắt buộc phải nâng version.

## 7.6 Giấy phép

Cả ba nguồn đều là MIT. Các file LICENSE gốc nằm trong [`LICENSES/`](../../LICENSES/). Hãy giữ nguyên chúng khi phân phối.

## 7.7 Hỗ trợ nhiều CLI

Làm theo Superpowers v7.0.0: một bộ `skills/`, mỗi CLI một manifest, khác biệt nằm trong `harness/<cli>.md`. Không tách nội dung controller theo CLI.

- **Thêm một CLI mới:** thêm manifest (nếu CLI có định dạng plugin), thêm một dòng vào `.version-bump.json`, viết `harness/<cli>.md`, và thêm tên CLI vào đoạn Harness của 5 controller.
- **Kiểm sau khi đổi controller hoặc khi CLI ra bản lớn:** cài kit, rồi bảo agent nạp `pre-pr-check` và chỉ làm theo đoạn Harness, và trả về thư mục kit, dòng đầu của `rules/RULES.md`, file ghi chú đã đọc, và tên công cụ subagent. Đạt khi cả bốn đều đúng.
- **Ba điều không được làm,** rút ra từ ADR 0002 của mattpocock/skills và một lần thử ngày 2026-10-14:
  - đưa `parts/` vào trong `skills/`: Codex và Cursor dò skill đệ quy, nên part sẽ thành skill và tốn context lúc mở phiên;
  - gom file bằng symlink trong plugin: Codex bỏ symlink khi cài;
  - khai nguồn marketplace của Codex kiểu `"url": "./"`: Codex coi đó là repo git và `git clone` thất bại; hãy dùng `"source": "local", "path": "./"`.
