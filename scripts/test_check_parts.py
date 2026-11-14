"""Tests for check_parts.py on a small fake pack: dangling part names, broken links and drifted shared paragraphs.
Usage: python3 scripts/test_check_parts.py"""
import pathlib
import subprocess
import sys
import tempfile
import unittest

SCRIPT = pathlib.Path(__file__).resolve().parent / "check_parts.py"
SHARED = "**Commands.** same\n\n**Graph (rule G1).** same\n\n**Standards (rule T1).** same\n\n**Outputs** (rule O1). same\n"


class CheckParts(unittest.TestCase):
    def run_check(self, story="Read part `grilling`.", extra=None, fix_shared=SHARED):
        with tempfile.TemporaryDirectory() as d:
            files = {"parts/grilling/SKILL.md": "# grilling\n", "parts/pr/SKILL.md": "# pr\n",
                     "skills/story-runner/SKILL.md": SHARED + story + "\n", "skills/bug-fixer/SKILL.md": fix_shared,
                     "skills/pre-pr-check/SKILL.md": SHARED}
            files.update(extra or {})
            for rel, text in files.items():
                pathlib.Path(d, rel).parent.mkdir(parents=True, exist_ok=True)
                pathlib.Path(d, rel).write_text(text)
            r = subprocess.run([sys.executable, str(SCRIPT), d], capture_output=True, text=True, encoding="utf-8")
            return r.returncode, r.stdout

    def test_clean_pack_passes(self):
        code, out = self.run_check(story="Read part `grilling`; parts `grilling` and `pr`; [x](../../parts/pr/SKILL.md)")
        self.assertEqual(code, 0, out)

    def test_unknown_part_in_controller_wording_fails(self):
        for story in ("Read part `griling`.", "Use parts `grilling`, `prr` and `pr`.", "dev-kit part `nope`"):
            code, out = self.run_check(story=story)
            self.assertEqual(code, 1, story)
            self.assertIn("part does not exist", out)

    def test_broken_relative_link_fails(self):
        _, out = self.run_check(story="See [notes](./missing.md).")
        self.assertIn("broken link ./missing.md", out)

    def test_drifted_shared_paragraph_fails(self):
        _, out = self.run_check(fix_shared=SHARED.replace("**Graph (rule G1).** same", "**Graph (rule G1).** other"))
        self.assertIn("shared paragraph **Graph (rule G1).** differs", out)
        self.assertIn("bug-fixer", out)

    def test_drifted_harness_paragraph_fails_in_any_skill(self):
        extra = {"skills/init/SKILL.md": "**Harness.** same\n", "skills/ticket/SKILL.md": "**Harness.** other\n",
                 "skills/brainstorm/SKILL.md": "**Harness.** same\n"}
        _, out = self.run_check(extra=extra)
        self.assertIn("shared paragraph **Harness.** differs from the others in: ticket", out)

    def test_no_argument_prints_usage(self):
        r = subprocess.run([sys.executable, str(SCRIPT)], capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(r.returncode, 1)
        self.assertIn("Usage:", r.stderr)

    def test_hidden_folders_are_skipped(self):
        code, out = self.run_check(extra={".outputs/notes.md": "Read part `x`."})
        self.assertEqual(code, 0, out)


if __name__ == "__main__":
    unittest.main()
