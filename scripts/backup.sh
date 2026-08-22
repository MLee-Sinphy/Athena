#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 BACKUP_DIRECTORY" >&2
  exit 2
fi
: "${ATHENA_BACKUP_PASSPHRASE:?ATHENA_BACKUP_PASSPHRASE is required}"

backup_root="$1"
timestamp="$(date -u +%Y%m%dT%H%M%SZ)"
work_dir="$(mktemp -d)"
trap 'rm -rf -- "$work_dir"' EXIT
mkdir -p -- "$backup_root"

docker compose -f compose.production.yaml exec -T postgres \
  pg_dump -U "${POSTGRES_USER:-athena}" -d "${POSTGRES_DB:-athena}" -Fc \
  >"$work_dir/database.dump"
docker compose -f compose.production.yaml run --rm --no-deps -T api \
  tar -C /app/media -cf - . >"$work_dir/media.tar"
(cd "$work_dir" && sha256sum database.dump media.tar >SHA256SUMS)
tar -C "$work_dir" -czf - database.dump media.tar SHA256SUMS | \
  openssl enc -aes-256-cbc -salt -pbkdf2 -pass env:ATHENA_BACKUP_PASSPHRASE \
    -out "$backup_root/athena-daily-$timestamp.tar.gz.enc"

if [[ "$(date -u +%u)" == "7" ]]; then
  cp -- "$backup_root/athena-daily-$timestamp.tar.gz.enc" \
    "$backup_root/athena-weekly-$timestamp.tar.gz.enc"
fi

find "$backup_root" -type f -name 'athena-daily-*.tar.gz.enc' -mtime +7 -delete
find "$backup_root" -type f -name 'athena-weekly-*.tar.gz.enc' -mtime +28 -delete
echo "$backup_root/athena-daily-$timestamp.tar.gz.enc"
