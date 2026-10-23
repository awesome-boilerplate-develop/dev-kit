<!-- i18n: source=docs/en/06-evidence.md source_commit=v1.7.2 review=human -->
[English](../en/06-evidence.md) | Tiếng Việt

> Bản dịch này có thể chậm hơn bản tiếng Anh; bản tiếng Anh là bản chính thức. Xem [bản tiếng Anh](../en/06-evidence.md).

# 6. Bằng chứng

Mọi số liệu trong tài liệu này đến từ lab của dev-kit (private). Kết quả từng lần chạy, kèm code agent làm ra, được giữ ở các repo demo private.

## 6.1 Lab đo gì

| Mục | Cách làm |
|---|---|
| Model, host | Haiku 5.5 (`claude-haiku-5-5`), Claude Code 2.1.296, chạy headless (`claude -p`) |
| Cô lập | `--setting-sources project,local`, MCP rỗng với `--strict-mcp-config`, chỉ nạp plugin đang thử qua `--plugin-dir`. Đã kiểm agent không thấy plugin, hook, MCP hay CLAUDE.md nào của máy host |
| So với gì | **baseline**: cùng model, không cài bộ nào; 3 bộ gốc dùng riêng; các phiên bản của bộ trộn |
| Bài thử | 9 ticket trên app mẫu giỏ hàng (story, bug, perf, refactor, 3 ticket pre-PR có lỗi cài sẵn) và 13 bài SWE-bench Verified (Django 4.0–5.0) |
| Chấm | Test ẩn (agent không thấy). Pre-PR: Sonnet 5.5 đối chiếu báo cáo với danh sách lỗi cài sẵn. SWE: như harness SWE-bench (đưa các file test về gốc, áp test của bản sửa thật, chạy FAIL_TO_PASS và các module test liên quan) |
| Kiểm đề | Mọi bài SWE: code gốc trượt, bản sửa thật thì qua. Ticket trên app mẫu: lời giải mẫu qua, code gốc trượt |

Tổng: 265 lần chạy, khoảng 12.4 USD (chi phí do Claude Code báo trong transcript).

## 6.2 Kết quả chính

**So sánh các cách chạy** (USD/lần chạy là trung bình trên các bài cùng nhóm):

| Cách chạy | Chất lượng so với baseline | Chi phí so với baseline |
|---|---|---|
| Superpowers | Ngang | ~1.5–14× |
| Matt Pocock | Ngang; có một lần controller dừng giữa chừng (bug B3) | ~1.5–3× |
| agent-skills | Ngang | ~1.4–3× |
| Bộ trộn v0.2 (gộp hết các part nặng) | Ngang | ~3–13× |
| Bộ trộn v0.3 | Ngang | ~3× |
| **v0.4.1 = dev-kit 0.5.x** | **Ngang** (điểm trung bình 0.864 so với 0.848) | **~2×** |

**v0.4.1 theo nhóm việc:**

| Nhóm | baseline | v0.4.1 | Tỉ lệ |
|---|---|---|---|
| Bug (3 ticket) | 0.023 | 0.041 | 1.8× |
| Pre-PR (3 ticket) | 0.031 | 0.089 | 2.8× |
| Refactor | 0.012 | 0.029 | 2.4× |
| Story (2 ticket) | 0.032 | 0.067 | 2.1× |
| SWE (13 bài) | 0.223 | 0.429 | 1.9× |

## 6.3 Thử với Sonnet 5.5 và trên repo thật (dev-kit 0.5.1)

**Sonnet 5.5, 5 bài SWE khó, mỗi bài 2 lần:**

| Bài | baseline | dev-kit |
|---|---|---|
| 15916 | 1/2 | 1/2 |
| 16256 | 1/2 | 0/2 |
| 16263 | 0/2 | 0/2 |
| 16560 | 2/2 | 2/2 |
| 16631 | 2/2 | 2/2 |
| **Tổng** | **6/10** | **5/10** |
| USD/lần chạy | 0.129 | 0.165 |

- **Chất lượng:** ngang nhau; chênh 1 bài nằm trong dao động ngẫu nhiên.
- **Chi phí:** với Sonnet, phần chi phí cộng thêm của dev-kit nhỏ hơn hẳn so với Haiku (khoảng 1.3×, so với khoảng 2× của Haiku).
- **Sonnet tự giải được** 16560 và 16631; Haiku thường trượt cả hai.

**Lặp lại 9 ticket với Haiku (0.5.1):** đạt hết, tổng chi phí 0.221 USD so với 0.226 của 0.4.1, nên không có regression.

**Một repo thật** (Node monorepo, Postgres thật, chạy trên bản copy), model Sonnet 5.5:
- **`dk:init`:**
  - chỉ đọc trước, rồi in kế hoạch và hỏi 4 câu trước khi làm;
  - nhận đúng monorepo (không có `package.json` ở gốc) và ghi lệnh test cho cả hai package;
  - baseline xanh (65 + 8 test);
  - tạo `.dev-kit/`, `.gitignore`, và chạy `codegraph init` theo các câu trả lời;
  - cảnh báo rằng plugin Superpowers đang được cài.

  Có một điểm bất thường: test Postgres vẫn pass dù người trả lời đã nói "chưa có Postgres". Agent ghi điều này vào báo cáo mà không bịa lý do. Kiểm lại thì máy có Postgres đang chạy qua OrbStack.
