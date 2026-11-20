#!/usr/bin/env python3
"""
Claude Code PostToolUse hook: whenever Claude writes or edits a file whose name
contains "workpaper" and ends in .json, run the skill's validator on it.

- Validation errors  -> exit code 2; stderr is shown to Claude so it fixes them.
- Warnings / success -> exit code 0 (Claude Code shows the output in transcript mode).
- Anything else (other files, validator not found) -> silently exit 0.

Wired up in .claude/settings.json. Reads the hook event JSON from stdin.
"""
import json
import os
import subprocess
import sys


def find_validator():
    candidates = []
    proj = os.environ.get("CLAUDE_PROJECT_DIR")
    if proj:
        candidates.append(os.path.join(proj, ".claude", "skills", "tax-audit-workpaper", "scripts", "validate_workpaper.py"))
    candidates.append(os.path.join(os.path.expanduser("~"), ".claude", "skills", "tax-audit-workpaper", "scripts", "validate_workpaper.py"))
    here = os.path.dirname(os.path.abspath(__file__))
    candidates.append(os.path.join(here, "..", "skills", "tax-audit-workpaper", "scripts", "validate_workpaper.py"))
    return next((c for c in candidates if os.path.isfile(c)), None)


def main():
    try:
        event = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0
    path = (event.get("tool_input") or {}).get("file_path") or ""
    name = os.path.basename(path).lower()
    if not (name.endswith(".json") and "workpaper" in name and os.path.isfile(path)):
        return 0
    validator = find_validator()
    if not validator:
        return 0
    res = subprocess.run([sys.executable, validator, path], capture_output=True, text=True)
    if res.returncode == 1:
        sys.stderr.write("Workpaper validation failed — fix these before rendering:\n" + res.stdout + res.stderr)
        return 2
    sys.stdout.write(res.stdout)
    return 0


if __name__ == "__main__":
    sys.exit(main())
