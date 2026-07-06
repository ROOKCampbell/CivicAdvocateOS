#!/usr/bin/env python3
# CivicAdvocate.OS | Production Authenticated Network Interface
# Workflow: Overview -> Code -> Implementation

import os
import sys
import json
import hmac
import hashlib
from aiohttp import web

# 1. Load Live Cryptographic Environment Context
PRIVATE_KEY = os.getenv("ARCHITECT_PRIVATE_KEY")
NODE_ADDRESS = os.getenv("NODE_ADDRESS")
LOG_DIR = "/data/data/com.termux/files/home/civicadvocate/ledger/mainnet"
LEDGER_PATH = os.path.join(LOG_DIR, "genesis_ledger.dat")

if not PRIVATE_KEY or not NODE_ADDRESS:
    print("[-] Error: Active cryptographic credentials missing from environment.")
    print("[*] Resolution: Run 'source ~/node.env' before launching the listener.")
    sys.exit(1)

routes = web.RouteTableDef()

def verify_payload_signature(payload_dict, provided_signature):
    """Verifies that incoming transactions were signed correctly."""
    serialized = json.dumps(payload_dict, sort_keys=True).encode('utf-8')
    key_bytes = bytes.fromhex(PRIVATE_KEY)
    expected_signature = hmac.new(key_bytes, serialized, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected_signature, provided_signature)

@routes.post('/v1/ledger/append')
async def handle_append(request):
    try:
        data = await request.json()
        payload = data.get("payload")
        signature = data.get("signature")
        signer = data.get("signer")
        
        if not payload or not signature or not signer:
            return web.json_response({"status": "REJECTED", "reason": "Malformed data package structure."}, status=400)
            
        # Security Guard: Validate sender signature match against node authority
        if signer.lower() != NODE_ADDRESS.lower():
            return web.json_response({"status": "REJECTED", "reason": "Signer address does not match node authority."}, status=401)
            
        if not verify_payload_signature(payload, signature):
            return web.json_response({"status": "REJECTED", "reason": "Cryptographic signature verification failed."}, status=403)
            
        # Write verified data directly into the active genesis_ledger file
        with open(LEDGER_PATH, 'a') as f:
            f.write(json.dumps({"payload": payload, "signer": signer, "signature": signature}) + "\n")
            
        print(f"[+] Cryptographically verified block accepted and appended via network port.")
        return web.json_response({"status": "SUCCESS", "message": "Transaction verified and committed to ledger."})
        
    except Exception as e:
        return web.json_response({"status": "ERROR", "reason": str(e)}, status=500)

async def init_app():
    app = web.Application()
    app.add_routes(routes)
    return app

if __name__ == "__main__":
    print("=== CivicAdvocate.OS Network Listener Initializing ===")
    print(f"[+] Binding interface to Node Address: {NODE_ADDRESS}")
    print("[+] Launching on target host: http://127.0.0.1:8080")
    web.run_app(init_app(), host='127.0.0.1', port=8080)