- **`dk:story-runner`** (ticket "ghi thời điểm xuất bản + lọc theo trạng thái"):
  - phát hiện nửa đầu đã có sẵn nên không làm lại;
  - thêm bộ lọc ở admin kèm 4 test (đã kiểm các test chuyển đỏ khi bỏ code);
  - pre-pr-check tự review (self-review), GO;
  - spec có mục Decisions, PR body có Evidence và Merge Danger.

  Vì chạy bằng `claude -p`, agent không dừng lại hỏi mà tự quyết và đánh dấu 3 giả định. Cách `grilling` hỏi một người thật vẫn chưa được kiểm.

**Lỗi áp rule đã sửa ở 0.5.2:** ở P3 (10 file, 170 dòng), agent tự review dù rule C2 yêu cầu 1 reviewer. Từ 0.5.2, pre-pr-check đo diff bằng `git diff --shortstat` trước khi chọn mức review.

### Công cụ đồ thị (dev-kit 0.7.0, rule G1)

17 lần chạy SWE Django mỗi bên, Haiku 5.5. Bên có index được dựng sẵn index codegraph và code-review-graph:
- **Kết quả:** giải được 10/17 cả hai bên; chi phí 0.034 so với 0.033 USD/lần chạy.
- **Cách agent tìm code đã đổi:** agent thật sự dùng đồ thị (27 lệnh codegraph, 33 lệnh CRG) và grep ít đi khoảng một nửa (31 so với 58).
- **Bài 16560:** CRG chỉ ra `__repr__` và `__eq__` chưa có test; có index thì giải 2/2, không có thì 1/2. Số lần chạy quá ít để kết luận.
- **0.8.0 (playbook):** 12/17, 0.031 USD/lần chạy.
  - Lệnh dùng nhiều nhất: `detect-changes` 21 lần, `codegraph sync` 14, `tests_for` 4; các lệnh còn lại vài lần.
  - 3 ticket R1, B3, P3 có index đều đạt.
  - Phát hiện: `codegraph affected` không tìm ra test Python, nên đã thay bằng `tests_for`.

### Thử trên một repo private thật ở công ty (dev-kit 0.8.x, Sonnet 5.5)

Chạy trong một git worktree riêng, không commit, không push. Repo là một Angular micro-frontend private, khoảng 1,500 file và khoảng 9,500 spec.
- **`dk:init`:**
  - tự tìm script test headless, dựng hai index (135 MB và 497 MB), build xanh;
  - baseline đỏ (290 spec); kiểm lại thì nhánh gốc cũng đỏ (303 spec). Từ đây có rule B1 và `templates/baseline.md`.
- **`pre-pr-check`** (chế độ report-only) trên diff của một PR đã merge (22 file, +1,569 dòng):
  - **0.8.1:** đọc sai đường dẫn `../../rules/` (tính theo thư mục đang đứng), nên bỏ qua `detect-changes`; chọn 1 reviewer; 1 major, 9 minor; 0.42 USD.
  - **0.8.2:** đường dẫn đổi sang `${CLAUDE_PLUGIN_ROOT}`, và C2 nay ghi rõ dữ liệu y tế. Agent chạy đủ `sync`/`update`/`detect-changes`, dùng 4 reviewer, và ra 2 major (gồm một test yếu: vẫn pass khi xóa phần xử lý lỗi) cùng một rủi ro bảo mật cần backend xác nhận; 0.87 USD.
  - **Kiểm tra theo baseline:** 290 test fail khớp đúng danh sách, 0 fail mới, nên đạt.
- **Từng finding đúng hay sai:** chưa có người kiểm ❓.

### Backtest `pre-pr-check` trên bug thật (repo private ở công ty, Sonnet 5.5)

8 bug đã sửa; với mỗi bug, tìm PR hoặc commit gây ra nó. Review lại PR đó ở chế độ report-only, rồi Sonnet chấm xem báo cáo có chỉ ra bug không.

| | 0.8.2 | 0.8.4–0.8.5 |
|---|---|---|
| 6 PR, mỗi PR 1 lần: bắt được / một phần | 1 / 3 | 0 / 2 |
| PR C (bug rõ nhất), lặp lại: bắt được | 3/4 | 1/4 (lần bắt được nằm ở tầng suspect, điểm 70) |
| PR D (3 bug UI form), lặp lại | gần như trượt hết | gần như trượt hết |
| `detect-changes` chạy | 2/6 | **6/6** |
| Báo cáo đạt `check_report` | – | **6/6** |
| Độ chính xác của tầng "certain" (agent tự kiểm, 0.8.4; người dùng giao agent quyết định, chưa có người xác nhận) | – | 5/9; bỏ các mục "thiếu test" thì còn 2/6 |

