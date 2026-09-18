# Spec: Landing Truth Gate (awesome-digital-engineering)

Date: 2026-09-18
Status: ready for planning
Owner: release tooling (scripts/check_release.py)

## Goal

The release gate must prove that the landing page (docs/index.html) tells the truth about the repository. Three status chips and eight section links are gate inputs: the version chip must equal RELEASE-INFO.txt, the sweep chip must equal the README badge, the entries chip must equal the count of grammar-valid curated entries, and every section-index fragment must be the GitHub slug of a curated README heading. The gate fails with a specific message for each mismatch.

## Background

The sibling repo awesome-archimate ships a "landing truth gate" inside its release checker. It treats the landing page not as decoration but as a set of claims, and it verifies each claim against the source of truth (RELEASE-INFO.txt, README.md, the curated list itself). awesome-digital-engineering already has a landing page with the same markup shape (`<dt>`/`<dd>` chips, one `ul.section-index` list) but nothing checks it. Drift is currently invisible: someone can bump the version, resweep the list, or rename a README heading and the landing page silently lies.

This work ports the proven gate from the gold sample into this repo's checker. No new scripts, no new dependencies, no new files beyond the one REQUIRED-list addition.

## Codebase context

Verified against the working tree on 2026-09-18:

- `scripts/check_release.py` currently performs: REQUIRED file existence, forbidden tracked paths, forbidden content regexes, copyright/SPDX header sentinel over `scripts/*.py`, version consistency (RELEASE-INFO Version vs CITATION.cff vs CHANGELOG tag vs Tag: line), README prose needles (install/usage/support/licensing URL), licence mention, and a SECURITY.md reporting-route check. It collects failures in `fails` and exits 1 with a report, else prints `release gate: PASS`.
- `docs/index.html` exists and already contains the exact chip markup (`<dt>version</dt><dd>0.1.1</dd>`, `<dt>sweep</dt><dd>2026-09</dd>`, `<dt>entries</dt><dd>31</dd>`) and a single `<ul class="section-index">` with eight `<li>`, each holding one anchor whose href ends in a README fragment.
- `README.md` has one sweep badge, format `![Last full sweep: 2026-09]` (YYYY-MM), and exactly the eight curated `##` headings listed under Requirements.
- `RELEASE-INFO.txt` carries `Version: 0.1.1`.
- The dispatch-announced context document was not present when this spec was written; the facts above come from direct inspection.

## Requirements

Normative. MUST language is binding on the implementation.

### Scope of change

- R1. The implementation MUST extend `scripts/check_release.py` only, plus add one `"docs/index.html"` entry to its `REQUIRED` list. It MUST NOT create new files, new test fixtures, or edit any other tracked file, except the AC1 data fix: correcting `docs/index.html` chip `<dd>` values when they disagree with computed sources.
- R2. Existing checks MUST be preserved unchanged in behavior on a valid tree: REQUIRED existence, forbidden paths, forbidden content, header/SPDX sentinel, version consistency, README prose needles, licence mention, SECURITY.md route, the failure report format, exit code 1 on failure, and the `release gate: PASS` line on success. Refactoring existing RELEASE-INFO/README reads onto a guarded reader is allowed when behavior on the valid tree stays identical.
- R3. A missing or unreadable `docs/index.html` MUST NOT crash the script with a traceback before the failure report prints. The read MUST be guarded (try/except OSError/UnicodeDecodeError; append `unreadable source file: docs/index.html` or rely on REQUIRED missing). When `html` is None, the checker MUST skip chip and section-index DOM parse (no `landing_chip(None, ...)` call) and still report through the normal `fails` path.

### Chip assertions

- R4. A helper `landing_chip(html, name)` MUST be ported from the gold sample. It MUST find the `<dd>` text following `<dt>{name}</dt>` (regex `<dt>{escaped name}</dt>\s*<dd>([^<]*)</dd>`), require exactly one match (else fail with `landing chip missing or ambiguous: {name}`), and return the stripped `<dd>` text.
- R5. The version chip MUST equal the RELEASE-INFO.txt version. The checker MUST first require exactly one `(?m)^Version: (\S+)\s*$` match in RELEASE-INFO.txt (else fail `RELEASE-INFO Version field missing or ambiguous`), then compare the `version` chip against it and fail with both values on mismatch.
- R6. The sweep chip MUST equal the README sweep badge. Exactly one `!\[Last full sweep: (\d{4}-\d{2})\]` match is required (else fail with the match count), then compare the `sweep` chip against the captured YYYY-MM.
- R7. The entries chip MUST be a plain non-negative integer (`re.fullmatch(r"[0-9]+", ...)`; else fail) and MUST equal the curated entry count from R8.

### Curated walk

- R8. A function `curated_walk(readme)` MUST be ported from the gold sample. It MUST:
  - iterate README lines; on a line whose stripped form starts with triple backticks, toggle a fence flag and continue; while fenced, skip the line;
  - on every non-fenced `## ` heading (not `###`), set `current` to the heading title text after `## `; only when that title is in CURATED_SECTIONS, increment that title's hit tally. Non-curated `##` headings still reset `current`, so later bullets are not counted under a previous curated section;
  - while `current` is a curated title, inspect only lines that match `^[-*] \[` after strip (link bullets). Normalize a leading `* ` to `- `, then require ENTRY_RX match; on match increment count; on miss fail with `curated entry malformed in {section}: {line preview}`;
  - plain bullets and non-link lines under curated sections are ignored (gold behavior);
  - return the count and the per-title hit tally.
- R9. `CURATED_SECTIONS` MUST be exactly this tuple, in this order:
  1. `Policy and strategy`
  2. `Standards`
  3. `Digital thread and interoperability`
  4. `Model-based definition and PMI`
  5. `Government and consortia programs`
  6. `Open tools and reference implementations`
  7. `Learning and reports`
  8. `Commercial platforms`
