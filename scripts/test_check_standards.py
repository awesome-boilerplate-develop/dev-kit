"""Tests for check_standards.py: a valid file passes, and each way a standards file can be wrong is caught.
Usage: python3 scripts/test_check_standards.py"""
import pathlib
import subprocess
import sys
import tempfile
import unittest

SCRIPT = pathlib.Path(__file__).resolve().parent / "check_standards.py"


def standard(id="coding/errors", topic="coding", applies='"**/*.py"', body=None):
    body = body if body is not None else """## Implement
- C1 Catch only the errors you handle. Why: a broad catch hides bugs.
- C2 Log with the request id. Why: logs must be traceable.

## Review
- C1–C2 on the diff → major
- V1 When the diff adds a retry loop, check it has a limit → major
"""
    return f"---\nid: {id}\ntopic: {topic}\nscope: project\nstatus: experimental\napplies_to: [{applies}]\n---\n\n{body}"


class CheckStandards(unittest.TestCase):
    def run_check(self, files, *args, cwd=None):
        with tempfile.TemporaryDirectory() as d:
            for rel, text in files.items():
                p = pathlib.Path(d, "standards", rel)
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_text(text, encoding="utf-8")
            r = subprocess.run([sys.executable, str(SCRIPT), str(pathlib.Path(d, "standards")), *args],
                               capture_output=True, text=True, cwd=cwd or d)
            return r.returncode, r.stdout

    def test_valid_file_with_range_and_review_only_check_passes(self):
        code, out = self.run_check({"coding/errors.md": standard()}, "--no-files")
        self.assertEqual(code, 0, out)

    def test_id_must_match_the_path(self):
        _, out = self.run_check({"coding/errors.md": standard(id="coding/other")}, "--no-files")
        self.assertIn("must be 'coding/errors'", out)

    def test_topic_must_match_the_folder(self):
        _, out = self.run_check({"coding/errors.md": standard(topic="testing")}, "--no-files")
        self.assertIn("must match its folder 'coding'", out)

    def test_review_naming_an_undefined_id_fails(self):
        body = "## Implement\n- C1 Catch only what you handle. Why: x.\n\n## Review\n- C1, C9 on the diff → major\n"
        _, out = self.run_check({"coding/errors.md": standard(body=body)}, "--no-files")
        self.assertIn("Review names C9", out)

    def test_range_expands_and_catches_a_gap(self):
        body = "## Implement\n- C1 One. Why: x.\n- C3 Three. Why: x.\n\n## Review\n- C1–C3 on the diff → major\n"
        _, out = self.run_check({"coding/errors.md": standard(body=body)}, "--no-files")
        self.assertIn("Review names C2", out)

    def test_item_without_id_and_wrong_letter_fail(self):
        body = "## Implement\n- Catch only what you handle.\n- T1 Wrong letter. Why: x.\n"
        _, out = self.run_check({"coding/errors.md": standard(body=body)}, "--no-files")
        self.assertIn("item without an ID", out)
        self.assertIn("ID T1 must be 'C'", out)

    def test_applies_to_must_match_a_tracked_file(self):
        with tempfile.TemporaryDirectory() as repo:
            subprocess.run(["git", "init", "-q", repo], check=True)
            pathlib.Path(repo, "app.py").write_text("x = 1\n")
            subprocess.run(["git", "-C", repo, "add", "app.py"], check=True)
            code, out = self.run_check({"coding/errors.md": standard()}, cwd=repo)
            self.assertEqual(code, 0, out)
            _, out = self.run_check({"coding/errors.md": standard(applies='"**/*.ts"')}, cwd=repo)
            self.assertIn("'**/*.ts' matches no tracked file", out)


if __name__ == "__main__":
    unittest.main()