**Đọc kết quả:**
- **Ép tuân thủ có hiệu quả.**
- **Khả năng bắt bug dao động mạnh giữa các lần chạy;** không thấy cổng (gate) làm mất bug nào.
- **Các finding sai ở tầng certain** chủ yếu là code có sẵn từ trước hoặc thay đổi có chủ ý.
- **Một nửa số bug** cần biết hành vi lúc chạy hoặc hợp đồng với backend, nên khó bắt bằng cách review diff.
- **Một finding sai do cách dựng diff** cho PR merge hai parent (kéo cả code của PR khác vào). Backtest đã được sửa; kết quả ở mục dưới.

**PR merge hai parent, dựng lại diff đúng phạm vi (dev-kit 0.8.7):** worktree đặt tại chính merge commit, base là parent thứ nhất, nên diff chỉ còn phần thay đổi của riêng PR (PR A: 12 file; PR B: 26 file). Mỗi PR chạy 1 lần.

| PR | Bug | 0.8.2 (diff rộng) | 0.8.4 (diff rộng) | 0.8.7 (diff đúng) |
|---|---|---|---|---|
| PR A | Một request sort gửi tên cột UI vào `SortString`, backend từ chối | trượt | trượt | **bắt được**, ở tầng suspect (điểm 70) |
| PR B | Double submit: bấm Submit nhiều lần khi request đang chạy | một phần | trượt | trượt |

- **Tầng "certain" (agent tự kiểm, chưa có người xác nhận):**
  - PR A không còn finding certain nào; các finding sai biến mất vì code của PR khác không còn trong diff.
  - PR B có 3/3 finding đúng: RBAC gán cứng `true` (giá trị nhất, đã thấy ở 0.8.4), một test filter dùng `every()` trên mảng có thể rỗng, và `en.json` có 62/48 dòng chỉ đổi khoảng trắng. Hai mục sau đúng nhưng ít giá trị.
  - Ba mục "thiếu test" mà 0.8.4 xếp vào tầng certain nay nằm ở tầng suspect, đúng theo cổng R1.
- **Cả hai báo cáo đạt `check_report --base`** (0.87 và 1.09 USD).
- **Lỗ hổng tuân thủ mới:** ở PR A, agent chỉ chạy `ls .dev-kit .codegraph`, rồi ghi "no .code-review-graph/ index" và bỏ qua `detect-changes`, dù index đã được dựng trước khi chạy. `check_report` chỉ kiểm dòng Graph có mặt, không kiểm nội dung có đúng không.
- **Sửa ở 0.8.8, chạy lại PR A một lần:** agent kiểm bằng `test -d`, chạy `detect-changes` (risk 0.85, 17 test gap), báo cáo đạt `check_report`; bug sort vẫn bắt được ở tầng suspect (điểm 70); 0.74 USD. Lỗ hổng còn lại: 2 finding "certain" (điểm 82 và 80) thực chất là thiếu test, nhưng được viết kiểu "No service spec covers…" và "Only 404 … is tested", nên regex "thiếu test" của `check_report` không bắt được.
- **0.8.9–0.8.10, chặn các mục thiếu test ở tầng certain theo vị trí và theo cột Rule:**
  - 0.8.9 (FAIL khi một mục chỉ trỏ vào file test và không có rule), chạy lại PR A: cả 6 mục certain đều là thiếu test, nhưng cột Rule ghi `R1`, nên vẫn lọt.
  - 0.8.10 (chỉ id tiêu chuẩn `topic/name#X` hoặc một spec mới được tính là rule), chạy lại PR A: agent nhận FAIL, chuyển các mục thiếu test xuống suspect, và chạy `check_report` 4 lần cho tới khi đạt. Tầng certain còn 1 mục minor (một khối xử lý lỗi lặp lại); bug sort vẫn bắt được ở tầng suspect (70); 0.75 USD.
  - Trên 16 báo cáo cũ, các báo cáo vốn đạt vẫn đạt. Kiểm tra dòng Graph bắt thêm một lần bỏ qua `detect-changes` (một lần chạy lặp PR D, 0.8.5), tức 2/16 báo cáo có lỗi này.
  - **Đọc kết quả:** agent khai thác mọi kẽ hở của một rule viết bằng lời (ghi `R1` vào cột Rule); kiểm tra bằng máy phải dựa trên thứ khó lách (vị trí file, định dạng id của rule), không dựa trên câu chữ.

### Rule của dự án: control nội bộ (dev-kit 0.8.7, rule T1)

Ticket "dialog form" (input, select, textarea, toggle, button), `dk:story-runner`, Sonnet, 2 lần mỗi bên:
- **Có rule:** dùng control nội bộ (6 và 10 tag), Material chỉ ở chỗ được phép.
- **Không có rule:** dùng toàn Material (18 và 16 tag), 0 control nội bộ.
- **Test xanh cả 4 lần.** Chi phí tăng khoảng 25%.

**Kết luận:** rule về điều agent không thể tự biết thì có hiệu quả rõ; rule về điều agent vốn đã tự làm thì không (xem mục trước về các rule chung).

