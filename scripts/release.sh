#!/usr/bin/env bash

set -e

VERSION=$(cat VERSION)
TAG="v${VERSION}"

echo "Preparing release ${TAG}..."

# Ensure we're on main
CURRENT_BRANCH=$(git branch --show-current)

if [ "$CURRENT_BRANCH" != "main" ]; then
    echo "You must be on the main branch."
    exit 1
fi

# Commit any changes
git add .

if ! git diff --cached --quiet; then
    git commit -m "release: ${TAG}"
fi

# Update main branch
git push origin main

# Check if tag already exists
if git rev-parse "$TAG" >/dev/null 2>&1; then
    echo "Tag ${TAG} already exists."
    exit 1
fi

# Create tag
git tag "$TAG"

# Push tag
git push origin "$TAG"

echo ""
echo "Release ${TAG} has been published."