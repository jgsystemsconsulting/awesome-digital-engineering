# Spec: link-check-product-surface

## Goal
Lychee PR and schedule workflows must scan docs/index.html as well as README.md. PR remains fail:true.

## Research
research: skipped (workflow config only; no external API)

## Requirements
- Add docs/index.html to lychee args in link-check-pr.yml and link-check-schedule.yml
- Add docs/index.html to PR paths filter
- Keep lychee-action SHA pin
