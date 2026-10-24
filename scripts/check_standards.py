"""Machine-check standards files (templates/standard.md format) after dk:init writes them.
Usage: python3 check_standards.py [<dir or file> ...] [--no-files]
Default target: .dev-kit/standards under the repo root (missing or empty: OK, only kit standards kept). Run from inside the repo: each applies_to glob must match at
least one tracked file (skip with --no-files, for the kit's own standards).
Checks: frontmatter keys; topic is one of the template's topics (plus review) and equals its folder; id == <topic>/<file name>; scope and status values; only the
sections Design, Implement, Review, Do not flag, Severity, each at most once; every Design/Implement item starts with
an ID: the topic's letter and a number (A1 architecture, C coding, T testing, S security, U ui, P api, D data, O ops,
R process or review); a Review line that defines its own item uses V (review-only check) or the topic's letter; IDs unique in the file; a Review line that starts with IDs
("A1, A3 on the diff", "C1–C5 → major") only names IDs defined in the file; a Review line with one ID and its own text
("V1 When the diff touches …") defines that ID.
Prints each problem; exits 1 if there are problems, 0 if all files pass."""
import pathlib
import re
import subprocess
import sys

SECTIONS = ["Design", "Implement", "Review", "Do not flag", "Severity"]
LETTER = {"architecture": "A", "coding": "C", "testing": "T", "security": "S", "ui": "U", "api": "P", "data": "D",
          "ops": "O", "process": "R", "review": "R"}
TOPICS = list(LETTER)
ID = r"[A-Z]{1,3}\d+"
ID_LIST = re.compile(rf"^- ((?:{ID})(?:\s*[–-]\s*{ID})?(?:\s*(?:,|and)\s*(?:{ID})(?:\s*[–-]\s*{ID})?)*)\b(.*)$")

args = sys.argv[1:]
check_files = "--no-files" not in args
targets = [a for a in args if a != "--no-files"]
root = pathlib.Path(subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip() or ".")
if not targets:
    targets = [str(root / ".dev-kit" / "standards")]
    if not list(pathlib.Path(targets[0]).rglob("*.md")):  # dk:init kept only kit files: no repo standards to check
        print("OK: no repo standards files (kit standards only)")
        sys.exit(0)
tracked = subprocess.run(["git", "ls-files"], capture_output=True, text=True, cwd=root).stdout.splitlines() if check_files else []


def glob_re(g):
    """Gitignore-like glob to regex: ** spans folders, * and ? stay inside one folder."""
    out, i = "", 0
    while i < len(g):
        if g.startswith("**/", i):
            out, i = out + "(?:.*/)?", i + 3
        elif g.startswith("**", i):
            out, i = out + ".*", i + 2
        elif g[i] == "*":
            out, i = out + "[^/]*", i + 1
        elif g[i] == "?":
            out, i = out + "[^/]", i + 1
        else:
            out, i = out + re.escape(g[i]), i + 1
    return re.compile(out + "$")


def expand(token):
    """'C1–C5' -> C1..C5; 'A1' -> A1."""
    m = re.fullmatch(rf"({ID})\s*[–-]\s*({ID})", token.strip())
    if not m:
        return [token.strip()]
    (p1, n1), (p2, n2) = re.fullmatch(r"([A-Z]+)(\d+)", m.group(1)).groups(), re.fullmatch(r"([A-Z]+)(\d+)", m.group(2)).groups()
    if p1 != p2 or int(n2) < int(n1):
        return [m.group(1), m.group(2)]
    return [f"{p1}{n}" for n in range(int(n1), int(n2) + 1)]


