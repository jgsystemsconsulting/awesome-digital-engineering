# Copyright (c) 2026 JG Systems Consulting Ltd. See LICENSE.
# SPDX-License-Identifier: CC0-1.0
"""Release gate (RR-B-15) for awesome-digital-engineering (Base + OSS list profile)."""
import pathlib
import re
import subprocess
import sys

fails: list[str] = []

REQUIRED = [
    "LICENSE",
    "COPYRIGHT",
    "NOTICE",
    "README.md",
    "CHANGELOG.md",
    "RELEASE-INFO.txt",
    "CITATION.cff",
    "SECURITY.md",
    "CONTRIBUTING.md",
    "CODE_OF_CONDUCT.md",
    ".gitignore",
    "docs/DISTRIBUTION.md",
    ".github/workflows/link-check-pr.yml",
    ".github/workflows/link-check-schedule.yml",
    ".github/workflows/validate.yml",
    ".github/ISSUE_TEMPLATE/bug_report.yml",
    ".github/ISSUE_TEMPLATE/config.yml",
    ".github/ISSUE_TEMPLATE/suggest-resource.yml",
]
for f in REQUIRED:
    if not pathlib.Path(f).is_file():
        fails.append(f"required file missing: {f}")

tracked = subprocess.run(
    ["git", "ls-files"], capture_output=True, text=True, check=True
).stdout.splitlines()
FORBIDDEN_PATH_PARTS = [
    "__pycache__",
    ".venv",
    ".worktrees",
    ".pytest_cache",
    ".ruff_cache",
    ".bak",
]
for f in tracked:
    if any(part in f for part in FORBIDDEN_PATH_PARTS):
        fails.append(f"forbidden tracked path: {f}")

FORBIDDEN_CONTENT = [
    re.compile(r"BEGIN [A-Z ]*PRIVATE KEY"),
    re.compile(r"CONFIDENTIAL\s+[-—]\s+Not for external distribution"),
]
for g in ["*.md", "*.txt", "*.cff", "docs/**/*.md", "scripts/*.py", ".github/**/*.yml"]:
    for path in pathlib.Path(".").glob(g):
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for rx in FORBIDDEN_CONTENT:
            if rx.search(text):
                fails.append(f"forbidden content in {path}: {rx.pattern}")

HEADER_SENTINEL = "Copyright (c) 2026 JG Systems Consulting Ltd"
for path in pathlib.Path("scripts").glob("*.py"):
    head = path.read_text(encoding="utf-8", errors="ignore")[:400]
    if HEADER_SENTINEL not in head:
        fails.append(f"header missing: {path}")
    if "SPDX-License-Identifier" not in head:
        fails.append(f"SPDX missing: {path}")

# Version consistency RELEASE-INFO vs CITATION vs CHANGELOG tag
info = pathlib.Path("RELEASE-INFO.txt").read_text(encoding="utf-8")
m = re.search(r"^Version:\s*(\S+)", info, re.M)
ver = m.group(1) if m else None
if not ver:
    fails.append("RELEASE-INFO.txt missing Version:")
else:
    cff = pathlib.Path("CITATION.cff").read_text(encoding="utf-8")
    if f'version: "{ver}"' not in cff and f"version: {ver}" not in cff:
        fails.append(f"CITATION.cff version does not match RELEASE-INFO {ver}")
    if f"[{ver}]" not in pathlib.Path("CHANGELOG.md").read_text(encoding="utf-8"):
        fails.append(f"CHANGELOG.md missing section [{ver}]")
    if f"Tag: v{ver}" not in info and f"Tag:v{ver}" not in info:
        fails.append("RELEASE-INFO.txt missing Tag: v<version>")

readme = pathlib.Path("README.md").read_text(encoding="utf-8")
# Awesome-list READMEs must keep Contents first and must not ship a Licence H2 (awesome-lint).
# RR-B-05 install/usage/support/licence-enquiry may appear as prose.
rl = readme.lower()
for needle in ("install", "usage", "support", "labs.jgsystemsconsulting.com/licensing.html"):
    if needle not in rl:
        fails.append(f"README missing required prose: {needle}")
if "cc0" not in rl and "license" not in rl and "licence" not in rl:
    fails.append("README missing licence mention")

sec = pathlib.Path("SECURITY.md").read_text(encoding="utf-8")
if "advisories" not in sec and "pull request" not in sec.lower():
    fails.append("SECURITY.md lacks advisory/PR reporting route")

if fails:
    print("RELEASE GATE FAILED:")
    for f in fails:
        print(f"  - {f}")
    sys.exit(1)
print("release gate: PASS")
