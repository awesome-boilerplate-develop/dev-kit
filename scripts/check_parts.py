"""Check for dangling references in a copied pack. Usage: python3 scripts/check_parts.py <plugin path>
- `parts/<x>/SKILL.md` and "dev-kit part `x`" must point to a part that exists.
- Relative Markdown links inside parts must exist."""
import pathlib
import re
import sys

pack = pathlib.Path(sys.argv[1])
parts = {p.name for p in (pack / "parts").iterdir() if p.is_dir()}
bad = []
for f in pack.rglob("*.md"):
    text = re.sub(r"```.*?```", "", f.read_text(), flags=re.S)  # ignore examples inside code fences
    for name in set(re.findall(r"parts/([a-z-]+)/SKILL\.md", text)) | set(re.findall(r"dev-kit part `([a-z-]+)`", text)):
        if name not in parts:
            bad.append(f"{f.relative_to(pack)}: part does not exist `{name}`")
    for link in re.findall(r"\]\((\.{1,2}/[^)#\s]+)", text):
        if not (f.parent / link).exists():
            bad.append(f"{f.relative_to(pack)}: broken link {link}")
print("\n".join(bad) or "OK: no dangling references")
sys.exit(1 if bad else 0)
