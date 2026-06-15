#!/usr/bin/env bash
# ==============================================================================
# CIVICADVOCATE.OS / LEGACYENGINE - PUBLIC GATEWAY DEPLOYER
# FILE: deploy_gateway.sh
# ENVIRONMENT: Termux (Android/Linux)
# AUTHOR: Lead Partner and Architect
# ==============================================================================

set -e

echo "[-] INITIALIZING DEPLOYMENT ROUTINE..."

# Step 1: Run the Core Orchestrator to ensure hashes are synced
echo "[*] RUNNING LOCAL ENFORCEMENT ORCHESTRATOR..."
python3 orchestrator.py

# Step 2: Extract the zero-knowledge public manifest patch
echo "[*] RE-GENERATING ZERO-KNOWLEDGE PUBLIC MANIFEST..."
python3 patch_public_gateway.py

# Step 3: Verify local Git tracking initialization
if [ ! -d ".git" ]; then
    echo "[!] Git repository not initialized locally. Initializing 'main' branch..."
    git init -b main
fi

# Step 4: Stage only the public-facing transport file (Keep core files untracked/ignored)
echo "[*] STAGING PUBLIC MANIFEST FOR LEDGER EXPORT..."
if [ ! -f ".gitignore" ]; then
    echo "Writing safety constraints to .gitignore..."
    echo "orchestrator.py" > .gitignore
    echo "patch_public_gateway.py" >> .gitignore
    echo "deploy_gateway.sh" >> .gitignore
    echo "sys/" >> .gitignore
    echo "*.pyc" >> .gitignore
fi

git add public_manifest.json .gitignore

# Step 5: Execute Cryptographic State Commit
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S %Z")
COMMIT_MESSAGE="State Sync Seal: ${TIMESTAMP}"

echo "[*] RECORDING BLOCK COMMIT TO CHRONOLOGICAL LEDGER..."
git commit -m "${COMMIT_MESSAGE}"

echo "------------------------------------------------------------"
echo "[+] DEPLOYMENT STAGING COMPLETE."
echo "[!] To transmit live to a remote public gateway host, configure your upstream destination:"
echo "    Command: git remote add origin <your_public_repository_url>"
echo "    Command: git push -u origin main"
echo "------------------------------------------------------------"

