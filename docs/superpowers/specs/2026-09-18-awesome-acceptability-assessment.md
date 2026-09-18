# Spec and assessment: awesome-acceptability-assessment (P3)

Date: 2026-09-18
Package: P3

## Problem

sindresorhus/awesome list PR is deferred because the acceptability gate was never assessed.

## Research

Primary sources consulted this session:

- https://github.com/sindresorhus/awesome/blob/main/awesome.md (contribution guidelines; create-list guidance)
- https://github.com/sindresorhus/awesome/blob/main/pull_request_template.md
- https://github.com/sindresorhus/awesome (README list structure)

research: local assessment with official awesome contribution docs (URLs above)

## Assessment criteria (from awesome contribution guidance)

1. List must be useful and focused; not a dumping ground.
2. Descriptions must be clear and not promotional fluff.
3. Table of contents and consistent formatting.
4. Links must work; dead links fail review.
5. Prefer established resources; avoid low-quality or spam.
6. Naming: Awesome X pattern; avoid trademark abuse.
7. Review bandwidth: maintainers are slow; list must be high quality before PR.
8. Badge and LICENSE expectations for listed projects.

## Awesome Digital Engineering against the bar

| Criterion | Status | Notes |
|---|---|---|
| Focus | PASS | Digital engineering transformation only (thread, MBD, policy/standards); 8 sections, 31 curated entries |
| Format | PASS | Family entry format with tags and year; Contents present; awesome-lint in CI |
| Links | PASS at launch | lychee on README; product-surface package adds docs/index.html |
| Naming | PASS | Awesome Digital Engineering matches Awesome X |
| Badge | PASS | awesome.re badge already on README |
| Licence | PASS | CC0-1.0 list; upstream keep own licences |
| Depth | PASS (borderline cleared) | 31 curated entries across eight sections; Commercial platforms still empty by design until verified |
| Freshness process | PASS | weekly lychee + release gate; last full sweep 2026-09 |
| CONTRIBUTING | PASS | inclusion bar and editorial neutrality |
| Self-promotion | PASS | editorial neutrality cited; commercial section empty until verified |

## Decision

**Go, with prerequisites (not PR-now).**

Do **not** open the sindresorhus/awesome PR in this package. Prerequisites before a future PR:

1. Keep curated depth at or above current quality; fill Commercial platforms only with verified, non-promotional entries when ready.
2. One clean full-sweep lychee run (README + landing) with zero open broken-link issues after the product-surface package lands on main.
3. Confirm list still matches awesome.md formatting conventions (TOC, descriptions, no marketing fluff).
4. Re-read the current PR template on sindresorhus/awesome the week of submission (templates change).

**No-go** only if the project abandons public awesome-list distribution. That is not the case.

## DISTRIBUTION.md update

Update the sindresorhus/awesome row: deferred with decision date 2026-09-18 and the go-with-prerequisites note above.

## Non-goals

- Opening the PR in this package
- Org catalogue work (P2)
- Community directory scatter-posts