**Quyết định phạm vi cho rule (2026-10-14, agent quyết định dựa trên dữ liệu repo):**
- **Chỉ trong phạm vi dự án** (`scope: project`): chỉ một trong ba repo dùng thư viện v2 (105 file import v2); hai repo còn lại có 0 file. Chưa đủ cơ sở để nâng lên thành rule của team.
- **v1:** cấm trong code mới khi v2 có component cùng mục đích. Một table skeleton loader và một helper form-object chưa có trong v2, nên vẫn được dùng.
- **Material được phép:** dialog service và các dialog container, tooltip, snackbar, spinner, input chips, CDK overlay. Bản thử trước đó miễn cả datepicker, nhưng v2 có datepicker và datetimepicker, tab group, autocomplete, paginator và color picker, nên các component này đã chuyển sang U1.

### Nhiều CLI (dev-kit 0.8.12)

**Dò thử bằng một plugin giả** (bố cục giống dev-kit: skill trong `skills/`, file cần đọc nằm ở `rules/` hai cấp phía trên; mỗi CLI 1 lần):

| CLI | Thay `${CLAUDE_PLUGIN_ROOT}` | Agent biết đường dẫn `SKILL.md` | Đọc được file hai cấp phía trên | Công cụ subagent |
|---|---|---|---|---|
| Claude Code 2.1.299 | có | có | có | `Agent` |
| Codex 0.160.1 | không | có (bản copy cả cây trong cache) | có | `spawn_agent` |
| Antigravity 1.3.5 | không | có (bản copy cả cây) | có | `invoke_subagent` |
| Copilot CLI 1.0.89 | không | có | có khi đã cài; với `--plugin-dir` phải thêm `--add-dir` | `task` |
| OpenCode 1.18.35 | không | đường dẫn symlink | có, sau khi resolve symlink và cho phép `external_directory` | `task` (`general`) |
| Cursor | – | – | – | chưa chạy được: cần `cursor-agent login` (bỏ hỗ trợ từ 1.2.3) |
| omp 18.10.4 | không | có | có | `task` |
| pi 1.0.2 | không | có | có | không có (pi lõi); tạm dừng hỗ trợ từ 0.8.13 |

**Kiểm với dev-kit thật:** cài kit, rồi bảo agent nạp `pre-pr-check` và chỉ làm theo đoạn Harness. Claude Code, Codex, Copilot, Antigravity, OpenCode, omp và pi đều trả đúng thư mục kit và dòng đầu của `rules/RULES.md`. Sáu CLI không phải Claude Code đều đọc đúng file `harness/<cli>.md` của mình. Trên omp (nạp bằng `--plugin-dir`), `security-auditor` và `test-engineer` hiện thành các task agent có tên.

**Backtest PR A, 1 lần mỗi bên:**

| | Claude Code (Sonnet 5.5) | Codex 0.160.1 (model mặc định của tài khoản) |
|---|---|---|
| Bug sort (`SortString`) | một phần (4 lần chạy trước, 0.8.7–0.8.10: bắt được) | bắt được, ở tầng suspect |
| `detect-changes` | chạy (risk 0.85, 17 test gap) | chạy (risk 0.85, 17 test gap) |
| Độ sâu review | bốn reviewer | bốn reviewer: 4 lần gọi `spawn_agent` với `fork_turns: "none"` (xem trong rollout của phiên) |
| `check_report` | đạt | đạt |
| Chi phí | 0.77 USD | 1.12 triệu token đầu vào (1.04 triệu từ cache), 4.6 nghìn token đầu ra |

**Đọc kết quả:**
- **Kit chạy được trên Codex với đủ luồng** (đồ thị, bốn reviewer, cổng kiểm báo cáo) mà không phải sửa nội dung controller nào.
- **Kết quả "một phần" ở lần chạy Claude chỉ là một lần duy nhất.** Đoạn Harness không đổi hành vi trên Claude Code (biến vẫn được thay), nên nhiều khả năng đây là dao động giữa các lần chạy; chưa chạy lặp để xác nhận.
- **Chất lượng review trên Copilot, Antigravity, OpenCode và omp chưa đo;** mới kiểm là nạp được.
- **pi tạm dừng (0.8.13):** nạp được nhưng không có subagent, nên các vai review chạy trong phiên chính; cách chạy này chưa được đo, nên chưa hỗ trợ.

**Rule trên các CLI khác:** các rule và bằng chứng ở trên được đo trên Claude. Trên Codex mới có 1 lần backtest; cần chạy lặp trước khi coi một rule là có ích trên CLI đó.

### Câu hỏi của `dk:init` trên 3 repo thật (dev-kit 1.2.0–1.2.2)

Git worktree mới của ba repository private, Claude Code với Sonnet 5.5, mỗi lượt một câu trả lời với `--resume`; mọi câu hỏi đều trả lời "default" (đã đọc lại để xác nhận). Đối chiếu với docs 09 §9.8: tối đa 12 câu hỏi, các câu trả lời đoán phần lớn đúng.

| Repo | Câu hỏi (tiêu chuẩn) | Probe đã đề xuất gì | Chi phí (USD) |
|---|---|---|---|
| A: Angular micro-frontend, ~840 file `.ts` | 9 (4) | Thư viện component nội bộ: 110 file dùng v2, 7 file dùng v1, 36 template dùng control của framework; một rule dự án được soạn và đọc lại | 0.33 |
| B: Angular micro-frontend, ~390 file `.ts` | 10 (4) | Bộ control riêng của repo (18 control trong một thư mục, 11 template dùng chúng, còn 77 form field của framework); một rule dự án được soạn và đọc lại | 0.40 |
| C: .NET API, ~290 file `.cs` | 8 (3) | Không có rule dự án; topic `ui` bị bỏ qua (không có UI). Test không chạy được: package restore lỗi trên một feed private | 0.23 |

