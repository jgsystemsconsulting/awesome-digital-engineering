# Landing Truth Gate Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Port the sibling repo's landing truth gate into `scripts/check_release.py` so the release gate fails whenever the docs/index.html status chips or section-index links disagree with RELEASE-INFO.txt, README.md, or the curated list itself.

**Architecture:** A straight port of proven code from the gold sample (`C:\Users\gower\OneDrive\Documents\GitHub\awesome-archimate\scripts\check_release.py`) into this repo's flat checker. One guarded reader (`read_source`), one chip extractor (`landing_chip`), one README walker (`curated_walk`), one slugifier (`github_slug`), plus chip, heading, and fragment assertions inserted after the existing version-consistency work. No new files, no new dependencies, no new imports.

**Tech Stack:** Python 3 standard library only (`pathlib`, `re`, `subprocess`, `sys`, all already imported). Run with `python scripts/check_release.py` from the repo root.

**Spec:** `docs/superpowers/specs/2026-09-18-landing-truth-gate.md`

## Global Constraints

- Only `scripts/check_release.py` may change, plus the one `"docs/index.html"` entry in its `REQUIRED` list. The only permitted edit to any other tracked file is correcting chip `<dd>` values in `docs/index.html` when they disagree with computed sources (spec R1, AC1).
- Existing checks keep identical behavior on a valid tree: same failure report format, exit 1 on failure, `release gate: PASS` on success (spec R2).
- `ENTRY_RX` must be exactly `^- \[[^\]]+\]\(https?://[^)\s]+\)\s+-\s+.+\(\d{4}\)\.$` (spec R10).
- `CURATED_SECTIONS` must be exactly these eight titles in this order (spec R9): `Policy and strategy`, `Standards`, `Digital thread and interoperability`, `Model-based definition and PMI`, `Government and consortia programs`, `Open tools and reference implementations`, `Learning and reports`, `Commercial platforms`.
- No new imports; no new scripts, test files, or dependencies (spec Implementation notes, Out of scope).
- Reads of RELEASE-INFO.txt, README.md, and docs/index.html go through the guarded reader. When `html` is None, chip and section-index DOM asserts are skipped and no `landing_chip(None, ...)` call happens (spec R3).
- Task 4 and Task 5 mutations are temporary and uncommitted; each is reverted before the next step. `README.md` and `docs/index.html` are clean tracked files at plan time, so `git checkout -- <file>` restores them.

## Codebase context

Verified by direct inspection and baseline run on 2026-09-18:

- `python scripts/check_release.py` currently prints `release gate: PASS` and exits 0. Nothing about the existing checks changes in this plan except the three read sites converted to the guarded reader (behavior-identical on a valid tree).
- `docs/index.html` carries chips `version` = `0.1.1`, `sweep` = `2026-09`, `entries` = `31`, and exactly one `<ul class="section-index">` with eight `<li>`. The eight href fragments already equal `github_slug` of the eight curated titles: `policy-and-strategy`, `standards`, `digital-thread-and-interoperability`, `model-based-definition-and-pmi`, `government-and-consortia-programs`, `open-tools-and-reference-implementations`, `learning-and-reports`, `commercial-platforms`.
- `RELEASE-INFO.txt` has `Version: 0.1.1`; `README.md` has exactly one sweep badge `![Last full sweep: 2026-09]`.
- Simulating the ported `curated_walk` plus `ENTRY_RX` over `README.md` computes exactly 31 valid bullets, and each of the eight curated headings appears exactly once. The `Commercial platforms` section currently holds 0 link bullets. Consequence: the entries chip needs no data fix, and Task 3 should pass without touching `docs/index.html`.

## Research

research: skipped (internal release-gate; gold sample on disk at ../awesome-archimate/scripts/check_release.py)

Gold sample line references from the spec's Implementation notes: `landing_chip` 64-69, version/sweep chip comparisons 76-98, `CURATED_SECTIONS`/`ENTRY_RX` 100-105, `curated_walk` 108-134, entries chip 142-147, `github_slug` 150-151, heading presence 154-158, section-index checks 160-181.

---

### Task 1: REQUIRED entry, guarded reader, null-safe reads

