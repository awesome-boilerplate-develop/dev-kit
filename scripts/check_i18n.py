"""Check translated docs against their English source (docs/i18n.json).
Usage: python3 scripts/check_i18n.py [--strict]

Each translation must start with
  <!-- i18n: source=<path> source_commit=<sha> review=machine|human -->
and is checked for:
  - missing files (per docs/i18n.json);
  - a valid header pointing at the right source and an existing commit;
  - fenced code blocks identical to the source (same blocks, same order);
  - relative links that resolve.
A translation whose source changed after source_commit is reported as STALE
(a warning; an error with --strict). Exit 1 on any error."""
import json
import pathlib
import re
import subprocess
import sys

root = pathlib.Path(__file__).resolve().parent.parent
config = json.loads((root / "docs" / "i18n.json").read_text(encoding="utf-8"))
strict = "--strict" in sys.argv[1:]
errors, warnings = [], []
HEADER = re.compile(r"^<!-- i18n: source=(\S+) source_commit=(\S+) review=(machine|human) -->$")
FENCE = re.compile(r"^(```|~~~)[^\n]*\n.*?^\1[ \t]*$", re.S | re.M)
LINK = re.compile(r"\]\(([^)\s]+)\)")


def git(*args):
    return subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True)


def pairs():
    for lang, path in config["readme"].items():
        yield lang, pathlib.Path(path), pathlib.Path("README.md")
    for lang, files in config["docs"].items():
        for name in files:
            yield lang, pathlib.Path("docs", lang, name), pathlib.Path("docs", config["source"], name)


def check_links(path, text):
    for target in LINK.findall(FENCE.sub("", text)):
        if re.match(r"^[a-z][a-z0-9+.-]*:", target) or target.startswith("#"):
            continue
        target = target.split("#", 1)[0]
        if target and not (root / path.parent / target).exists():
            errors.append(f"{path}: broken link {target}")


for lang, path, source in pairs():
    if not (root / source).exists():
        errors.append(f"{path}: source {source} does not exist")
        continue
    if not (root / path).exists():
        errors.append(f"{path}: missing ({lang})")
        continue
    text = (root / path).read_text(encoding="utf-8")
    header = HEADER.match(text.splitlines()[0] if text else "")
    if not header:
        errors.append(f"{path}: first line must be the i18n header comment")
    else:
        declared, commit, _review = header.groups()
        if declared != source.as_posix():
            errors.append(f"{path}: header source={declared}, expected {source.as_posix()}")
        if git("cat-file", "-e", f"{commit}^{{commit}}").returncode != 0:
            errors.append(f"{path}: source_commit {commit} is not a commit")
        elif git("diff", "--quiet", commit, "--", source.as_posix()).returncode != 0:
            (errors if strict else warnings).append(f"{path}: STALE, {source} changed since {commit}")
    src_blocks = [m.group(0) for m in FENCE.finditer((root / source).read_text(encoding="utf-8"))]
    own_blocks = [m.group(0) for m in FENCE.finditer(text)]
    if own_blocks != src_blocks:
        errors.append(f"{path}: code blocks differ from {source} ({len(own_blocks)} vs {len(src_blocks)} blocks)")
    check_links(path, text)

for w in warnings:
    print("WARN:", w)
for e in errors:
    print("FAIL:", e)
print("OK" if not errors else f"{len(errors)} error(s)")
sys.exit(1 if errors else 0)