- **≤ 12 câu hỏi:** đạt (3–4 câu hỏi về tiêu chuẩn, tổng 8–10 câu). `git status` không đổi ở cả ba repo.
- **Câu trả lời đoán** (agent tự kiểm với code, không phải người xác nhận): đề xuất cho repo B đưa ra 7 nhận định, 6 đúng; nhận định sai nói rằng control mới thay control cũ, trong khi code dùng control cũ nhiều hơn (16 so với 10 và 11 so với 0). Các con số của repo A khớp với những lần đếm thủ công trước đó trên repo ấy.
- **Sai lệch, đã sửa ở 1.2.2:**
  - "default" đã tick các file kit `experimental` ở B và C (A để tắt), dù skill nói chúng bắt đầu ở trạng thái không tick → "default" giờ không bao giờ tick file `experimental` và không giữ rule đề xuất nào.
  - Một hướng migration được nêu mà không có bằng chứng sử dụng → mọi con số phải đến từ một lệnh agent đã chạy, và một hướng không có bằng chứng thì được hỏi dưới dạng câu hỏi.
  - Test không chạy được chưa có đường xử lý xác định; agent tự ứng biến "not measured" → giờ là một nhánh xác định (`baseline: not-measured` trong `config.yml`).
  - Khi không có rule nào được soạn, bước đọc lại bị gộp vào câu hỏi mở ở C → giờ được phép.
- **Sau khi sửa (repo B, chỉ các câu hỏi theo topic):** câu hỏi `coding` nêu "experimental, nên mặc định là tắt", và những ý chưa được chứng minh (`: any` trong 124 file, kiểu unsubscribe) được hỏi dưới dạng câu hỏi. Lần chạy thứ hai còn đề xuất các rule `architecture` mà lần đầu đã bỏ qua: những gì probe tìm thấy thay đổi giữa các lần chạy.

### Tiêu chuẩn của `dk:init` theo hai lượt (dev-kit 1.4.0)

Một lần chạy `dk:init standards` trên repo B (worktree mới, `.dev-kit/` từ lần chạy trước với phần tiêu chuẩn đã xóa), Claude Code với Sonnet 5.5, mỗi lượt một câu trả lời với `--resume`; phần lớn là "default", một quy ước riêng, "no" để kết thúc mỗi vòng lặp. Một lần chạy duy nhất, do agent tự kiểm, chưa được người xác nhận.

- **Lượt 1:** 9 câu hỏi: architecture (7 mục từ probe, như contract module federated, file permission key và pattern của key, giá trị trong mọi file environment, key trong cả hai file dịch), 4 file kit (`security/web` được khuyến nghị bỏ S1 và S3, `ui/forms-and-actions` bỏ U5, mỗi cái kèm lý do), thư viện nội bộ (5 package nhưng chỉ 2 file import, so với 30+ component riêng: Recommended là "không có rule"), 2 lượt của vòng lặp, 1 lần đọc lại.
- **Agent đã kiểm quy ước riêng của người dùng với code:** "mở dialog thêm/sửa qua `common-dialog`" gặp 3 file dùng nó và 54 file dùng thẳng dialog service; nó viết rule đúng như được nói và nêu khoảng chênh ở bước đọc lại.
- **Lượt 2:** 5 câu hỏi: severity, các kiểm tra chỉ dành cho review, Do not flag (cờ compiler, `.editorconfig`, Sonar trong CI), 1 lượt của vòng lặp, 1 lần đọc lại. Các mục được đặt dưới `## Review`, `## Do not flag` và `## Severity` của cùng hai file dự án; `git status` không đổi.
- **Chi phí:** 0.60 USD cho 15 lượt (lượt 1 + lượt 2 + câu hỏi `CONSTRAINTS.md`).
- **Sai lệch, đã sửa ở 1.4.0 và chạy lại ở lượt 2:** "default" kết thúc các vòng lặp (giờ chỉ "no" hoặc "skip" mới kết thúc; chạy lại: vòng lặp hỏi lại sau "default"); các kiểm tra chỉ dành cho review nhắc lại rule của lượt 1, ví dụ key dịch và giá trị environment (giờ đã loại ra; chạy lại: agent bỏ chúng và nói lý do); một rule về vị trí đặt code mà code lân cận đã cho thấy lại được khuyến nghị (giờ không đưa vào Recommended, chưa chạy lại).

### `dk:init` trên 6 CLI, một repo private (dev-kit 1.4.3, sửa ở 1.4.4)

Mỗi CLI chạy một lần trên một worktree mới của một micro-frontend Angular private (~850 file được index, baseline đỏ 303 test). Tin nhắn đầu là `dk:init` kèm "hỏi và trả lời bằng tiếng Việt"; agent điều phối đóng vai người dùng theo kịch bản cố định (default, thêm một quy ước và một kiểm tra riêng, trả "không" để kết thúc vòng lặp). Agent tự kiểm, chưa có người xác nhận.