- R10. `ENTRY_RX` MUST be exactly `^- \[[^\]]+\]\(https?://[^)\s]+\)\s+-\s+.+\(\d{4}\)\.$` (identical to the archimate gate).
- R11. Each curated title MUST appear in README exactly once: zero hits fails with `curated heading missing from README: {title}`; more than one fails with the duplicate message and count.

### Section-index assertions

- R12. A helper `github_slug(title)` MUST be ported verbatim: lowercase; `re.sub(r"[^\w\s-]", "", ...)`; strip; replace ASCII space `" "` with `"-"` only (not other whitespace).
- R13. The checker MUST extract section-index blocks with a DOTALL non-greedy regex on `<ul class="section-index">...</ul>` (exactly one match, else fail with the count found). Inside that block it MUST find exactly eight `<li>...</li>` (else fail with the count), and exactly one fragment-bearing href per `<li>` (regex `href="[^"#]*#([^"]+)"`; else fail with a li preview). Each captured fragment MUST equal `github_slug(title)` for the corresponding curated title, compared in CURATED_SECTIONS order. Fail fragment mismatches with a greppable `got != want` form.

### Gate inputs

- R14. Gate inputs (must match sources): dt names `version`, `sweep`, `entries`; the `<dd>` values of those chips; section-index href fragments; curated titles; ENTRY_RX. Free to change without gate failure: visible heading labels (h1/h2 text), nav labels, anchor link text inside section-index, and other prose.

## Acceptance criteria

- AC1. `python scripts/check_release.py` on the clean tree exits 0 and prints `release gate: PASS`. The entries chip value must equal whatever the gate computes from the README; if the current chip (31) disagrees with the computed count, the `<dd>` value in docs/index.html is corrected to the computed count (a data fix, not a gate weakening). Same rule applies to version and sweep chips if they ever drift.
- AC2. Each mismatch class produces a specific, greppable failure message: wrong or missing/ambiguous chip value, non-integer entries chip, malformed curated bullet (with section name and line preview), missing or duplicated curated heading, missing/ambiguous/duplicated section-index block or li, wrong fragment (message shows `got != want`).
- AC3. Negative checks, done with temporary uncommitted mutations and reverted immediately: change one chip value (exit 1, chip message); change one fragment (exit 1, mismatch message); malform one curated link bullet (exit 1, malformed message); rename one curated `##` heading (exit 1, missing-heading message); add a second section-index `<ul>` (exit 1, ambiguous message). Each must include the named failure class. Pre-existing R2 checks (forbidden paths/content, headers, SECURITY, README prose needles) MUST still pass. Mutations that change curated count (malformed bullet, heading rename) MAY also fail the entries-chip comparison; that co-failure is expected and does not fail AC3.
- AC4. Diff review confirms R2 behavior on the valid tree: the only intentional product change is the REQUIRED entry plus the ported gate (guarded-reader refactor of existing reads allowed per R2).
- AC5. `python scripts/check_release.py` still exits 1 (no traceback) when docs/index.html is temporarily absent or unreadable. Expected messages include `required file missing: docs/index.html` and/or `unreadable source file: docs/index.html`. Chip and section-index DOM asserts are skipped when html is None (R3); do not require chip-specific messages in that case.

## Out of scope

- Visitor-facing copy or design of docs/index.html (chip display text, section label text).
- lychee link checking, GitHub Action pinning, the Labs catalogue, DISTRIBUTION.md.
- Any README content change (the gate reads README; it never edits it).
- Path N or any other roadmap path.
- New test files, new dependencies, new scripts.

## Implementation notes

Gold sample: `C:\Users\gower\OneDrive\Documents\GitHub\awesome-archimate\scripts\check_release.py`. Port these pieces, adapted to this repo's flat script (it has no `read_source`/`scanned` machinery):

- `landing_chip(html, name)`: gold lines 64-69. Port as-is.
- `CURATED_SECTIONS` and `ENTRY_RX`: gold lines 100-105. Keep ENTRY_RX verbatim; replace the eight titles with the tuple in R9.
- `curated_walk(readme)`: gold lines 108-134, including the `* ` normalization, fence toggle, and malformed-bullet failure. Port as-is.
- Chip comparisons: gold lines 76-98 (version, sweep) and 142-147 (entries). Port as-is.
- Heading presence checks: gold lines 154-158. Port as-is.
- `github_slug(title)`: gold lines 150-151. Port verbatim.
- Section-index checks: gold lines 160-181. Port as-is.

Integration points in this repo's `scripts/check_release.py`:

- Add `"docs/index.html"` to `REQUIRED`.
- Add a small guarded reader in the gold style (try/except OSError/UnicodeDecodeError, append `unreadable source file: {path}`, return None). This repo currently reads files directly; the plain read after a REQUIRED failure would traceback before the report, which R3 forbids. Use the guarded reader for RELEASE-INFO.txt, README.md, and docs/index.html, then null-check like the gold sample does.
- Insert the landing gate after the existing version-consistency block and before the final `if fails:` report. The existing `readme` variable and `ver` logic stay; the ported version-chip comparison reuses the single-match Version extraction from the gold sample (slightly stricter than the current inline `re.search`, which stays for CITATION/CHANGELOG/Tag checks).
- No new imports: `pathlib` and `re` are already imported.

Ponytail note: this is a straight port of a proven gate, not a framework. No config object, no plugin points, no CLI flags. If a future landing page changes shape, the gate changes with it; nothing here anticipates that.

## Research

research: skipped (internal release-gate assertions; sibling gold sample on disk)
