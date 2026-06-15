#!/bin/bash

# CivicAdvocate.OS Repository Initialization
# Target: Public sync for discovery and indexing

echo "[*] Initializing Git Repository..."
git init

echo "[*] Adding project nodes..."
git add .

echo "[*] Committing baseline..."
git commit -m "Initial commit: CivicAdvocate.OS Core and Audit Utilities"

# Replace with your actual repository URL
# Use 'git remote add origin https://github.com/YOUR_USERNAME/CivicAdvocate.OS.git' 
# or SSH equivalent
echo "[*] Configuring remote..."
git remote add origin <YOUR_REMOTE_URL>

echo "[*] Pushing to master..."
git push -u origin main

echo "[+] Repository initialized and synchronized."
