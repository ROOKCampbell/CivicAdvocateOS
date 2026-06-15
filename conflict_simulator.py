import json, socket, ecdsa, time
from ledger_utils import HashUtility

# 1. GENERATE A ROGUE PEER IDENTITY
print("[*] GENERATING ROGUE PEER IDENTITY...")
rogue_sk = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
rogue_pub = rogue_sk.verifying_key.to_string().hex()

# 2. DEFINE CONFLICTING BLOCK (BLOCK #4)
conflict_data = {
    "id": 4, # THIS IS THE CONFLICT: Assumes last_hash is unknown
    "data": "Rogue Data (Consensus Test)",
    "prev_hash": "c001da4a001da4... (Simulated Link)",
    "pub_key": rogue_pub
}

# 3. SIGN AND CALCULATE HASH (Self-consistent)
print(f"[*] FORGING BLOCK {conflict_data['id']} (Linked to rogue chain)...")
forged_hash = HashUtility.calculate_hash(conflict_data['prev_hash'] + conflict_data['data'])
forged_sig = rogue_sk.sign(forged_hash.encode()).hex()

conflict_data["expected_hash"] = forged_hash
conflict_data["signature"] = forged_sig

# 4. BROADCAST CONFLICT TO LOCAL LISTENER
try:
    print(f"[*] ATTENDANT BROADCASTING BLOCK {conflict_data['id']} TO LOCAL NODE...")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(('127.0.0.1', 5000)) # Targeted to your existing listener
        s.sendall(json.dumps(conflict_data).encode())
        print("[*] CONFLICT BROADCAST COMPLETE.")
except ConnectionRefusedError:
    print("[!] ERROR: network_node.py IS NOT RUNNING ON PORT 5000.")
