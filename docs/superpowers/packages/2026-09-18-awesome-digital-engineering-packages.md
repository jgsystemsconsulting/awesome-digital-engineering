---
date: 2026-09-18
project: awesome-digital-engineering
mode: light
rounds: 1
input_digest: 2aaed0a2fed1ce1b257b5748bad7db5aafcd1da602342789573b9881d3c4d32a
open_objections: []
---

# Work packages: awesome-digital-engineering (2026-09-18, light mode, round 1)

First package-loop run. Trigger state: public seed v0.1.1 plus Path S DESIGN and
docs/index.html ported from awesome-archimate gold (2026-09-18). Lens wave found
5 candidates per lens; merge unions left 5 packages; triage graded all 5 PASS with
zero critical defects. Dependency order for drain: P1, P2, P3, P4, P5 (user default
order; visitor-copy killed as already clean). P5 is independent and can run any time.

landing-visitor-copy is not a package: taste and three lenses confirmed visitor labels
(Top/Status), shared Open full list CTA, short family pointer, favicon, woff2 preload,
and 44px targets already meet the outcome bar.

## P1: landing-truth-gate

| Field | Value |
|---|---|
| id | P1 |
| name | landing-truth-gate |
| size | S |
| deps | none |
| status | done |
| promoted_ids | [] |
| corroboration | 3 (value, risk, cohesion) |
| first_prompt | `/superpowers-process full landing truth gate` |

**Problem.** Path S landing `docs/index.html` is live with version/sweep/entries chips
and an eight-anchor section-index, but `scripts/check_release.py` neither requires the
landing file nor asserts chip values, section-index fragments, or curated entry count
against README/RELEASE-INFO. Without that gate, release bumps and heading renames
desync Pages while CI stays green.

**Evidence.**

- scripts/check_release.py:L11-30, REQUIRED list without `docs/index.html`
- docs/index.html chips: version 0.1.1, sweep 2026-09, entries 31
- docs/index.html section-index: eight README fragment links
- RELEASE-INFO.txt Version 0.1.1; README sweep badge 2026-09; curated entry count 31

**In scope.** Add `docs/index.html` to REQUIRED; assert landing chips match
RELEASE-INFO version, README sweep badge, and curated entry count; assert
section-index href fragments match the eight curated README heading anchors;
document the single write path so maintainers know chips and anchors are gated.

**Out of scope.** Visitor-copy or chrome restyle; lychee args; action SHA pins;
Labs products.yml; sindresorhus PR; DISTRIBUTION.md Pages row (P2 owns ledger).

**Why now.** First drain lock. Every entry add and release can desync Pages
silently until the gate lands.

**Triage notes.** PASS. Non-critical: Pages DISTRIBUTION row moved exclusively to P2
so two packages do not touch the ledger.

## P2: org-catalogue-entry

| Field | Value |
|---|---|
| id | P2 |
| name | org-catalogue-entry |
| size | M |
| deps | P1 |
| status | done |
| promoted_ids | [] |
| corroboration | 3 (value, risk, cohesion) |
| first_prompt | `/superpowers-process full org catalogue entry` |

**Problem.** `docs/DISTRIBUTION.md` marks the org catalogue as planned and has no
GitHub Pages row for the Path S landing. Labs `data/products.yml` lists
awesome-archimate but not awesome-digital-engineering, so family discovery stays
capped after Pages ships.

**Evidence.**

- docs/DISTRIBUTION.md org catalogue row status planned (2026-09-17)
- jgsystemsconsulting-website data/products.yml: awesome-archimate present, this list absent
- docs/index.html canonical Pages URL already set

**In scope.** Add awesome-digital-engineering to Labs products.yml (name, url, page,
blurb matching sibling shape) and regenerate docs/index.html on that site; update
DISTRIBUTION.md with GitHub Pages submitted row and org catalogue status flip;
refresh last-reviewed date/version.

**Out of scope.** sindresorhus/awesome PR; landing HTML redesign; CI pins; assessment
write-up body (P3).

**Why now.** Next named growth channel after the landing router is trustworthy (P1).

