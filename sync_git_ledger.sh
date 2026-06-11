#!/data/data/com.termux/files/usr/bin/bash
# ==============================================================================
# REPO SYNC: CivicAdvocate.OS / Truth Mandate Ledger
# ==============================================================================

LEDGER_FILE="/data/data/com.termux/files/home/truth_mandate/ledger/mission_ledger.jsonl"
GIT_DIR="$HOME/CivicAdvocate.OS"

if [ ! -d "$GIT_DIR" ]; then
    echo "[!] Git repository directory not found."
    exit 1
fi

cd "$GIT_DIR"
cp "$LEDGER_FILE" ./ledger/mission_ledger.jsonl

# Generate SHA-512 fingerprint for the commit message
FINGERPRINT=$(sha512sum "$LEDGER_FILE" | awk '{print $1}')

git add .
git commit -m "Truth Mandate Ledger Update | Anchor: ${FINGERPRINT:0:16}"
git push origin main
echo "[+] Ledger pushed to repository with anchor: ${FINGERPRINT:0:16}"
