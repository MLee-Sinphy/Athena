#!/usr/bin/env bash
set -euo pipefail

if [[ "${ATHENA_DESTROY_CONFIRM:-}" != "destroy-athena-data" ]]; then
  echo "Refusing to delete data. Set ATHENA_DESTROY_CONFIRM=destroy-athena-data." >&2
  exit 2
fi

docker compose down --volumes --remove-orphans
echo "Athena local containers, network, database volume, and media volume were removed."