**Files:**
- Modify: `scripts/check_release.py` (REQUIRED list near lines 11-30; version-consistency reads near lines 71-86; README prose block near lines 86-94)

**Interfaces:**
- Consumes: module-level `fails` list (exists at line 9).
- Produces: `read_source(path: str) -> str | None`, a module-level function that appends `unreadable source file: {path}` to `fails` on `OSError`/`UnicodeDecodeError` and returns None. Task 2 consumes the module variables `info`, `readme`, and `html` set here.

**Model:** flash

- [ ] **Step 1: Add `docs/index.html` to REQUIRED**

In the `REQUIRED` list, add one entry after `"docs/DISTRIBUTION.md",` so the docs group stays together:

```python
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
```

- [ ] **Step 2: Add the guarded reader above the version-consistency block**

Insert directly above the line `# Version consistency RELEASE-INFO vs CITATION vs CHANGELOG tag`:

```python
def read_source(path):
    try:
        return pathlib.Path(path).read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        fails.append(f"unreadable source file: {path}")
        return None
```

- [ ] **Step 3: Convert the RELEASE-INFO read and null-check it**

Replace the version-consistency block (currently starting `info = pathlib.Path("RELEASE-INFO.txt").read_text(encoding="utf-8")` and running through the `Tag: v<version>` check) with this version. The inner checks are byte-identical to the current ones; only the read and its null branch are new:

```python
# Version consistency RELEASE-INFO vs CITATION vs CHANGELOG tag
info = read_source("RELEASE-INFO.txt")
ver = None
if info is None:
    fails.append("RELEASE-INFO.txt missing Version:")
else:
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
```

- [ ] **Step 4: Convert the README read, add the html read, wrap the prose block**

Replace the current line `readme = pathlib.Path("README.md").read_text(encoding="utf-8")` and the prose-needle block that follows it with:

```python
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
```

Leave the SECURITY.md block and everything after it untouched in this task.

- [ ] **Step 5: Run the gate on the valid tree**

Run: `python scripts/check_release.py`
Expected: `release gate: PASS`, exit 0. This is the R2 behavior-preservation check for Task 1.

- [ ] **Step 6: Smoke-test the guarded read (R3)**

```bash
mv docs/index.html docs/index.html.absent
python scripts/check_release.py; echo "exit=$?"
mv docs/index.html.absent docs/index.html
```

