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
    "docs/index.html",
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


def read_source(path):
    try:
        return pathlib.Path(path).read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        fails.append(f"unreadable source file: {path}")
        return None


# Version consistency RELEASE-INFO vs CITATION vs CHANGELOG tag
info = read_source("RELEASE-INFO.txt")
ver = None
if info is not None:
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

readme = read_source("README.md")
html = read_source("docs/index.html")
# Awesome-list READMEs must keep Contents first and must not ship a Licence H2 (awesome-lint).
# RR-B-05 install/usage/support/licence-enquiry may appear as prose.
if readme is not None:
    rl = readme.lower()
    for needle in ("install", "usage", "support", "labs.jgsystemsconsulting.com/licensing.html"):
        if needle not in rl:
            fails.append(f"README missing required prose: {needle}")
    if "cc0" not in rl and "license" not in rl and "licence" not in rl:
        fails.append("README missing licence mention")

sec = pathlib.Path("SECURITY.md").read_text(encoding="utf-8")
if "advisories" not in sec and "pull request" not in sec.lower():
    fails.append("SECURITY.md lacks advisory/PR reporting route")

# --- landing truth gate: chips and section index vs sources ---


def landing_chip(html, name):
    hits = re.findall(rf"<dt>{re.escape(name)}</dt>\s*<dd>([^<]*)</dd>", html)
    if len(hits) != 1:
        fails.append(f"landing chip missing or ambiguous: {name}")
        return None
    return hits[0].strip()


if info is not None:
    version_hits = re.findall(r"(?m)^Version: (\S+)\s*$", info)
    if len(version_hits) != 1:
        fails.append(
            f"RELEASE-INFO Version field missing or ambiguous: {len(version_hits)} matches"
        )
    else:
        chip_version = landing_chip(html, "version") if html is not None else None
        if chip_version is not None and chip_version != version_hits[0]:
            fails.append(
                f"landing version chip {chip_version} != RELEASE-INFO Version {version_hits[0]}"
            )

if readme is not None:
    sweep_hits = re.findall(r"!\[Last full sweep: (\d{4}-\d{2})\]", readme)
    if len(sweep_hits) != 1:
        fails.append(f"README sweep badge missing or ambiguous: {len(sweep_hits)} matches")
    else:
        chip_sweep = landing_chip(html, "sweep") if html is not None else None
        if chip_sweep is not None and chip_sweep != sweep_hits[0]:
            fails.append(
                f"landing sweep chip {chip_sweep} != README sweep badge {sweep_hits[0]}"
            )

CURATED_SECTIONS = (
    "Policy and strategy",
    "Standards",
    "Digital thread and interoperability",
    "Model-based definition and PMI",
    "Government and consortia programs",
    "Open tools and reference implementations",
    "Learning and reports",
    "Commercial platforms",
)
ENTRY_RX = re.compile(r"^- \[[^\]]+\]\(https?://[^)\s]+\)\s+-\s+.+\(\d{4}\)\.$")


def curated_walk(readme):
    """Count grammar-valid bullets under curated headings and tally exact ## hits."""
    count = 0
    heading_hits = {title: 0 for title in CURATED_SECTIONS}
    current = None
    in_fence = False
    for raw in readme.splitlines():
        line = raw.strip()
        if line.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        stripped = line.strip()
        if stripped.startswith("## ") and not stripped.startswith("###"):
            current = stripped[3:].strip()
            if stripped == "## " + current and current in heading_hits:
                heading_hits[current] += 1
            continue
        if current in heading_hits and line and re.match(r"^[-*] \[", line):
            probe = "- " + line[2:] if line.startswith("* ") else line
            if ENTRY_RX.match(probe):
                count += 1
            else:
                fails.append(f"curated entry malformed in {current}: {line[:60]}")
    return count, heading_hits


curated_count = None
heading_hits = {}
if readme is not None:
    curated_count, heading_hits = curated_walk(readme)

chip_entries = landing_chip(html, "entries") if html is not None else None
if chip_entries is not None:
    if not re.fullmatch(r"[0-9]+", chip_entries):
        fails.append(f"landing entries chip not an integer: {chip_entries}")
    elif curated_count is not None and int(chip_entries) != curated_count:
        fails.append(f"landing entries chip {chip_entries} != curated count {curated_count}")


def github_slug(title):
    return re.sub(r"[^\w\s-]", "", title.lower()).strip().replace(" ", "-")


for title, hits in heading_hits.items():
    if hits == 0:
        fails.append(f"curated heading missing from README: {title}")
    elif hits > 1:
        fails.append(f"curated heading duplicated in README ({hits}x): {title}")

if html is not None:
    blocks = re.findall(r'<ul class="section-index">(.*?)</ul>', html, re.DOTALL)
    if len(blocks) != 1:
        fails.append(f"landing section-index list missing or ambiguous: {len(blocks)} found")
    else:
        lis = re.findall(r"<li\b[^>]*>.*?</li>", blocks[0], re.DOTALL)
        if len(lis) != 8:
            fails.append(f"section-index li count {len(lis)} != 8")
        else:
            fragments = []
            for li in lis:
                hrefs = re.findall(r'href="[^"#]*#([^"]+)"', li)
                if len(hrefs) != 1:
                    fails.append(f"section-index li href missing or ambiguous: {li[:60]}")
                    fragments = None
                    break
                fragments.append(hrefs[0])
            if fragments is not None:
                expected = [github_slug(t) for t in CURATED_SECTIONS]
                for got, want in zip(fragments, expected):
                    if got != want:
                        fails.append(f"section-index fragment mismatch: {got} != {want}")

if fails:
    print("RELEASE GATE FAILED:")
    for f in fails:
        print(f"  - {f}")
    sys.exit(1)
print("release gate: PASS")
