#!/bin/bash
# Compressing the full mission state for Lead Partner review
tar -czf system_dump_full_061226.tar.gz ~/CivicAdvocate.OS/
sha512sum system_dump_full_061226.tar.gz > system_dump_full_061226.hash
echo "[SYS] State-dump complete."
echo "[SYS] Manifest: system_dump_full_061226.tar.gz"
echo "[SYS] Anchor Hash: $(cat system_dump_full_061226.hash)"
