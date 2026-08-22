#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 || ! -f "$1" ]]; then
  echo "Usage: $0 BACKUP_FILE" >&2
  exit 2
fi
: "${ATHENA_BACKUP_PASSPHRASE:?ATHENA_BACKUP_PASSPHRASE is required}"
: "${ATHENA_RESTORE_CONFIRM:?Set ATHENA_RESTORE_CONFIRM=restore-athena to continue}"
[[ "$ATHENA_RESTORE_CONFIRM" == "restore-athena" ]] || { echo "Restore not confirmed" >&2; exit 2; }

work_dir="$(mktemp -d)"
trap 'rm -rf -- "$work_dir"' EXIT
openssl enc -d -aes-256-cbc -pbkdf2 -pass env:ATHENA_BACKUP_PASSPHRASE \
  -in "$1" | tar -C "$work_dir" -xzf -
(cd "$work_dir" && sha256sum --check SHA256SUMS)

docker compose -f compose.production.yaml exec -T postgres \
  pg_restore --clean --if-exists --no-owner --no-privileges \
    -U "${POSTGRES_USER:-athena}" -d "${POSTGRES_DB:-athena}" <"$work_dir/database.dump"
docker compose -f compose.production.yaml run --rm --no-deps -T api \
  sh -c 'find /app/media -mindepth 1 -delete && tar -C /app/media -xf -' <"$work_dir/media.tar"
echo "Backup restored and checksums verified."
