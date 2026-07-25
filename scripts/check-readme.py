"""Check README.md for repo-relative links that would render broken on PyPI."""

import re
import sys

from pathlib import Path

README = Path(__file__).parent.parent / "README.md"

ALLOWED = ("http://", "https://", "mailto:", "#")


def main():
    contents = README.read_text()
    problems = []
    for match in re.finditer(r"!?\[[^]]*\]\(([^)\s]+)[^)]*\)", contents):
        url = match.group(1)
        if not url.startswith(ALLOWED):
            line = contents.count("\n", 0, match.start()) + 1
            problems.append(f"{README.name}:{line}: {match.group(0)}")
    if problems:
        print("README.md contains repo-relative links that will not render on PyPI.")
        print("Use absolute URLs instead:")
        for problem in problems:
            print(" ", problem)
        return 1
    print("README.md links OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
