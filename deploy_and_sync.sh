#!/bin/bash
# CivicAdvocate.OS - Final Deployment & Sync Script

echo "[*] Killing existing node processes..."
pkill -f network_node.py

echo "[*] Launching persistent node listener..."
nohup python3 network_node.py > node.log 2>&1 &

echo "[*] Waiting 2 seconds for node to bind..."
sleep 2

echo "[*] Executing peer-to-peer sync..."
python3 sync_client.py

echo "[*] Audit Report:"
python3 audit_report.py
