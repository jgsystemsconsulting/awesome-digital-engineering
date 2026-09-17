# Contributing to Awesome Digital Engineering

Thanks for helping keep this list accurate and useful.

## 1. How to contribute

Open a PR or use the **Suggest a resource** issue form. One resource per PR when practical.

## 2. Inclusion bar

A resource must be:

1. **On-topic** — digital thread, model-based definition (MBD), digital engineering policy/standards, or DE transformation practice (see FAMILY scope for this spoke).
2. **Substantive** — not a stub, not pure vendor marketing fluff.
3. **Live** — URL returns a real page.
4. **Not duplicative** — not already listed (see the canonical-URL rule, §6).
5. **Legally linkable** — publicly accessible. We **link**, we never re-host model files,
   paywalled standards PDFs, or proprietary content.

## 3. Entry format

One line per entry, hyphen separator (` - `, never an en/em-dash):

```
- [Resource Name](https://example.com) - One-line factual description `tag` `tag` (YYYY).
```

- **Description:** factual, one line, **≤ 140 characters** (measured from the first
  non-space character after ` - ` through the character before the first tag backtick).
- **Tags:** inline code spans before the terminal period, in axis order below.
- **Year:** parentheses as the last token.

## 4. Tag vocabulary (DE)

Axis order (FAMILY axes with first axis renamed for this list):

`domain → method → tool → has-model → type → spec/standard → paid → year`

This spoke **renames** the first FAMILY axis from `language` to `domain` as an intentional
per-list deviation (DE has no single modeling language). Documented here for contributors.

| Axis | Cardinality | Values |
|------|-------------|--------|
| domain | exactly 1 | `DE-general` · `digital-thread` · `MBD` |
| method | 0 or 1 | `MBE` · `GD&T` |
| tool | 0 or more | `other-tool` until a named tag graduates (≥3 entries, one PR) |
| has-model | 0 or 1 | only when primary URL is a downloadable DE-format file (`.step`/`.stp`/`.p21`, `.qif`, `.jt`); not on `type=tool` repo homes |
| type | exactly 1 | `tutorial` · `course` · `book` · `paper` · `report` · `blog` · `video` · `tool` · `plugin`. Standards/storefront/policy/program pages use `report`. |
| spec/standard | 0 or 1 | `spec` · `standard` (if present, type ∈ {report, book, paper}) |
| paid | 0 or 1 | `paid` |
| year | exactly 1 | `(YYYY)` |

**Section → default domain:** Policy→`DE-general`; Standards→`MBD` or `digital-thread` by subject (never `DE-general`); Digital thread→`digital-thread`; MBD/PMI→`MBD`; Government/consortia→`DE-general` unless single-family; Open tools→thread or MBD; Learning→`DE-general` unless topic-locked; Commercial→match product, always `paid`.

**`DE-general` rule:** legal only when the primary subject is not specifically digital-thread or MBD. Reviewers reject lazy `DE-general` on standards and pure MBD/thread tools.

## 5. The year rule (`YYYY`)

Use the resource's publication or last-substantive-update year as four digits. Prefer the
most recent author-published version date when versions exist. If the year is unknown,
omit the entry until known (do not invent a year).

## 6. Canonical-URL dedupe

Before deciding "is this a duplicate", canonicalize both URLs: force `https`, lowercase
the host, strip a trailing slash and non-semantic query parameters unless they are
semantically required. If the canonical forms match, it's a duplicate.

## 7. Editorial neutrality

Maintained by [JG Systems Consulting Ltd.](https://github.com/jgsystemsconsulting).
Competing products and standards appear alongside each other when they pass the inclusion
bar. Maintainer commercial offerings in this niche, if any, are disclosed here when they
exist; none are listed as preferred by default.

## 8. Pull request checklist

- [ ] On-topic for digital engineering / digital thread / MBD
- [ ] Live link, not a re-host
- [ ] Entry format and DE tags correct
- [ ] Not a duplicate under §6
