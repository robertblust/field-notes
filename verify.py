#!/usr/bin/env python3
"""Check that every relative link in every note resolves to a file that exists.

The one failure this repo can have that looks like success: the README lists the notes,
each note is a separate file, and a rename or a typo leaves a link that renders perfectly
and 404s when clicked. Nothing about the page says so, and the person who finds out is a
stranger who came for the answer.

Only relative links are checked. External URLs are deliberately not fetched: a link checker
that hits the network fails on someone else's outage, and a suite that cries wolf is a
suite people stop reading.

    python3 verify.py
"""
import pathlib, re, sys, urllib.parse

ROOT = pathlib.Path(__file__).resolve().parent
LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)")

def main():
    problems, checked = [], 0
    for md in sorted(ROOT.rglob("*.md")):
        if ".github" in md.parts:
            continue
        for target in LINK.findall(md.read_text()):
            if re.match(r"^[a-z][a-z0-9+.-]*:", target) or target.startswith("#"):
                continue                       # external scheme, or an in-page anchor
            path, _, anchor = target.partition("#")
            if not path:
                continue
            checked += 1
            resolved = (md.parent / urllib.parse.unquote(path)).resolve()
            if not resolved.exists():
                problems.append(f"  {md.relative_to(ROOT)} -> {target}")
    if problems:
        print(f"✗ {len(problems)} broken link(s):")
        print("\n".join(problems))
        return 1
    print(f"✓ {checked} relative link(s) resolve")
    return 0

if __name__ == "__main__":
    sys.exit(main())