| CLI | Model | Lượt | Thời gian | Chi phí | Kết quả |
|---|---|---|---|---|---|
| Claude Code 2.1.299 | Sonnet 5.5 | 22 | ~13 phút | 1,15 USD | đủ |
| Codex 0.162.1 | model mặc định của tài khoản (`gpt-6-luna`) | 22 | ~31 phút | chỉ báo token | không ghi lượt 2 |
| Copilot CLI 1.0.89 | Auto | 22 | ~33 phút | 10,56 AIC | đủ (chạy tương tác; headless không hỏi gì) |
| Antigravity 1.3.5 | không báo | 22 | ~22 phút | chỉ báo token | đủ |
| OpenCode 1.18.35 | một model miễn phí | 20 | ~27 phút | 0 | đủ, sau 4 lần khởi động hỏng |
| omp 18.11.0 | Sonnet 5.5 qua Copilot | 22 | ~14,5 phút | ~1,51 USD | đủ |

- Cả 6 CLI đều hỏi bằng tiếng Việt và `git status` không đổi.
- **Cùng repo, kết quả khác nhau:** từ 3 đến 7 file standards của repo, từ 11 đến 34 dòng mục.
- **Các lệch tìm thấy:**
  - 3 CLI lấy base branch theo `origin/HEAD` (nhánh cập nhật lần cuối từ hai tháng trước), trong khi các PR gần đây merge vào một nhánh khác đi trước 1.181 commit;
  - đường dẫn `.git/info/exclude` hỏng trong worktree; hai CLI báo đã thêm exclude mà không có lệnh ghi; `.dev-kit/` bị thêm dù `.gitignore` riêng của nó đã ẩn nó;
  - dung lượng index bị ước thấp khoảng 2 lần theo con số cũ "mỗi 3.000 file" (đo được 136 MB và 529 MB cho ~850 file);
  - hai CLI chạy bộ test hai lần để lấy tên test lỗi;
  - Codex coi câu đọc lại chưa được trả lời là bị từ chối và mất lượt 2;
  - hai câu hỏi trong một tin; dòng Recommended thiếu mục mà chính nội dung đã đề xuất; ID mục đã xác nhận bị đổi khi ghi; một kiểm tra phụ thuộc mô tả PR được xác nhận mà không nói reviewer chỉ thấy diff.
- **Đã sửa ở 1.4.4 và chạy lại** (cùng repo, worktree mới, mỗi bên 1 lần):
  - Claude Code, bước 1–6: base branch được hỏi thành lựa chọn kèm ngày, số commit và bằng chứng merge, đề xuất đúng nhánh; `.codegraph/` được thêm vào file exclude ngay ở bước 5 (`git status` sạch, không có dòng `.dev-kit/`); output test và build ghi vào `.dev-kit/baseline-*.log`, bộ test chạy một lần; không còn câu xin phép giữa các bước sau lần sửa thứ hai (lần chạy lại đầu hỏi "chạy luôn nhé?" trước baseline và hoãn dòng exclude sang bước 9); dòng Recommended tiếp theo khớp nội dung. Ước tính dung lượng đếm cả 1.455 file trong `src/` (230 MB và 870 MB), vẫn cao hơn thực tế.
  - Codex, `dk:init standards review` từ trạng thái lượt 1 của lần chạy trước: câu đọc lại là một tin riêng, agent chờ, và sau "ok" thì ghi checklist review (`## Review`, `## Do not flag`, `## Severity`).
- Chưa chạy lại để kiểm việc giữ ID mục và cảnh báo về mô tả PR.

### Từ `dk:init` đến `dk:pre-pr-check` trên cùng một repo (dev-kit 1.4.7)

Controller có dùng những gì `dk:init` đã ghi không? Một lần chạy với agy 1.3.5 (Gemini 3.8 Flash), headless, chế độ chỉ báo cáo, trên bản clone local của repo private, sau một lần `dk:init` tương tác (3 file standards của repo, 5 file kit, tắt `security/web#S1`). Diff là một nhánh feature thật chưa merge, checkout detached (không tạo commit): 4 commit, 38 file, khoảng 3.500 dòng thêm. Agent tự kiểm, chưa có người xác nhận.

- **Đã nạp:** mục Review setup của báo cáo liệt kê 5 file kit và 3 file của repo; mức review bốn reviewer (dữ liệu bệnh nhân và config, rule C2); `detect-changes` đã chạy (risk 0,55).
- **Rule của repo bắt được một vấn đề thật:** nhánh viết cứng hai chuỗi quyền trong một file model thay vì lấy từ file key quyền tập trung; báo cáo xếp nó vào tầng chắc chắn, mức major (độ tin cậy 90), trích `architecture/structure#A4`, rule mà `dk:init` đã soạn từ probe. Một phát hiện chắc chắn khác trích `ui/in-house-components#I2` của repo (thiếu key dịch). Rule `#A5` và `#D1` của repo được trích ở tầng nghi vấn, cho code mà chính agent ghi là nằm ngoài diff (R1 quy định phát hiện như vậy phải bỏ, không liệt kê).
- **Rule của kit** mang 4 blocker (`security/web#S2`, `#S3`, `#S4`, `coding/review-basics#C1`); verdict NO-GO.
- `check_report.py --base <base>` báo OK (agent điều phối chạy lại); `git status` không đổi; khoảng 19,5 phút.

