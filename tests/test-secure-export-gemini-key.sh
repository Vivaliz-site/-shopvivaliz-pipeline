#!/usr/bin/env bash
set -euo pipefail

repo_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
tmp_dir=$(mktemp -d)
trap 'rm -rf "$tmp_dir"' EXIT

openssl genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:2048 \
  -out "$tmp_dir/private.pem" 2>/dev/null
openssl pkey -in "$tmp_dir/private.pem" -pubout \
  -out "$tmp_dir/public.pem" 2>/dev/null

export GEMINI_API_KEY='test-gemini-key-with-special_chars-123'
combined_output=$(
  "$repo_root/scripts/secure-export-gemini-key.sh" \
    "$tmp_dir/public.pem" \
    "$tmp_dir/gemini-key.enc" 2>&1
)

if [[ "$combined_output" == *"$GEMINI_API_KEY"* ]]; then
  echo "FAIL: secret leaked to process output" >&2
  exit 1
fi

openssl pkeyutl -decrypt \
  -inkey "$tmp_dir/private.pem" \
  -in "$tmp_dir/gemini-key.enc" \
  -pkeyopt rsa_padding_mode:oaep \
  -pkeyopt rsa_oaep_md:sha256 \
  -out "$tmp_dir/decrypted.txt"

if [[ "$(cat "$tmp_dir/decrypted.txt")" != "$GEMINI_API_KEY" ]]; then
  echo "FAIL: decrypted value does not match the source secret" >&2
  exit 1
fi

if grep -Fq "$GEMINI_API_KEY" "$tmp_dir/gemini-key.enc"; then
  echo "FAIL: ciphertext contains plaintext secret" >&2
  exit 1
fi

echo "PASS: Gemini key export is encrypted and silent"