Expected: exit 1, report printed, no traceback, and both lines present: `required file missing: docs/index.html` and `unreadable source file: docs/index.html` (the REQUIRED loop catches the absence; `read_source` also reports the failed read, matching gold behavior and spec AC5's "and/or").

- [ ] **Step 7: Verify clean tree and commit**

```bash
git status --porcelain -- README.md docs/index.html scripts/check_release.py
git add scripts/check_release.py
git commit -m "feat(release): guard landing-page source reads, require docs/index.html"
```

Expected: status shows only `scripts/check_release.py` modified.

### Task 2: Port the landing truth gate

**Files:**
- Modify: `scripts/check_release.py` (insert one block between the SECURITY.md check and the final `if fails:` report)

**Interfaces:**
- Consumes: `read_source`, `fails`, `info`, `readme`, `html` from Task 1.
- Produces: the full gate behavior; nothing downstream consumes new names (the block sits last before the report). Internal names used by the block itself: `landing_chip`, `CURATED_SECTIONS`, `ENTRY_RX`, `curated_walk`, `curated_count`, `heading_hits`, `chip_version`, `chip_sweep`, `chip_entries`, `github_slug`, `blocks`, `lis`, `fragments`.

**Model:** standard

- [ ] **Step 1: Insert the landing gate block**

Insert this entire block immediately after the SECURITY.md check (`fails.append("SECURITY.md lacks advisory/PR reporting route")`) and before the final `if fails:` report. Adaptations from the gold sample: the eight `CURATED_SECTIONS` titles are this repo's (spec R9), and gold's `release_info` variable is this repo's `info`. Everything else is ported as-is:

```python
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
```

- [ ] **Step 2: Run the gate on the valid tree**

Run: `python scripts/check_release.py`
Expected: `release gate: PASS`, exit 0. The chips (0.1.1 / 2026-09 / 31), headings, and fragments all verified against sources in the Codebase context section.

- [ ] **Step 3: Diff review for AC4**

Run: `git diff scripts/check_release.py`
Expected: relative to Task 1's commit, the only change is the inserted landing-gate block plus the section comment. No existing check was rewritten or deleted; the three `read_source` conversions from Task 1 remain the only touches to prior logic.

- [ ] **Step 4: Commit**

```bash
git add scripts/check_release.py
git commit -m "feat(release): landing truth gate for chips and section index"
```

### Task 3: Clean-tree acceptance (AC1)

**Files:**
- Possibly modify: `docs/index.html` (chip `<dd>` values only, and only on drift)

**Interfaces:**
- Consumes: the complete gate from Task 2.
- Produces: the AC1 acceptance result.

**Model:** flash

- [ ] **Step 1: Run the gate and check exit code**

Run: `python scripts/check_release.py; echo "exit=$?"`
Expected: stdout exactly `release gate: PASS`, exit 0.

- [ ] **Step 2: Chip drift rule (conditional)**

If and only if Step 1 prints a `landing version chip`, `landing sweep chip`, or `landing entries chip` mismatch: correct the corresponding `<dd>` value in `docs/index.html` to the computed source value shown in the message (version from RELEASE-INFO.txt, sweep from the README badge, entries from the curated count). Change nothing else in the file, then rerun Step 1 until PASS. Baseline data says this branch should not fire: computed entries count is 31 and the chip already reads 31.

- [ ] **Step 3: Commit only if a data fix was applied**

```bash
git status --porcelain docs/index.html
```

If `docs/index.html` is modified, commit it:

```bash
git add docs/index.html
git commit -m "fix(landing): correct chip value to computed source"
```

If clean, nothing to commit; proceed to Task 4.

### Task 4: AC3 negative mutation checks

**Files:**
- Temporarily mutate, then revert: `README.md`, `docs/index.html`. No net change; nothing to commit.

**Interfaces:**
- Consumes: the complete gate from Task 2.
- Produces: AC2/AC3 evidence. Failure-class messages asserted here, exactly as the gate emits them:

| Mutation class | Expected failure message |
|---|---|
| Wrong chip value | `landing version chip 9.9.9 != RELEASE-INFO Version 0.1.1` |
| Wrong fragment | `section-index fragment mismatch: policy-and-strategy-x != policy-and-strategy` |
| Malformed curated bullet | `curated entry malformed in Standards: * [Bad entry](https://example.com) - No year here` |
| Renamed curated heading | `curated heading missing from README: Commercial platforms` |
| Second section-index ul | `landing section-index list missing or ambiguous: 2 found` |

**Model:** flash

Between mutations, `README.md` and `docs/index.html` are clean tracked files, so `git checkout -- <file>` reverts exactly. R2 side-check: every mutation run must show exit 1 with only the listed landing-gate failure(s); any `forbidden`, `header missing`, `README missing required prose`, or `SECURITY.md` line in the report means an existing check broke and the task fails.

- [ ] **Step 1: Mutate the version chip, run, revert**

```bash
python - <<'EOF'
import pathlib
p = pathlib.Path("docs/index.html")
t = p.read_text(encoding="utf-8")
t = t.replace("<dd>0.1.1</dd>", "<dd>9.9.9</dd>", 1)
p.write_text(t, encoding="utf-8")
EOF
python scripts/check_release.py; echo "exit=$?"
git checkout -- docs/index.html
python scripts/check_release.py
```

Expected on the mutated run: exit 1 and `landing version chip 9.9.9 != RELEASE-INFO Version 0.1.1`. After revert: `release gate: PASS`.

- [ ] **Step 2: Mutate one section-index fragment, run, revert**

```bash
python - <<'EOF'
import pathlib
p = pathlib.Path("docs/index.html")
t = p.read_text(encoding="utf-8")
t = t.replace("#policy-and-strategy", "#policy-and-strategy-x", 1)
p.write_text(t, encoding="utf-8")
EOF
python scripts/check_release.py; echo "exit=$?"
git checkout -- docs/index.html
python scripts/check_release.py
```

Expected on the mutated run: exit 1 and `section-index fragment mismatch: policy-and-strategy-x != policy-and-strategy`. After revert: PASS.

- [ ] **Step 3: Add one malformed curated bullet, run, revert**

```bash
python - <<'EOF'
import pathlib
p = pathlib.Path("README.md")
t = p.read_text(encoding="utf-8")
t = t.replace("## Standards\n", "## Standards\n* [Bad entry](https://example.com) - No year here\n", 1)
p.write_text(t, encoding="utf-8")
EOF
python scripts/check_release.py; echo "exit=$?"
git checkout -- README.md
python scripts/check_release.py
```

Expected on the mutated run: exit 1 and `curated entry malformed in Standards: * [Bad entry](https://example.com) - No year here`. The malformed bullet does not increment the count, so no entries-chip co-failure appears. After revert: PASS.

- [ ] **Step 4: Rename one curated heading, run, revert**

```bash
python - <<'EOF'
import pathlib
p = pathlib.Path("README.md")
t = p.read_text(encoding="utf-8")
t = t.replace("## Commercial platforms\n", "## Commercial platforms renamed\n", 1)
p.write_text(t, encoding="utf-8")
EOF
python scripts/check_release.py; echo "exit=$?"
git checkout -- README.md
python scripts/check_release.py
```

Expected on the mutated run: exit 1 and `curated heading missing from README: Commercial platforms`. That section holds 0 link bullets, so the curated count stays 31 and no entries-chip co-failure appears. After revert: PASS.

- [ ] **Step 5: Add a second section-index ul, run, revert**

```bash
python - <<'EOF'
import pathlib
p = pathlib.Path("docs/index.html")
t = p.read_text(encoding="utf-8")
t = t.replace('<ul class="section-index">', '<ul class="section-index"></ul><ul class="section-index">', 1)
p.write_text(t, encoding="utf-8")
EOF
python scripts/check_release.py; echo "exit=$?"
git checkout -- docs/index.html
python scripts/check_release.py
```

Expected on the mutated run: exit 1 and `landing section-index list missing or ambiguous: 2 found`. After revert: PASS.

- [ ] **Step 6: Confirm no residue**

```bash
git status --porcelain README.md docs/index.html
python scripts/check_release.py; echo "exit=$?"
```

Expected: empty status output, PASS, exit 0. Nothing to commit in this task; the mutations were never staged.

Note on spec R14: these mutations touch only gate inputs (chip `<dd>` values, href fragments, README link bullets, curated headings). Visible labels, nav text, and anchor link text are free to change without gate failure; no step asserts on them.

### Task 5: AC5 missing and unreadable index.html

**Files:**
- Temporarily rename or overwrite, then restore: `docs/index.html`. No net change; nothing to commit.

**Interfaces:**
- Consumes: the complete gate from Task 2.
- Produces: AC5 evidence that a missing or unreadable landing page degrades to a clean exit 1, never a traceback.

**Model:** flash

- [ ] **Step 1: Absent file**

```bash
mv docs/index.html docs/index.html.absent
python scripts/check_release.py; echo "exit=$?"
mv docs/index.html.absent docs/index.html
```

Expected: exit 1, report printed, no traceback, both lines present: `required file missing: docs/index.html` and `unreadable source file: docs/index.html`. Chip and section-index messages must be absent (html is None, DOM asserts skipped per R3).

- [ ] **Step 2: Unreadable file (invalid UTF-8)**

```bash
python - <<'EOF'
import pathlib
pathlib.Path("docs/index.html").write_bytes(b"\xff\xfe\x00bad")
EOF
python scripts/check_release.py; echo "exit=$?"
git checkout -- docs/index.html
```

Expected: exit 1, report printed, no traceback, and `unreadable source file: docs/index.html` present (the `UnicodeDecodeError` branch of `read_source`). Chip and section-index messages absent. The forbidden-content scan is unaffected because it reads with `errors="ignore"`.

- [ ] **Step 3: Final clean verification**

```bash
git status --porcelain README.md docs/index.html scripts/check_release.py
python scripts/check_release.py; echo "exit=$?"
```

Expected: status shows no modifications (the tree matches the Task 2 commit), `release gate: PASS`, exit 0.
