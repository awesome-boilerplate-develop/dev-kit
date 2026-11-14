"""Tests for check_i18n.py on a fake repo: header, code blocks, links, and stale translations (WARN, FAIL with --strict).
Usage: python3 scripts/test_check_i18n.py"""
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile
import unittest

SCRIPT = pathlib.Path(__file__).resolve().parent / "check_i18n.py"
SOURCE = "# Guide\n\n```bash\nmake check\n```\n\nSee [setup](guide.md).\n"


class CheckI18n(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.root = pathlib.Path(self.dir.name)
        (self.root / "scripts").mkdir()
        shutil.copy(SCRIPT, self.root / "scripts")  # the script finds the repo from its own path
        for rel, text in {"README.md": "# Kit\n", "README.vi.md": self.header("README.md") + "# Kit\n",
                          "docs/en/guide.md": SOURCE}.items():
            (self.root / rel).parent.mkdir(parents=True, exist_ok=True)
            (self.root / rel).write_text(text, encoding="utf-8")
        (self.root / "docs" / "i18n.json").write_text(json.dumps(
            {"source": "en", "readme": {"vi": "README.vi.md"}, "docs": {"vi": ["guide.md"]}}))
        self.git("init", "-q")
        self.git("add", ".")
        self.git("commit", "-qm", "base")
        self.git("tag", "v1")

    def tearDown(self):
        self.dir.cleanup()

    def git(self, *args):
        subprocess.run(["git", "-C", str(self.root), "-c", "user.name=t", "-c", "user.email=t@t", *args],
                       check=True, capture_output=True)

    @staticmethod
    def header(source, commit="v1"):
        return f"<!-- i18n: source={source} source_commit={commit} review=machine -->\n"

    def translate(self, text):
        (self.root / "docs" / "vi").mkdir(parents=True, exist_ok=True)
        (self.root / "docs" / "vi" / "guide.md").write_text(text, encoding="utf-8")

    def run_check(self, *args):
        r = subprocess.run([sys.executable, str(self.root / "scripts" / "check_i18n.py"), *args], capture_output=True, text=True, encoding="utf-8")
        return r.returncode, r.stdout

    def test_faithful_translation_passes(self):
        self.translate(self.header("docs/en/guide.md") + SOURCE.replace("# Guide", "# Hướng dẫn"))
        code, out = self.run_check()
        self.assertEqual(code, 0, out)

    def test_wrong_header_fails(self):
        self.translate("# Hướng dẫn\n" + SOURCE)
        self.assertIn("first line must be the i18n header", self.run_check()[1])
        self.translate(self.header("docs/en/other.md") + SOURCE)
        self.assertIn("expected docs/en/guide.md", self.run_check()[1])

    def test_changed_code_block_fails(self):
        self.translate(self.header("docs/en/guide.md") + SOURCE.replace("make check", "make test"))
        self.assertIn("code blocks differ", self.run_check()[1])

    def test_broken_link_fails(self):
        self.translate(self.header("docs/en/guide.md") + SOURCE.replace("(guide.md)", "(missing.md)"))
        self.assertIn("broken link missing.md", self.run_check()[1])

    def test_stale_is_a_warning_and_fails_with_strict(self):
        self.translate(self.header("docs/en/guide.md") + SOURCE)
        (self.root / "docs" / "en" / "guide.md").write_text(SOURCE + "\nMore.\n", encoding="utf-8")
        self.git("commit", "-qam", "source changed")
        code, out = self.run_check()
        self.assertEqual(code, 0, out)
        self.assertIn("WARN: docs/vi/guide.md: STALE", out)
        code, out = self.run_check("--strict")
        self.assertEqual(code, 1, out)


if __name__ == "__main__":
    unittest.main()
