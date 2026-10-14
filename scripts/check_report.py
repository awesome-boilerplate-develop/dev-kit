"""Machine-check a pre-pr-check report against rules R1/C2.
Usage: python3 check_report.py <report.md> [--base <branch>]
With --base (run inside a repo): a "certain" finding must point to a file in the diff, and at least one line must be
inside or next to (±5 lines) the changed code; otherwise it may be pre-existing code (R1) → move to suspect or drop.
Run from inside a repo: if the repo has .code-review-graph/, the Graph line must have a detect-changes summary (or
"detect-changes failed: <error>"); it must not say "no .code-review-graph/ index" (rule G1).
A "certain" finding that cites no rule (an id that really exists in the kit/team/project standards, or a specific place in a spec; R1–R7 do not count)
and is about a missing test or only points at a test file: Do not flag (R1) → move to suspect; keep it only if it clearly says the existing test is wrong.
A rule id cited in the certain tier must exist in a standards file (rule T1, R7); an id that is not found FAILs.
Prints each violation; exits 1 if there are violations, 0 if the report passes."""
import os
import pathlib
import re
import subprocess
import sys

args = sys.argv[1:]
base = None
if "--base" in args:
    i = args.index("--base")
    base = args[i + 1]
    del args[i:i + 2]
text = open(args[0], encoding="utf-8").read()
problems = []
root = pathlib.Path(subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip() or ".")


def standard_ids():
    """Ids in the frontmatter of kit standards (dev-kit/standards), project standards (.dev-kit/standards) and team standards (standards.team)."""
    dirs = [pathlib.Path(__file__).resolve().parent.parent / "standards", root / ".dev-kit" / "standards"]
    cfg = root / ".dev-kit" / "config.yml"
    if cfg.is_file():
        m = re.search(r"^\s+team:\s*[\"']?([^\"'#\n]*?)[\"']?\s*(#.*)?$", cfg.read_text(encoding="utf-8"), re.M)
        if m and m.group(1).strip():
            dirs.append(root / os.path.expanduser(m.group(1).strip()))
    ids = set()
    for d in dirs:
        for f in d.rglob("*.md") if d.is_dir() else []:
            m = re.search(r"^id:\s*(\S+)", f.read_text(encoding="utf-8", errors="ignore"), re.M)
            if m:
                ids.add(m.group(1))
    return ids



def section(title):
    m = re.search(rf"^###? {re.escape(title)}\s*\n(.*?)(?=^###? |\Z)", text, re.S | re.M)
    return m.group(1) if m else None


def rows(block):
    out = []
    for line in (block or "").splitlines():
        if line.startswith("|") and not re.match(r"^\|\s*-", line) and "Severity" not in line:
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if any(cells) and cells[0] not in ("—", "-", "none", ""):
                out.append(cells)
    return out


def conf(cells):
    m = re.search(r"\d+", cells[1]) if len(cells) > 1 else None
    return int(m.group()) if m else None


setup = section("Review setup (required)") or section("Review setup")
if not setup:
    problems.append("missing section 'Review setup'")
else:
    for key in ("Depth:", "Graph:", "Standards applied:"):
        if key not in setup:
            problems.append(f"Review setup lacks '{key}'")
    # Reports may be written in the user's language: keep non-English alternatives (Vietnamese) in these patterns.
    if re.search(r"Depth:.*(cost|save|tiết kiệm)", setup, re.I):
        problems.append("review depth justified by cost (rule C2 forbids lowering for cost)")
    graph = re.search(r"Graph:(.*)", setup)
    if graph and (root / ".code-review-graph").is_dir():
        if re.search(r"no\s+`?\.?code-review-graph", graph.group(1), re.I):
            problems.append("Review setup says 'no .code-review-graph/ index' but the repo has one: run detect-changes (rule G1)")
        elif not re.search(r"risk|detect-changes", graph.group(1), re.I):
            problems.append("Graph line lacks the detect-changes summary although .code-review-graph/ exists (rule G1)")

