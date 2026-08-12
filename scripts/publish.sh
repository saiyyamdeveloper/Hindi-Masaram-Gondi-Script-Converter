#!/usr/bin/env bash
# Create the public GitHub repo and push main.
# Usage:
#   ./scripts/publish.sh YOUR_GITHUB_USERNAME
# Optional:
#   GH_TOKEN=ghp_... ./scripts/publish.sh YOUR_GITHUB_USERNAME
set -euo pipefail

REPO_NAME="masaram-gondi"
USER_NAME="${1:-${GITHUB_USER:-}}"

if [[ -z "$USER_NAME" ]]; then
  echo "Usage: $0 YOUR_GITHUB_USERNAME"
  echo "Optional: export GH_TOKEN=ghp_xxx  (repo + workflow scopes)"
  exit 1
fi

REMOTE="https://github.com/${USER_NAME}/${REPO_NAME}.git"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if [[ ! -d .git ]]; then
  git init -b main
fi

if [[ -n "${GH_TOKEN:-}" ]]; then
  echo "Creating public repo via API…"
  code=$(curl -sS -o /tmp/gh-create.json -w "%{http_code}" \
    -X POST "https://api.github.com/user/repos" \
    -H "Accept: application/vnd.github+json" \
    -H "Authorization: Bearer ${GH_TOKEN}" \
    -d "{\"name\":\"${REPO_NAME}\",\"description\":\"Devanagari → Masaram Gondi converter, 75-key keyboard, FlorisBoard layouts, Hindi–Gondi dictionary\",\"homepage\":\"https://${USER_NAME}.github.io/${REPO_NAME}/\",\"private\":false,\"has_issues\":true,\"has_wiki\":false,\"auto_init\":false}")
  echo "GitHub API HTTP ${code}"
  cat /tmp/gh-create.json
  echo
  if [[ "$code" != "201" && "$code" != "422" ]]; then
    echo "Repo create failed. Check the token (scopes: repo, workflow)."
    exit 1
  fi
  AUTH_REMOTE="https://x-access-token:${GH_TOKEN}@github.com/${USER_NAME}/${REPO_NAME}.git"
  git remote remove origin 2>/dev/null || true
  git remote add origin "$REMOTE"
  git push -u "$AUTH_REMOTE" main
  echo
  echo "Enabling GitHub Pages (Actions)…"
  curl -sS -X POST \
    -H "Accept: application/vnd.github+json" \
    -H "Authorization: Bearer ${GH_TOKEN}" \
    "https://api.github.com/repos/${USER_NAME}/${REPO_NAME}/pages" \
    -d '{"build_type":"workflow"}' || true
  echo
  echo "Repo:  https://github.com/${USER_NAME}/${REPO_NAME}"
  echo "Site:  https://${USER_NAME}.github.io/${REPO_NAME}/"
  echo "(first Pages deploy takes ~1 minute after the workflow runs)"
else
  git remote remove origin 2>/dev/null || true
  git remote add origin "$REMOTE"
  echo
  echo "Local repo is ready. On your machine (GitHub CLI or browser):"
  echo
  echo "  1) Create the empty public repo:"
  echo "       https://github.com/new   name=${REPO_NAME}  (no README)"
  echo "     or:  gh repo create ${REPO_NAME} --public --source=. --remote=origin --push"
  echo
  echo "  2) Push:"
  echo "       git push -u origin main"
  echo
  echo "  3) Settings → Pages → Source: GitHub Actions"
  echo
  echo "Site will be: https://${USER_NAME}.github.io/${REPO_NAME}/"
fi
