#!/usr/bin/env bash
# Copyright (c) 2026 JG Systems Consulting Ltd. See LICENSE.
# SPDX-License-Identifier: CC0-1.0
# Idempotent platform configuration (RR-B-21/23) via the gh CLI.
set -euo pipefail

OWNER="jgsystemsconsulting"
REPO="awesome-digital-engineering"
DESCRIPTION="A curated list of digital engineering, digital thread, and model-based definition resources"
# Pages landing (RR-B-20) when enabled; empty skips
HOMEPAGE=""
TOPICS=(awesome awesome-list digital-engineering digital-thread mbd mbse)
# CI check names required before merge (RR-B-23); match job names from workflows
CI_CHECKS=("validate" "lychee" "awesome-lint")
BRANCH="$(gh api "repos/$OWNER/$REPO" --jq .default_branch)"

gh repo edit "$OWNER/$REPO" --description "$DESCRIPTION"
[ -n "$HOMEPAGE" ] && gh repo edit "$OWNER/$REPO" --homepage "$HOMEPAGE"
for t in "${TOPICS[@]}"; do gh repo edit "$OWNER/$REPO" --add-topic "$t"; done

# Branch protection: PR + green CI, no force-push/deletion; solo-maintainer
# shape (enforce_admins off, 0 required approvals) per RR-B-23.
# contexts must match the check names GitHub reports on PRs.
gh api -X PUT "repos/$OWNER/$REPO/branches/$BRANCH/protection" \
  --input - <<JSON
{
  "required_status_checks": {"strict": true, "contexts": $(printf '%s\n' "${CI_CHECKS[@]}" | python -c 'import json,sys; print(json.dumps([l.strip() for l in sys.stdin if l.strip()]))')},
  "enforce_admins": false,
  "required_pull_request_reviews": {"required_approving_review_count": 0},
  "restrictions": null,
  "allow_force_pushes": false,
  "allow_deletions": false
}
JSON

echo "verify:"
gh repo view "$OWNER/$REPO" --json description,homepageUrl,repositoryTopics
gh api "repos/$OWNER/$REPO/branches/$BRANCH/protection" --jq \
  '{checks: .required_status_checks.contexts, force: .allow_force_pushes.enabled, del: .allow_deletions.enabled}'
