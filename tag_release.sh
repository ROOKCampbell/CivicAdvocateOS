#!/bin/bash

# Usage: ./tag_release.sh <version> "<message>"
# Example: ./tag_release.sh v1.0.0 "First official production release"

if [ -z "$1" ] || [ -z "$2" ]; then
    echo "Error: Missing arguments."
    echo "Usage: $0 <version> <message>"
    exit 1
fi

git tag -a "$1" -m "$2"
git push origin "$1"

echo "Tag $1 pushed successfully."