### Probe ưu tiên graph trong `dk:init` (dev-kit 1.4.10)

Bước dò của phần standards có dùng các index graph mà nó dựng không? Trước đây thì không: trên agy, các lần chạy `dk:init` trong ngày chỉ gọi 0–1 lệnh truy vấn graph mỗi lần, so với 2–20 lệnh grep/find, và lệnh duy nhất skill nêu tên, `codegraph callers HttpClient`, không tìm thấy gì (class của framework không có trong graph). Bản 1.4.10 nêu lệnh graph cụ thể cho từng mục dò. So sánh A/B trên cùng bản clone, agy 1.3.5 (Gemini 3.8 Flash), `dk:init standards` headless, index và baseline đã có sẵn; agent tự kiểm, chưa có người xác nhận:

| Lần | Skill | Thời gian (s) | Token | Lệnh graph | grep/find | File / mục |
|---|---|---|---|---|---|---|
| A1 | 1.4.9 | 360 | 280.446 | 0 | 12 | 4 / 12 |
| A2 | 1.4.9 | 507 | 348.517 | 0 | 17 | 6 / 22 |
| B1 | 1.4.10 | 385 | 255.961 | 6 | 10 | 6 / 19 |
| B3 | 1.4.10 | 354 | 298.904 | 8 | 9 | 6 / 19 |

- Lần B thứ ba (B2) dừng sau câu hỏi đầu: agent viết câu hỏi dạng chữ thay vì dùng công cụ chọn, nên agy headless không có gì để tự bỏ qua. Không tính; đây là biến động của chế độ headless, không phải tác động của graph.
- **Graph được dùng:** các lần B gọi `code-review-graph architecture`, `codegraph explore` cho cách gọi backend, phân quyền, cấu hình, class nền dùng chung và dữ liệu bệnh nhân, và `codegraph callers RbacService`; grep/find giảm khoảng một phần ba; cả hai lần đều liệt kê lệnh graph trong `init-report.md`.
- **Tốc độ và chi phí:** B trung bình 370 s và 277 nghìn token, so với A 434 s và 314 nghìn; với 2 lần mỗi bên và A dao động từ 360 đến 507 s, kết luận là "không chậm hơn", chưa phải đã đo được là nhanh hơn.
- **Rule:** hai bên ra phần lớn cùng các sự thật; B có thêm chi tiết chỉ graph mới thấy, như các service theo bệnh nhân kế thừa một service nền dùng chung. Cả bốn lần đều qua `check_standards.py`.

### Form chọn dễ đọc và độ phù hợp với stack trên omp (dev-kit 1.4.11)

Một lần chạy `dk:init` tương tác của người dùng trên omp với một app React Native (bản 1.4.10) cho thấy ba câu hỏi kit liên tiếp (`testing`, `security`, `ui`) mà phần đánh giá chỉ nằm trong phần suy luận của agent: form ghi "Giữ U2, tắt U1/U3/U4/U5" mà không nói các ID đó là gì, và `security/web` được đưa cho một app di động. Bản 1.4.11 yêu cầu một tin nhắn thường trước mỗi nhóm, các lựa chọn phải giải thích ID, và mỗi mục nói rõ có hợp với stack không.

Chạy lại với 1.4.11 trên omp (GPT-6.1 Sol), `dk:init standards` trên bản clone mới của cùng app, chế độ tương tác; agent tự kiểm, một lần chạy:

| Nhóm | Tin nhắn trước form | Form |
|---|---|---|
| kiến trúc, `coding`, `testing`, `security`, `ui` | một tin nhắn thường kèm bảng 6–8 dòng (mục, lý do, bằng chứng trong repo), lần nào cũng có | phần câu hỏi liệt kê từng ID kèm vài chữ; nhãn vẫn chỉ nêu ID, dòng mô tả nói ý nghĩa |

- **`security/web`:** tin nhắn nói tên là "web" nhưng file bao gồm app di động, hiểu `localStorage` là storage thiết bị không mã hóa (`AsyncStorage`), đánh dấu các mục phía server S1–S3 là không áp dụng cho app client, và khuyến nghị S4–S6.
- **Còn lại:** nhãn kiểu "Giữ S4, S5, S6; tắt S1, S2, S3" vẫn chỉ nêu ID; ý nghĩa nằm ở phần câu hỏi và dòng mô tả.
- Lần chạy đầu của đợt này mất vì script driver của mình (kiểm tra ổn định trên dòng trạng thái, rồi một từ khóa trùng với lựa chọn "dừng" ở baseline đỏ), không phải do kit.

### Thiết lập nhanh và các mục không đưa ra trên omp (dev-kit 1.6.0)

`dk:init` đầy đủ, chế độ tương tác, trên omp (GPT-6.1 Sol) với bản clone mới của cùng app React Native, chọn thiết lập nhanh, mọi câu khác chọn phương án Recommended; agent tự kiểm, một lần chạy.

