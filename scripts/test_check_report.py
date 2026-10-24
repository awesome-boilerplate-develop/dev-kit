"""Tests for check_report.py: reports that must pass and ways a report could slip through.
Usage: python3 scripts/test_check_report.py"""
import pathlib
import subprocess
import sys
import tempfile
import unittest

SCRIPT = pathlib.Path(__file__).resolve().parent / "check_report.py"


def report(certain="", suspect="", verdict="GO", diff=""):
    return f"""## Commands run
| Command | Result |
|---|---|
| make check | pass |

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
        return subprocess.run([sys.executable, str(SCRIPT), str(path), *args], cwd=cwd, capture_output=True, text=True)

    def check(self, text, *args):
        with tempfile.TemporaryDirectory() as d:
            return self.run_check(text, d, *args)

    def test_located_fixed_blocker_with_go_passes(self):
        r = self.check(report("| blocker | 90 | src/pay.ts:12 | total is negative when qty is 0 | — | fixed |"))
        self.assertEqual(r.returncode, 0, r.stdout)

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

    def test_base_checks_cited_line_against_diff(self):
        with tempfile.TemporaryDirectory() as d:
            git = lambda *a: subprocess.run(["git", "-C", d, "-c", "user.name=t", "-c", "user.email=t@t", *a],
                                            check=True, capture_output=True, text=True).stdout.strip()
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


if __name__ == "__main__":
    unittest.main()
