# Distribution ledger · awesome-digital-engineering

One row per place this product is, or could be, distributed and discovered
(RR-B-36). Statuses: `submitted`, `in progress`, `deferred`, `deliberate N/A`,
`planned`. Non-submitted rows carry decision + date. Revisit every release.

Last reviewed: 0.1.1 / 2026-09-18

Posture: open-source curated list (CC0-1.0). Not an MCP bridge, skills pack, or
installable agent plugin. In-host marketplace rows are deliberate N/A.

## In-host marketplaces (RR-B-29a)

| Channel | Manifest | Status | Decision / reason | Date |
|---|---|---|---|---|
| Claude Code plugin directory | n/a | deliberate N/A | Curated list, not a Claude plugin or skill pack. | 2026-09-17 |
| Cursor marketplace | n/a | deliberate N/A | Not a Cursor extension. | 2026-09-17 |
| OpenAI Codex Plugin Directory | n/a | deliberate N/A | Not a Codex plugin. | 2026-09-17 |
| Gemini CLI extensions gallery | n/a | deliberate N/A | Not a Gemini extension. | 2026-09-17 |

## Web directories and catalogues

| Channel | Artifact | Status | Decision / reason | Date |
|---|---|---|---|---|
| GitHub Pages landing | docs/index.html | submitted | Path S static landing under docs/; chips and section index gated by scripts/check_release.py. | 2026-09-18 |
| Org catalogue (https://labs.jgsystemsconsulting.com/) | site entry | submitted | Entry added in jgsystemsconsulting-website data/products.yml + regenerated docs/index.html (branch feat/awesome-digital-engineering-catalogue-entry, commit ba61ac2). Live after Labs site merge/deploy. | 2026-09-18 |
| GitHub About + topics + Release | configure_repo.sh + gh release | in progress | Description and topics set; point homepage at Pages URL after Pages enabled on main. | 2026-09-18 |
| sindresorhus/awesome | PR | deferred | Acceptability assessed 2026-09-18: go with prerequisites (clean lychee README+landing after main ship, keep depth/quality, re-read PR template at submit). Assessment: docs/superpowers/specs/2026-09-18-awesome-acceptability-assessment.md. Do not open PR until prerequisites clear. | 2026-09-18 |
| Other community awesome-lists | PR | deferred | Assess each list bar before submitting. | 2026-09-17 |

## MCP aggregator directories (RR-M-07)

| Channel | Artifact | Status | Decision / reason | Date |
|---|---|---|---|---|
| awesome-mcp-servers / Glama / Smithery / PulseMCP | n/a | deliberate N/A | Not an MCP server product. | 2026-09-17 |

## Process notes

| Topic | Status | Decision / reason | Date |
|---|---|---|---|
| RR-B-27 squash-merge authors | deferred | GitHub squash merges attribute to the merging account email; force-push rewrite blocked by RR-B-23 protection. Accept until solo merge uses noreply identity in gh settings, or lift force-push briefly for a one-shot history rewrite. | 2026-09-17 |
| RR-B-01 LICENSE org name | submitted | Canonical CC0 body + appendix naming JG Systems Consulting Ltd (PR #9). | 2026-09-17 |

Multi-page assessment (RR-B-30): content walked; outcome is one HTML landing plus the README as deep content; nothing justifies a third page.
