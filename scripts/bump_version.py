"""Sync the version across the manifests listed in .version-bump.json (the Superpowers way).
Usage: python3 scripts/bump_version.py <x.y.z>   # write the new version into every manifest
       python3 scripts/bump_version.py --check   # exit 1 if the manifests disagree on version"""
import json
import pathlib
import sys

root = pathlib.Path(__file__).resolve().parent.parent
entries = json.loads((root / ".version-bump.json").read_text(encoding="utf-8"))["files"]


def get(path, field):
    node = json.loads((root / path).read_text(encoding="utf-8"))
    for key in field.split("."):
        node = node[int(key)] if isinstance(node, list) else node[key]
    return node


def put(path, field, value):
    data = json.loads((root / path).read_text(encoding="utf-8"))
    *parents, last = field.split(".")
    node = data
    for key in parents:
        node = node[int(key)] if isinstance(node, list) else node[key]
    node[int(last) if isinstance(node, list) else last] = value
    (root / path).write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


if len(sys.argv) != 2:
    sys.exit(__doc__)
if sys.argv[1] == "--check":
    found = {e["path"]: get(e["path"], e["field"]) for e in entries}
    for path, value in found.items():
        print(f"{value}  {path}")
    sys.exit(0 if len(set(found.values())) == 1 else 1)
for e in entries:
    put(e["path"], e["field"], sys.argv[1])
    print(f"{sys.argv[1]}  {e['path']}")