def check(path, problems):
    text = path.read_text(encoding="utf-8")
    rel = path.as_posix()
    fm = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not fm:
        problems.append(f"{rel}: missing frontmatter between --- lines")
        return
    meta = dict(re.findall(r"^(\w+):\s*(.*?)\s*$", fm.group(1), re.M))
    for key in ("id", "topic", "scope", "status", "applies_to"):
        if key not in meta:
            problems.append(f"{rel}: frontmatter lacks '{key}'")
    expect_id = f"{path.parent.name}/{path.stem}"
    if meta.get("id") and meta["id"] != expect_id:
        problems.append(f"{rel}: id '{meta['id']}' must be '{expect_id}' (folder/file name)")
    if meta.get("topic") and meta["topic"] not in TOPICS:
        problems.append(f"{rel}: topic '{meta['topic']}' is not one of {', '.join(TOPICS)}")
    if meta.get("topic") and meta["topic"] != path.parent.name:
        problems.append(f"{rel}: topic '{meta['topic']}' must match its folder '{path.parent.name}'")
    if meta.get("scope") and meta["scope"] not in ("kit", "team", "project"):
        problems.append(f"{rel}: scope '{meta['scope']}' must be kit, team or project")
    if meta.get("status") and meta["status"] not in ("experimental", "validated"):
        problems.append(f"{rel}: status '{meta['status']}' must be experimental or validated")
    globs = re.findall(r"[\"']([^\"']+)[\"']", meta.get("applies_to", ""))
    if "applies_to" in meta and not globs:
        problems.append(f"{rel}: applies_to has no quoted glob")
    if check_files:
        for g in globs:
            if not any(glob_re(g).match(f) for f in tracked):
                problems.append(f"{rel}: applies_to glob '{g}' matches no tracked file")

    body = text[fm.end():]
    heads = re.findall(r"^## (.+?)\s*$", body, re.M)
    for h in heads:
        if h not in SECTIONS:
            problems.append(f"{rel}: unknown section '## {h}' (allowed: {', '.join(SECTIONS)})")
    for h in set(heads):
        if heads.count(h) > 1:
            problems.append(f"{rel}: section '## {h}' appears {heads.count(h)} times")
    if not any(h in heads for h in ("Design", "Implement", "Review", "Do not flag")):
        problems.append(f"{rel}: no Design, Implement, Review or Do not flag section")

    parts = re.split(r"^## (.+?)\s*$", body, flags=re.M)
    sections = {}
    for name, content in zip(parts[1::2], parts[2::2]):
        sections.setdefault(name, []).extend(l for l in content.splitlines() if l.startswith("- "))
    defined, refs = [], []
    for name in ("Design", "Implement"):
        for line in sections.get(name, []):
            m = re.match(rf"^- ({ID}) ", line)
            if m:
                defined.append(m.group(1))
            else:
                problems.append(f"{rel}: {name} item without an ID (like 'A1 When …'): {line[:70]}")
    for line in sections.get("Review", []):
        m = ID_LIST.match(line)
        if not m:
            continue
        ids = [x for t in re.split(r"\s*(?:,|and)\s*", m.group(1)) for x in expand(t)]
        rest = m.group(2)
        if len(ids) == 1 and re.match(r"\s+When\b", rest):
            defined.append(ids[0])  # a review-only check: "V1 When the diff touches X, check Y → major"
        elif re.search(r"on the diff\b|→|->", rest):
            refs.extend(ids)  # a severity line: "C1–C5 on the diff → major", "T1 missing on a bug fix → major"
        elif len(ids) == 1:
            defined.append(ids[0])  # a review item: "R1 It is introduced by this change"
        else:
            refs.extend(ids)
    letter = LETTER.get(meta.get("topic", ""))
    if letter:
        for name in ("Design", "Implement"):
            for line in sections.get(name, []):
                m = re.match(rf"^- ({ID}) ", line)
                if m and not re.fullmatch(rf"{letter}\d+", m.group(1)):
                    problems.append(f"{rel}: {name} ID {m.group(1)} must be '{letter}' and a number (topic {meta['topic']})")
        for x in defined:
            if x not in [i for n in ("Design", "Implement") for i in re.findall(rf"^- ({ID}) ", "\n".join(sections.get(n, [])), re.M)] \
                    and not re.fullmatch(rf"(V|{letter})\d+", x):
                problems.append(f"{rel}: Review ID {x} must be 'V' (review-only check) or '{letter}' and a number")
    for x in set(defined):
        if defined.count(x) > 1:
            problems.append(f"{rel}: ID {x} is defined {defined.count(x)} times")
    for x in refs:
        if x not in defined:
            problems.append(f"{rel}: Review names {x}, which no item in this file defines")


problems = []
files = []
for t in targets:
    p = pathlib.Path(t)
    if p.is_dir():
        files += sorted(p.rglob("*.md"))
    elif p.is_file():
        files.append(p)
    else:
        problems.append(f"{t}: not found")
if not files:
    problems.append(f"no standards files under {', '.join(targets)}")
for f in files:
    check(f, problems)
for p in problems:
    print("FAIL:", p)
print("OK" if not problems else f"{len(problems)} problem(s)")
sys.exit(1 if problems else 0)
