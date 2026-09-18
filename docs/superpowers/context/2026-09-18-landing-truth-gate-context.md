# P1 landing-truth-gate context (2026-09-18)

Spec author input for awesome-digital-engineering.

## Findings

- `scripts/check_release.py` is Base + OSS list only. No `docs/index.html` in REQUIRED. No chip, section-index, or curated-count asserts.
- Path S landing is live: chips `version=0.1.1`, `sweep=2026-09`, `entries=31`; eight section-index anchors match README H2 slugs. CI can stay green while Pages desyncs.
- Gold pattern lives in `../awesome-archimate/scripts/check_release.py` landing truth gate (~L54-182). Port helpers; swap section titles; freeze chip dt names.
- `.github/workflows/validate.yml` already runs `python scripts/check_release.py` on push/PR. No workflow change for P1.
- Out of scope: `docs/DISTRIBUTION.md`, lychee, visitor copy/chrome, action SHA pins (P2/P4/P5 or already clean).

## Current `scripts/check_release.py`

Path: `scripts/check_release.py` (105 lines). Checks today:

1. REQUIRED files (no landing HTML): LICENSE, COPYRIGHT, NOTICE, README.md, CHANGELOG.md, RELEASE-INFO.txt, CITATION.cff, SECURITY.md, CONTRIBUTING.md, CODE_OF_CONDUCT.md, .gitignore, docs/DISTRIBUTION.md, three workflows, three issue templates.
2. Forbidden tracked path parts: `__pycache__`, `.venv`, `.worktrees`, `.pytest_cache`, `.ruff_cache`, `.bak`.
3. Forbidden content (md/txt/cff/docs md/scripts py/github yml): private key blocks; confidential external-distribution marker.
4. Every `scripts/*.py` header: copyright sentinel + SPDX.
5. Version consistency: RELEASE-INFO `Version:` matches CITATION.cff, CHANGELOG `[ver]`, and `Tag: v<ver>`.
6. README prose needles: install, usage, support, labs licensing URL; licence/cc0 mention.
7. SECURITY.md: advisory or PR reporting route.

Exit: print fails + `sys.exit(1)`, else `release gate: PASS`.

## Gold sample (copy approach)

Sibling: `C:\Users\gower\OneDrive\Documents\GitHub\awesome-archimate\scripts\check_release.py` L54-182.

| Piece | Role |
|---|---|
| `read_source(path)` | UTF-8 read; fail + None on OS/decode error |
| `landing_chip(html, name)` | exactly one `<dt>{name}</dt>\s*<dd>([^<]*)</dd>` |
| `curated_walk(readme)` | fence-aware; exact `## {title}` hits; count grammar-valid bullets under curated H2s |
| `github_slug(title)` | lower; strip non-word except space/hyphen; spaces to `-` |
| `CURATED_SECTIONS` | ordered 8-title tuple |
| `ENTRY_RX` | `^- \[[^\]]+\]\(https?://[^)\s]+\)\s+-\s+.+\(\d{4}\)\.$` |

Gold asserts: unique RELEASE-INFO `Version:` vs chip `version`; unique README sweep badge vs chip `sweep`; chip `entries` integer equals curated count; each curated heading once; one `<ul class="section-index">` with 8 `li`, each one `#fragment`, fragments == slug(title) in order; malformed bullets fail. Gold also adds `docs/index.html` to REQUIRED and scans html in content globs.

## This repo curated titles (8, freeze order)

1. Policy and strategy -> `policy-and-strategy`
2. Standards -> `standards`
3. Digital thread and interoperability -> `digital-thread-and-interoperability`
4. Model-based definition and PMI -> `model-based-definition-and-pmi`
5. Government and consortia programs -> `government-and-consortia-programs`
6. Open tools and reference implementations -> `open-tools-and-reference-implementations`
7. Learning and reports -> `learning-and-reports`
8. Commercial platforms -> `commercial-platforms`

## Entry grammar and count

Under those H2s, lines matching `ENTRY_RX` (`-` or `*` marker, markdown link, ` - ` description, trailing `(YYYY).`). Live count **31**. Commercial platforms has no entries yet; still 31 from the other seven. Do not hardcode 31; derive from README and compare to chip.

## Sweep badge

Exactly one README hit expected:

`![Last full sweep: YYYY-MM](...)` with capture `(\d{4}-\d{2})`. Current: `2026-09`.

## RELEASE-INFO Version

```
Product: awesome-digital-engineering
Version: 0.1.1
Built: 2026-09-17T15:30:00Z
Tag: v0.1.1
```

Version chip source of truth: `Version:` (`0.1.1`). Keep existing Tag/CITATION/CHANGELOG Base checks.

## Landing freeze points (`docs/index.html`)

Chip dt names (freeze): `version`, `sweep`, `entries`. Current dd: `0.1.1`, `2026-09`, `31`.

```html
<dl class="chips">
  <div class="chip"><dt>version</dt><dd>0.1.1</dd></div>
  <div class="chip"><dt>sweep</dt><dd>2026-09</dd></div>
  <div class="chip"><dt>entries</dt><dd>31</dd></div>
</dl>
```

Section index: single `ul` class **`section-index`** (freeze class), eight `li` href fragments matching slugs above.

## CI and scope

- CI already gates via validate.yml `python scripts/check_release.py`. P1 surface: `scripts/check_release.py` (+ short maintainer write-path note if package requires).
- In scope: add `docs/index.html` to REQUIRED; chip asserts vs RELEASE-INFO / sweep badge / curated count; section-index fragments vs eight headings; document single write path.
- Out of scope: DISTRIBUTION.md (P2), lychee (P4), visitor copy, pins (P5), Labs products.yml, entry content edits.
