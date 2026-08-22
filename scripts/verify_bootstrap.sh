#!/usr/bin/env bash

set -euo pipefail

project_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

required_files=(
  "frontend/package.json"
  "frontend/src/App.test.tsx"
  "backend/manage.py"
  "backend/config/settings.py"
  "backend/health/tests.py"
  "compose.yaml"
  ".github/workflows/ci.yml"
)

for relative_path in "${required_files[@]}"; do
  if [[ ! -f "$project_root/$relative_path" ]]; then
    echo "missing bootstrap file: $relative_path" >&2
    exit 1
  fi
done

echo "bootstrap structure verified"