certain = rows(section("Certain findings"))
suspect = rows(section("Suspect findings (do not block)") or section("Suspect findings"))
test_gap = re.compile(r"\b(untested|no tests?|missing tests?|not tested|test coverage|thiếu test|chưa có test)\b", re.I)
test_file = re.compile(r"[._](spec|test)s?\.\w+$|(^|/)(tests?|__tests__|spec)/|(^|/)test_[^/]+\.py$")
broken_test = re.compile(r"\bpass(es|ed)?\s+(vacuously|even|regardless|always|when|without)|\bstill pass|\bvacuous|always (passes|green)"
                         r"|never fails|never asserts?|(does not|doesn't|do not) assert|asserts? nothing|accepts any", re.I)
LOC = r"([\w./@-]+\.[A-Za-z]{1,5})(?::(\d+))?"
known_ids = standard_ids()

for c in certain:
    v = conf(c)
    if v is None:
        problems.append(f"certain finding without confidence: {c[2] if len(c) > 2 else c}")
    elif v < 80:
        problems.append(f"certain finding with confidence {v} < 80 (move to suspect): {c[2]}")
    # "Has a rule" = a real standards id (T1) other than finding-quality, or a specific place in a spec; R1–R7 are conditions for raising a finding.
    rule = c[4] if len(c) > 4 else ""
    tokens = [t.strip("`'\"") for t in re.split(r"[\s,;()]+", rule)]
    cited = [m.group(1) for t in tokens if (m := re.fullmatch(r"([\w-]+/[\w-]+)(?:#[\w-]+)?", t))]
    for x in cited:
        if x not in known_ids:
            problems.append(f"rule id '{x}' not found in kit/team/project standards (rules T1, R7): {c[2]}")
    valid = [x for x in cited if x in known_ids and x != "review/finding-quality"]
    no_rule = not valid and not re.search(r"specs?/|\bspec\b.*(§|#|\d)", rule, re.I)
    files = [f for f, _ in re.findall(LOC, c[2] if len(c) > 2 else "")]
    if no_rule and test_gap.search(" ".join(c)):
        problems.append(f"'missing tests' reported as certain without a rule (Do not flag): {c[2]}")
    elif no_rule and files and all(test_file.search(f) for f in files) and not broken_test.search(" ".join(c[3:4])):
        problems.append("certain finding only on test files without a rule: missing coverage is Do not flag (move to suspect); "
                        f"a wrong test must say how it passes while the code is broken: {c[2]}")
for c in suspect:
    v = conf(c)
    if v is not None and v < 50:
        problems.append(f"suspect finding with confidence {v} < 50 (drop it): {c[2]}")
    if v is not None and v >= 80:
        problems.append(f"suspect finding with confidence {v} ≥ 80 (move to certain): {c[2]}")

if base:
    diff = subprocess.run(["git", "diff", "-U0", f"{base}...HEAD"], capture_output=True, text=True).stdout
    changed = {}  # file -> list of (start, end) on the new side
    current = None
    for line in diff.splitlines():
        if line.startswith("+++ "):
            current = line[6:] if line.startswith("+++ b/") else None
            if current:
                changed.setdefault(current, [])
        m = re.match(r"^@@ -\S+ \+(\d+)(?:,(\d+))? @@", line)
        if m and current:
            start, count = int(m.group(1)), int(m.group(2) or 1)
            changed[current].append((start, start + max(count, 1) - 1))
    for c in certain:
        loc = c[2] if len(c) > 2 else ""
        refs = re.findall(LOC, loc)
        if not refs:
            continue
        ok = False
        for f, ln in refs:
            files = [k for k in changed if k == f or k.endswith("/" + f) or f.endswith(k)]
            for k in files:
                if not ln:
                    ok = True
                elif any(a - 5 <= int(ln) <= b + 5 for a, b in changed[k]):
                    ok = True
        if not ok:
            problems.append(f"certain finding points outside the changed lines (pre-existing code? rule R1): {loc}")

blockers = [c for c in certain if c and c[0].lower().startswith("blocker") and "fixed" not in " ".join(c).lower()]
verdict = re.search(r"Verdict:\s*\**\s*(NO-GO|GO)", text)
if not verdict:
    problems.append("missing 'Verdict: GO | NO-GO'")
elif blockers and verdict.group(1) != "NO-GO":
    problems.append("open certain blocker but verdict is GO")
elif not blockers and verdict.group(1) == "NO-GO":
    problems.append("verdict NO-GO without an open certain blocker")

for p in problems:
    print("FAIL:", p)
print("OK" if not problems else f"{len(problems)} problem(s)")
sys.exit(1 if problems else 0)
