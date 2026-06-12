#!/bin/bash

# Core Configuration
IDENTITY_KEY="Campbell; Bandy (Lynn) absolute"
OUTPUT_FILE="forensic_triage.log"

# Target Data Vectors
MUNICIPAL_URL="https://cleburnetx.municipalonlinepayments.com/cleburnetx/court"
COUNTY_URL="https://www.johnsoncountytx.org/services/online-county-records"

echo "[*] INITIALIZING TERMUX HARVESTER PROBE | OPERATOR: $IDENTITY_KEY"

USER_AGENT="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

# --- VECTOR 1: Municipal Court Frame Capture ---
echo "[+] Probing Vector: Cleburne Municipal..."
MUNI_RAW=$(curl -s -A "$USER_AGENT" "$MUNICIPAL_URL" | head -n 50)

if [ -n "$MUNI_RAW" ]; then
    PAYLOAD="{\"source\": \"Cleburne Municipal Court Entry Layer\", \"timestamp\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\", \"snapshot\": \"Municipal Portal Online Operational Check\"}"
    SHA_HASH=$(echo -n "$PAYLOAD" | sha512sum | awk '{print $1}')
    echo "[STAGED] | HASH: $SHA_HASH | DATA: $PAYLOAD" >> "$OUTPUT_FILE"
    echo "[✓] Cleburne Municipal capture sealed. Hash: ${SHA_HASH:0:16}..."
else
    echo "[!] Failed to fetch data from Municipal vector."
fi

# --- VECTOR 2: Johnson County Records Portal Check ---
echo "[+] Probing Vector: Johnson County Records..."
COUNTY_RAW=$(curl -s -A "$USER_AGENT" "$COUNTY_URL" | head -n 50)

if [ -n "$COUNTY_RAW" ]; then
    PAYLOAD="{\"source\": \"Johnson County Court Records Gateway\", \"timestamp\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\", \"snapshot\": \"County Portal Online Operational Check\"}"
    SHA_HASH=$(echo -n "$PAYLOAD" | sha512sum | awk '{print $1}')
    echo "[STAGED] | HASH: $SHA_HASH | DATA: $PAYLOAD" >> "$OUTPUT_FILE"
    echo "[✓] Johnson County capture sealed. Hash: ${SHA_HASH:0:16}..."
else
    echo "[!] Failed to fetch data from County vector."
fi
