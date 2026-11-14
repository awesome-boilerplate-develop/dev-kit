"""Tests for check_report.py: reports that must pass and ways a report could slip through.
Usage: python3 scripts/test_check_report.py"""
import pathlib
import subprocess
import sys
import tempfile
import unittest

SCRIPT = pathlib.Path(__file__).resolve().parent / "check_report.py"


def report(certain="", suspect="", verdict="GO", diff="", result="PASS: 12 tests"):
    return f"""## Commands run
| Command | Result |
|---|---|
| make check | {result} |

## Review setup (required)
{diff}
- Depth: one — reason: small diff: 1 file, 3 lines
- Graph: no .code-review-graph/ index
- Standards applied: none

## Review
Verdict: {verdict}

### Certain findings
| Severity | Conf. | file:line | Finding (what, when it happens, impact, fix) | Rule | Status |
|---|---|---|---|---|---|
{certain}

### Suspect findings (do not block)
| Severity | Conf. | file:line | Finding | Rule |
|---|---|---|---|---|
{suspect}
"""


class CheckReport(unittest.TestCase):
    def run_check(self, text, cwd, *args):
        path = pathlib.Path(cwd) / "report.md"
        path.write_text(text, encoding="utf-8")
        return subprocess.run([sys.executable, str(SCRIPT), str(path), *args], cwd=cwd, capture_output=True, text=True, encoding="utf-8")

    def check(self, text, *args):
        with tempfile.TemporaryDirectory() as d:
            return self.run_check(text, d, *args)

    def test_located_fixed_blocker_with_go_passes(self):
        r = self.check(report("| blocker | 90 | src/pay.ts:12 | total is negative when qty is 0 | — | fixed |"))
        self.assertEqual(r.returncode, 0, r.stdout)

    def test_failing_check_needs_no_go(self):
        for result in ("FAIL: compiler error, exit 1", "**FAIL** 1 new failing test", "NOT RUN: restore failed",
                       "thất bại: 1 test mới fail", "Lỗi compile, exit 1", "không chạy được: thiếu SDK",
                       "skipped, suite did not run", "could not run: missing SDK", "0 tests ran", "suite not executed",
                       "that bai: 1 test", "khong chay duoc", "bỏ qua: thiếu môi trường"):
            r = self.check(report(result=result))
            self.assertIn("required check failed or did not run but verdict is GO", r.stdout, result)
            self.assertEqual(self.check(report(verdict="NO-GO", result=result)).returncode, 0, result)
        for result in ("12 passed, 3 failed (2 known failures, 1 new failure)", "PASS: 3 failed, 2 known", "PASS: exit 1"):
            self.assertIn("did not run but verdict is GO", self.check(report(result=result)).stdout, result)
        for result in ("PASS: 40 tests, 2 known baseline failures", "PASS, 0 lỗi", "none: no skips added", "12 passed, 0 failed",
                       "PASS: 40 passed, 2 skipped", "PASS, 2 skipped (marked skip in baseline)",
                       "PASS: 38 passed, 2 failed, 2 known (baseline)", "PASS: exit 1, 2 known baseline failures",
                       "PASS: 342 passed, 12 new tests green"):
            self.assertEqual(self.check(report(result=result)).returncode, 0, result)

    def test_gate_holds_against_layout_tricks(self):
        open_blocker = "| blocker | 90 | src/pay.ts:12 | Severity: total is negative when qty is 0 | — | open |"
        self.assertIn("open certain blocker but verdict is GO", self.check(report(open_blocker)).stdout)
        counted = report("| blocker | 90 | src/pay.ts:12 | total is negative | — | open |").replace(
            "### Certain findings", "### Certain findings (1)")
        self.assertIn("open certain blocker but verdict is GO", self.check(counted).stdout)
        step = report(result="FAIL: build").replace("## Commands run", "## Commands run (step 1)")
        self.assertIn("did not run but verdict is GO", self.check(step).stdout)
        for result in ("12 passed, 3 failed", "exit 1", "PASS: 12 passed, 3 failed", "PASS (exit code 2)"):
            self.assertIn("did not run but verdict is GO", self.check(report(result=result)).stdout, result)
        empty = report().replace("| make check | PASS: 12 tests |\n", "")
        self.assertIn("Commands run lists no check", self.check(empty).stdout)

    def test_verdict_left_as_the_template_fails(self):
        for line in ("GO | NO-GO (from open **certain** blockers and checks that FAIL or did NOT RUN)", "GO or NO-GO"):
            self.assertIn("still has the template's choices", self.check(report(verdict=line)).stdout, line)
        for line in ("**NO-GO**", "GO (no open certain blocker)"):
            self.assertNotIn("template's choices", self.check(report(verdict=line)).stdout, line)

    def test_depth_lowered_for_cost_fails(self):
        for reason in ("one reviewer to save cost", "self — tiết kiệm token", "one: cheaper than four", "self, within budget",
                       "one, rẻ hơn"):
            r = self.check(report().replace("one — reason: small diff: 1 file, 3 lines", reason))
            self.assertIn("justified by cost", r.stdout, reason)

    def test_uncommitted_changes_forbid_go(self):
        tree = report().replace("- Depth:", "- Tree: uncommitted: src/pay.ts\n- Depth:")
        self.assertIn("the checks did not run on HEAD", self.check(tree).stdout)
        self.assertEqual(self.check(tree.replace("Verdict: GO", "Verdict: NO-GO")).returncode, 0)
        with tempfile.TemporaryDirectory() as d:
            subprocess.run(["git", "init", "-q", d], check=True)
            pathlib.Path(d, "pay.ts").write_text("fixed but not committed\n")
            pathlib.Path(d, ".dev-kit").mkdir()
            pathlib.Path(d, ".dev-kit", "notes.md").write_text("kit output\n")
            r = self.run_check(report(), d)
            self.assertIn("uncommitted changes outside .dev-kit/ (pay.ts)", r.stdout)
            pathlib.Path(d, "pay.ts").unlink()
            self.assertEqual(self.run_check(report(), d).returncode, 0, "the report itself and .dev-kit/ do not count")

    def test_fixed_later_keeps_the_blocker_open(self):
        for status in ("fixed (will do)", "fixed later", "fixed — chưa commit"):
            r = self.check(report(f"| blocker | 90 | src/pay.ts:12 | total is negative | — | {status} |"))
            self.assertIn("open certain blocker but verdict is GO", r.stdout, status)
        for status in ("fixed", "fixed (a1b2c3d)"):
            r = self.check(report(f"| blocker | 90 | src/pay.ts:12 | total is negative | — | {status} |"))
            self.assertEqual(r.returncode, 0, status + r.stdout)

    def test_missing_tests_without_rule_is_not_certain(self):
        r = self.check(report("| major | 90 | src/pay.ts:12 | refund path is untested | — | open |"))
        self.assertIn("'missing tests' reported as certain without a rule", r.stdout)

    def test_unknown_standard_file_fails(self):
        r = self.check(report("| major | 90 | src/pay.ts:12 | total is negative | coding/no-such-file | open |"))
        self.assertIn("rule id 'coding/no-such-file' not found", r.stdout)

    def test_graph_line_when_the_repo_has_an_index(self):
        with tempfile.TemporaryDirectory() as d:
            subprocess.run(["git", "init", "-q", d], check=True)
            pathlib.Path(d, ".code-review-graph").mkdir()
            self.assertIn("but the repo has one", self.run_check(report(), d).stdout)
            summary = report().replace("no .code-review-graph/ index", "risk 0.2, 1 test gap")
            self.assertEqual(self.run_check(summary, d).returncode, 0)

    def test_file_without_extension_is_located(self):
        r = self.check(report(suspect="| minor | 60 | Makefile:12 | check target skips lint | — |"))
        self.assertEqual(r.returncode, 0, r.stdout)

    def test_report_without_finding_sections_fails(self):
        r = self.check(report().split("### Certain findings")[0])
        self.assertIn("missing section 'Certain findings'", r.stdout)
        self.assertIn("missing section 'Suspect findings'", r.stdout)

    def test_unknown_item_of_a_real_standard_fails(self):
        r = self.check(report("| major | 90 | src/pay.ts:12 | total is negative | coding/review-basics#C99 | open |"))
        self.assertIn("coding/review-basics has no item C99", r.stdout)

    def test_known_item_of_a_real_standard_passes(self):
        r = self.check(report("| major | 90 | src/pay.ts:12 | error swallowed | coding/review-basics#C1 | open |"))
        self.assertEqual(r.returncode, 0, r.stdout)

    def test_suspect_without_confidence_fails(self):
        r = self.check(report(suspect="| minor | high | src/pay.ts:12 | x | — |"))
        self.assertIn("suspect finding without confidence", r.stdout)

    def test_confidence_above_100_fails(self):
        r = self.check(report("| major | 999 | src/pay.ts:12 | x | — | open |"))
        self.assertIn("confidence 999 > 100", r.stdout)

    def test_finding_without_any_file_fails(self):
        r = self.check(report(suspect="| major | 60 | payment logic | rounding differs | — |"))
        self.assertIn("without a file:line location", r.stdout)

    def test_finding_with_file_but_no_line_fails(self):
        r = self.check(report("| minor | 85 | src/pay.ts | duplicated branch | — | open |"))
        self.assertIn("without a file:line location", r.stdout)

    def test_unfixed_blocker_with_go_fails(self):
        r = self.check(report("| blocker | 90 | src/pay.ts:12 | total is negative | — | unfixed |"))
        self.assertIn("open certain blocker but verdict is GO", r.stdout)

    def test_fixed_in_finding_text_does_not_close_blocker(self):
        r = self.check(report("| blocker | 90 | src/buf.c:7 | fixed-size buffer overflows on long names | — | open |"))
        self.assertIn("open certain blocker but verdict is GO", r.stdout)

    def test_open_blocker_with_no_go_passes(self):
        r = self.check(report("| blocker | 90 | src/pay.ts:12 | total is negative | — | open |", verdict="NO-GO"))
        self.assertEqual(r.returncode, 0, r.stdout)

    def test_row_with_missing_status_cell_fails(self):
        r = self.check(report("| major | 85 | src/pay.ts:12 | total is negative | — |"))
        self.assertIn("row has 5 cells, the template has 6", r.stdout)

    def test_unknown_severity_fails(self):
        r = self.check(report(suspect="| critical | 60 | src/pay.ts:12 | total is negative | — |"))
        self.assertIn("is not blocker / major / minor", r.stdout)

    def test_unknown_status_fails(self):
        r = self.check(report("| major | 85 | src/pay.ts:12 | total is negative | — | done |"))
        self.assertIn("Status is not fixed / open / pushed back", r.stdout)

    def test_route_folders_and_deleted_files_are_in_the_diff(self):
        with tempfile.TemporaryDirectory() as d:
            def git(*a):
                return subprocess.run(["git", "-C", d, "-c", "user.name=t", "-c", "user.email=t@t", *a],
                                      check=True, capture_output=True, text=True, encoding="utf-8").stdout.strip()
            git("init", "-q", "-b", "main")
            route = pathlib.Path(d, "app", "[id]")
            route.mkdir(parents=True)
            (route / "page.tsx").write_text("x\n")
            pathlib.Path(d, "old.ts").write_text("".join(f"line {i}\n" for i in range(1, 21)))
            git("add", ".")
            git("commit", "-qm", "base")
            git("checkout", "-qb", "feature")
            pathlib.Path(d, "old.ts").unlink()
            (route / "page.tsx").write_text("y\n")
            git("commit", "-qam", "drop old.ts, change the route")
            diff = f"- Diff: {git('merge-base', 'main', 'HEAD')[:7]}...{git('rev-parse', 'HEAD')[:7]}"
            for loc in ("app/[id]/page.tsx:1", "(app/[id]/page.tsx:1)", "old.ts:12"):
                r = self.run_check(report(suspect=f"| minor | 60 | {loc} | x | — |", diff=diff), d, "--base", "main")
                self.assertEqual(r.returncode, 0, f"{loc}: {r.stdout}")

    def test_base_checks_cited_line_against_diff(self):
        with tempfile.TemporaryDirectory() as d:
            def git(*a):
                return subprocess.run(["git", "-C", d, "-c", "user.name=t", "-c", "user.email=t@t", *a],
                                      check=True, capture_output=True, text=True, encoding="utf-8").stdout.strip()
            git("init", "-q", "-b", "main")
            src = pathlib.Path(d, "pay.ts")
            src.write_text("".join(f"line {i}\n" for i in range(1, 41)))
            git("add", ".")
            git("commit", "-qm", "base")
            git("checkout", "-qb", "feature")
            src.write_text(src.read_text().replace("line 30\n", "changed\n"))
            git("commit", "-qam", "change")
            diff = f"- Diff: {git('merge-base', 'main', 'HEAD')[:7]}...{git('rev-parse', 'HEAD')[:7]}"
            inside = self.run_check(report(suspect="| minor | 60 | pay.ts:30 | x | — |", diff=diff), d, "--base", "main")
            self.assertEqual(inside.returncode, 0, inside.stdout)
            outside = self.run_check(report(suspect="| minor | 60 | pay.ts:3 | x | — |", diff=diff), d, "--base", "main")
            self.assertIn("outside the changed lines", outside.stdout)
            for sub in ("lib", "app"):
                pathlib.Path(d, sub).mkdir()
                pathlib.Path(d, sub, "util.ts").write_text("x\n")
            git("add", ".")
            git("commit", "-qm", "more")
            diff2 = f"- Diff: {git('merge-base', 'main', 'HEAD')[:7]}...{git('rev-parse', 'HEAD')[:7]}"
            suffix = self.run_check(report(suspect="| minor | 60 | xpay.ts:30 | x | — |", diff=diff2), d, "--base", "main")
            self.assertIn("outside the changed lines", suffix.stdout)  # pay.ts is not a path segment of xpay.ts
            bare = self.run_check(report(suspect="| minor | 60 | util.ts:1 | x | — |", diff=diff2), d, "--base", "main")
            self.assertIn("matches several changed files", bare.stdout)
            full = self.run_check(report(suspect="| minor | 60 | lib/util.ts:1 | x | — |", diff=diff2), d, "--base", "main")
            self.assertEqual(full.returncode, 0, full.stdout)
            git("reset", "-q", "--hard", "HEAD~1")
            no_diff = self.run_check(report(suspect="| minor | 60 | pay.ts:30 | x | — |"), d, "--base", "main")
            self.assertIn("lacks 'Diff:'", no_diff.stdout)
            pathlib.Path(d, ".dev-kit").mkdir()
            pathlib.Path(d, ".dev-kit", "report.md").write_text("report\n")
            git("add", ".dev-kit")
            git("commit", "-qm", "the report itself")
            kit_only = self.run_check(report(suspect="| minor | 60 | pay.ts:30 | x | — |", diff=diff), d, "--base", "main")
            self.assertEqual(kit_only.returncode, 0, kit_only.stdout)
            src.write_text(src.read_text() + "later\n")
            git("commit", "-qam", "after the review")
            stale = self.run_check(report(suspect="| minor | 60 | pay.ts:30 | x | — |", diff=diff), d, "--base", "main")
            self.assertIn("does not match the repo now", stale.stdout)
            git("checkout", "-q", "main")
            git("merge", "-q", "feature")
            merged = self.run_check(report(diff=f"- Diff: {git('rev-parse', 'HEAD')[:7]}...{git('rev-parse', 'HEAD')[:7]}"),
                                    d, "--base", "main")
            self.assertIn("empty diff has no review", merged.stdout)


if __name__ == "__main__":
    unittest.main()
