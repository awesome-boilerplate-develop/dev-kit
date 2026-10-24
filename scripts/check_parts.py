"""Check for dangling references in a copied pack. Usage: python3 scripts/check_parts.py <plugin path>
- `parts/<x>/SKILL.md` and "dev-kit part `x`" must point to a part that exists.
- Relative Markdown links must exist (with or without a leading ./).
- The paragraphs the controllers share (Commands, Graph, Standards, Outputs) must be identical in every controller."""
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
    for link in re.findall(r"\]\((?![a-z][a-z0-9+.-]*:|/)([^)#\s]+)", text):  # every relative link, with or without ./
        if not (f.parent / link).exists():
            bad.append(f"{f.relative_to(pack)}: broken link {link}")
shared = ("**Commands.**", "**Graph (rule G1).**", "**Standards (rule T1).**", "**Outputs** (rule O1).")
controllers = [f for f in sorted((pack / "skills").glob("*/SKILL.md")) if f.parent.name not in ("init", "brainstorm")]
for start in shared:
    found = {f.parent.name: next((l for l in f.read_text().splitlines() if l.startswith(start)), None) for f in controllers}
    usual = max(set(found.values()), key=list(found.values()).count)
    odd = [n for n, l in found.items() if l != usual]
    if odd:
        bad.append(f"shared paragraph {start} differs from the other controllers in: {', '.join(odd)}")
print("\n".join(bad) or "OK: no dangling references")
sys.exit(1 if bad else 0)