**Triage notes.** PASS. Sole owner of DISTRIBUTION.md edits in this cut.

## P3: awesome-acceptability-assessment

| Field | Value |
|---|---|
| id | P3 |
| name | awesome-acceptability-assessment |
| size | S |
| deps | P1 |
| status | done |
| promoted_ids | [] |
| corroboration | 3 (value, risk, cohesion) |
| first_prompt | `/superpowers-process full awesome acceptability assessment` |

**Problem.** sindresorhus/awesome is deferred solely because the acceptability gate
is unassessed. Without a concrete go/no-go on membership bar, naming, and
prerequisites, the list cannot pursue or permanently close its largest external
payoff.

**Evidence.**

- docs/DISTRIBUTION.md sindresorhus/awesome deferred row
- README claims Awesome badge; curated depth 31; single sweep 2026-09
- CI already runs awesome-lint on PRs

**In scope.** Written acceptability assessment against the sindresorhus/awesome
membership bar; explicit go/no-go plus prerequisite README or process fixes;
DISTRIBUTION.md note update with decision date. Assessment only; do not open the
upstream PR.

**Out of scope.** Opening the awesome PR; org catalogue work; CI refactors.

**Why now.** Pure gate-assessment debt; resolves or closes the biggest external
payoff without blocking landing fixes.

**Triage notes.** PASS, no defects.

## P4: link-check-product-surface

| Field | Value |
|---|---|
| id | P4 |
| name | link-check-product-surface |
| size | S |
| deps | P1 |
| status | done |
| promoted_ids | [] |
| corroboration | 3 (value, risk, cohesion) |
| first_prompt | `/superpowers-process full landing link check coverage` |

**Problem.** PR and weekly lychee scan README.md only. The Pages landing exposes
full-list CTAs, eight section anchors, contribute links, and licence enquiry URLs
with zero link coverage, so product-surface rot never fails a PR or appears in
the weekly report.

**Evidence.**

- .github/workflows/link-check-pr.yml args README.md, fail: true; paths omit docs/
- .github/workflows/link-check-schedule.yml args README.md, fail: false
- docs/index.html outbound GitHub and labs hrefs

**In scope.** Add docs/index.html to lychee args on PR and schedule workflows;
extend link-check-pr paths filter to docs/index.html; keep PR fail:true and
schedule fail:false; keep lychee-action SHA pin.

**Out of scope.** Chip and anchor sync (P1); action tag pins (P5); entry content.

**Why now.** Without landing coverage, P1 can prove anchors match README while
outbound landing URLs rot uncaught.

**Triage notes.** PASS. Split with P1: gate owns chip/fragment asserts; this package
owns workflow args and fail policy.

## P5: pin-validate-setup-python

| Field | Value |
|---|---|
| id | P5 |
| name | pin-validate-setup-python |
| size | M |
| deps | none |
| status | done |
| promoted_ids | [] |
| corroboration | 3 (value, risk, cohesion) |
| first_prompt | `/superpowers-process full pin validate setup python` |

**Problem.** validate.yml and both link-check workflows pull actions by mutable
major tags (checkout@v4, setup-python@v5, setup-node@v4, create-issue-from-file@v5)
while only lychee-action is SHA-pinned. Gold sample awesome-archimate pins full
commit SHAs. A retagged major can change the runner under the gate without a
reviewable diff.

**Evidence.**

- .github/workflows/validate.yml checkout@v4, setup-python@v5
- .github/workflows/link-check-pr.yml checkout@v4, setup-node@v4
- .github/workflows/link-check-schedule.yml checkout@v4, create-issue-from-file@v5
- lychee-action already at e7477775783ea5526144ba13e8db5eec57747ce8

**In scope.** SHA-pin actions/checkout, actions/setup-python, actions/setup-node,
and peter-evans/create-issue-from-file across the three workflows with version
comments; leave lychee-action pin as-is unless comment refresh only.

**Out of scope.** Python/node version bumps; lychee args; check_release logic.

**Why now.** Independent CI hygiene on the path to merge main; can run any time.

**Triage notes.** PASS, no defects.
