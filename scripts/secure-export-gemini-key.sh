#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 2 ]]; then
  echo "usage: $0 PUBLIC_KEY_FILE OUTPUT_FILE" >&2
  exit 64
fi

public_key_file=$1
output_file=$2

if [[ ! -s "$public_key_file" ]]; then
  echo "public key file is missing or empty" >&2
  exit 66
fi

if [[ -z "${GEMINI_API_KEY:-}" ]]; then
  echo "GEMINI_API_KEY is missing or empty" >&2
  exit 65
fi

umask 077
mkdir -p "$(dirname "$output_file")"

printf '%s' "$GEMINI_API_KEY" | openssl pkeyutl -encrypt \
  -pubin \
  -inkey "$public_key_file" \
  -pkeyopt rsa_padding_mode:oaep \
  -pkeyopt rsa_oaep_md:sha256 \
  -out "$output_file"

chmod 600 "$output_file"
echo "Encrypted Gemini key export created"
