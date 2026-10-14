<!-- i18n: source=docs/en/06-evidence.md source_commit=v1.0.0 review=human -->
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
| Cursor | – | – | – | chưa chạy được: cần `cursor-agent login` |
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
