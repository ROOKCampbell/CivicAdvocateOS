#!/data/data/com.termux/files/usr/bin/bash
# ==============================================================================
# SECURE REMOTE COUPLING PROTOCOL
# ==============================================================================

GIT_DIR="$HOME/CivicAdvocate.OS"
REMOTE_URL="git@github.com:thespiritadvocate101/CivicAdvocate.OS.git"

cd "$GIT_DIR"

echo "[*] Configuring remote synchronization pathways..."

# Verify or clear existing origin pathing safely
if git remote | grep -q "origin"; then
    git remote set-url origin "$REMOTE_URL"
else
    git remote add origin "$REMOTE_URL"
fi

echo "[+] Remote target locked: $REMOTE_URL"
echo "[*] Executing authenticated cryptographic push..."

# Update sync script to handle ongoing automated pushing
sed -i 's/git push origin main/git push -u origin main --force/' ./sync_git_ledger.sh

# Fire the manual sync script pass to deploy remote state instantly
./sync_git_ledger.sh