| | Chi tiết (1.4.11, chỉ phần tiêu chuẩn) | Nhanh (1.6.0, init đầy đủ) |
|---|---|---|
| Số câu hỏi | 8 câu cho phần tiêu chuẩn | 5 câu tổng cộng: lệnh, index, nhanh hay chi tiết, baseline đỏ, một lần đọc lại |
| Thời gian | ~12 phút cho phần tiêu chuẩn | ~15 phút cho cả init |

- **Lần đọc lại duy nhất** liệt kê từng file kit kèm các mục được giữ và bằng chứng (C1–C5, S4–S6, U1–U3, U5), các mục bị tắt kèm lý do (T1–T4 vì không có test runner, U4 vì không có luồng ghi danh sách), S1–S3 là không đưa ra (không có handler server, không có UI kiểm quyền theo role, không có chỗ injection, kèm ghi chú rằng tìm không thấy không chứng minh repo an toàn), và ba kiểm tra chỉ dành cho review sẽ được ghi.
- **Đã ghi sau khi chọn "ghi tất cả":** 3 file của repo trong `ops/` và `ui/`, `standards.disable` gồm S1–S3 và U4, `check_standards.py` OK, `init-report.md` ghi rõ dùng thiết lập nhanh và các dòng Recommended đã lấy, không tạo `CONSTRAINTS.md`, `git status` không đổi.
### Checklist tick sẵn và form tick trên omp (dev-kit 1.7.0)

Hai lần chạy `dk:init standards` tương tác trên omp (Opus 5.5) với bản clone React Native đã xóa phần tiêu chuẩn, SKILL 1.7.0 chép đè lên bản 1.6.0 đã cài; agent tự kiểm, các lựa chọn do script driver bấm.

| | Lần 1: ghi như đã tick (`A`) | Lần 2: đổi tick bằng form (`B`) |
|---|---|---|
| Số câu hỏi | 2 (nhanh hay chi tiết, đọc lại) | 7 (nhanh hay chi tiết, đọc lại, 4 form, xác nhận) |
| Thời gian | ~7 phút | ~12 phút |
| Kết quả | 4 file kit, tắt S1–S3 và U4 | như lần 1, thêm C5 tắt, `init-report.md` ghi là do người dùng đổi |

- **Form:** nhãn ghi trạng thái bằng chữ (`bật · C1 …`, `tắt · S1 …`), mục giữ nguyên nằm cuối và được chọn sẵn làm Recommended; omp tick bằng `␣` và gửi bằng `⏎`.
- **Chỗ hụt, đã sửa trong skill:** lần 1 gom S1–S3 vào ghi chú "không đưa ra" thay vì dòng `☐`; một dòng Do-not-flag được tick nhưng chưa có file khiến agent tự tạo `coding/baseline.md` sau khi đã duyệt. Sau khi đổi tick, agent nêu thay đổi ngay trong câu hỏi ("C5 đã tắt") thay vì hiện lại checklist; skill giờ chỉ yêu cầu hiện lại các dòng đã đổi.

## 6.4 Những phát hiện đã đưa vào thiết kế

| Phát hiện | Thay đổi trong dev-kit |
|---|---|
| Một skill con đăng ký rồi ẩn bằng `disable-model-invocation` thì controller cũng không gọi được | Skill con để ở `parts/`, không đăng ký |
| Claude Code có sẵn các skill `init`, `code-review`, `security-review` | Controller dùng tên riêng; khởi tạo là `dk:init` |
| Copy về để lại các tham chiếu treo (`executing-plans`, `writing-skills`) | Đã sửa; thêm `scripts/check_parts.py` |
| Một part làm controller dừng giữa chừng | Rule F1 |
| SDD và 4 reviewer không làm code đúng hơn mà tốn nhiều | Rule C1, C2 |
| Một rule trông như thắng 6/6 hóa ra là overfitting | Quy trình bật rule: phải qua ≥ 5 bài mới |

## 6.5 Giới hạn của phép đo

- **Ít lần lặp:** phần lớn tổ hợp chạy 1–3 lần. Chênh 1 bài chưa đủ để kết luận; chỉ dùng các chênh lệch lớn và lặp lại.
- **Model:** chủ yếu Haiku 5.5. Sonnet 5.5 mới thử trên 5 bài SWE và 1 repo thật; Opus chưa thử ❓.
- **Không có người:**
  - Lab chạy headless: mọi câu hỏi và cổng duyệt đều được quyết định tự động.
  - Phần "hỏi đúng câu" của `grilling` và giá trị của cổng duyệt chưa được đo.
- **Việc trong một phiên:** chưa có việc kéo dài nhiều phiên, và chưa thử khôi phục sau khi context bị nén.
- **Repo:** app mẫu, Django, và một repo thật (Node monorepo, chạy trên bản copy).

## 6.6 Lịch sử chi tiết

Báo cáo từng vòng nằm trong lab của dev-kit (private), không được công bố:
- vòng 1: ticket dễ;
- vòng 2: ticket khó;
- vòng 3: SWE-bench;
- v0.3;
- kiểm rule trên bài mới;
- v0.4.
