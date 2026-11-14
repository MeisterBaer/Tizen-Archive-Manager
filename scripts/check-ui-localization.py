#!/usr/bin/env python3
"""Heuristic guard against hardcoded user-facing Compose text.

Dynamic package/device values and protocol tokens are data, not UI copy.
This check deliberately targets literal arguments to common Compose text
components and accessibility properties; it is not a Kotlin parser.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "app" / "src" / "main" / "kotlin"

PATTERNS = (
    re.compile(r'\\b(?:Text|BasicText)\\s*\\(\\s*(?:text\\s*=\\s*)?"((?:\\\\.|[^"\\\\])*)"', re.DOTALL),
    re.compile(r'\\b(?:contentDescription|stateDescription|label|placeholder)\\s*=\\s*"((?:\\\\.|[^"\\\\])*)"', re.DOTALL),
)
PURE_INTERPOLATION = re.compile(r'^(?:\\$\\{[^}]+\\}|\\$[A-Za-z_]\\w*)+$')
DATA_LITERALS = {".tpk", ".wgt", "TPK", "WGT", "SDB", "APK"}


def violations_in(source: str, path: str = "sample.kt") -> list[str]:
    found: list[str] = []
    for pattern in PATTERNS:
        for match in pattern.finditer(source):
            literal = match.group(1)
            if not literal or literal in DATA_LITERALS or PURE_INTERPOLATION.fullmatch(literal):
                continue
            line = source.count("\\n", 0, match.start()) + 1
            found.append(f"{path}:{line}: hardcoded UI text {literal!r}; use stringResource()")
    return found


def self_test() -> bool:
    sample = '''
        Text("Ready")
        Text(text = "Setup needed")
        Modifier.semantics { contentDescription = "Open setup" }
        Text(packageName)
        Text("$packageName")
        Text("TPK")
    '''
    found = violations_in(sample)
    return len(found) == 3 and all("stringResource()" in item for item in found)


def main() -> int:
    if "--self-test" in sys.argv:
        if self_test():
            print("localization checker self-test passed")
            return 0
        print("localization checker self-test failed", file=sys.stderr)
        return 1

    violations: list[str] = []
    for path in sorted(SOURCE.rglob("*.kt")):
        if path.is_file():
            violations.extend(violations_in(path.read_text(encoding="utf-8"), str(path.relative_to(ROOT))))
    if violations:
        print("\\n".join(violations), file=sys.stderr)
        return 1
    print("No hardcoded Compose text literals found.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
