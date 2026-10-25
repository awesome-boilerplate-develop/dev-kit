"""Check for dangling references in a copied pack. Usage: python3 scripts/check_parts.py <plugin path>
- `parts/<x>/SKILL.md`, "part `x`" and "parts `a`, `b` and `c`" must point to a part that exists.
- Relative Markdown links must exist (with or without a leading ./).
- The paragraphs the controllers share (Commands, Graph, Standards, Outputs) must be identical in every controller.
- Warning only: the Rules row of docs/en/03-skills.md names every rule id in a controller's Rules paragraph."""
import pathlib
import re
import sys

pack = pathlib.Path(sys.argv[1])
parts = {p.name for p in (pack / "parts").iterdir() if p.is_dir()}
bad = []
for f in pack.rglob("*.md"):
    if any(d.startswith(".") for d in f.relative_to(pack).parts[:-1]):
        continue  # local notes (.outputs/, .docs/) are not part of the pack
    text = re.sub(r"```.*?```", "", f.read_text(), flags=re.S)  # ignore examples inside code fences
    # parts/x/SKILL.md, "dev-kit part `x`", and the controllers' "part `x`" / "parts `a`, `b` and `c`"
    named = {n for group in re.findall(r"\bparts? ((?:`[a-z-]+`(?:,\s*|\s+and\s+|\s+or\s+)?)+)", text)
             for n in re.findall(r"`([a-z-]+)`", group)}
    for name in set(re.findall(r"parts/([a-z-]+)/SKILL\.md", text)) | named:
        if name not in parts:
            bad.append(f"{f.relative_to(pack)}: part does not exist `{name}`")
    for link in re.findall(r"\]\((?![a-z][a-z0-9+.-]*:|/)([^)#\s]+)", text):  # every relative link, with or without ./
        if not (f.parent / link).exists():
            bad.append(f"{f.relative_to(pack)}: broken link {link}")
shared = ("**Commands.**", "**Graph (rule G1).**", "**Standards (rule T1).**", "**Outputs** (rule O1).")
controllers = [f for f in sorted((pack / "skills").glob("*/SKILL.md")) if f.parent.name not in ("init", "brainstorm", "ticket")]
for start in shared:
    found = {f.parent.name: next((ln for ln in f.read_text().splitlines() if ln.startswith(start)), None) for f in controllers}
    usual = max(set(found.values()), key=list(found.values()).count)
    odd = [n for n, ln in found.items() if ln != usual]
    if odd:
        bad.append(f"shared paragraph {start} differs from the other controllers in: {', '.join(odd)}")
# Warning only: docs/en/03-skills.md's Rules row should name every rule id the controllers apply.
doc = pack / "docs" / "en" / "03-skills.md"
row = next((ln for ln in doc.read_text().splitlines() if ln.startswith("| **Rules**")), "") if doc.exists() else None
for f in controllers if row is not None else []:
    rules = next((ln for ln in f.read_text().splitlines() if ln.startswith("**Rules.**")), "")
    for rid in sorted(set(re.findall(r"\b([A-Z]\d)\b", rules)) - set(re.findall(r"\b([A-Z]\d)\b", row))):
        print(f"WARN: docs/en/03-skills.md Rules row lacks {rid}, which {f.parent.name} applies")
print("\n".join(bad) or "OK: no dangling references")
sys.exit(1 if bad else 0)
