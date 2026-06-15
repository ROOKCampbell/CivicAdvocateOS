import json, socket, ecdsa
from ledger_utils import HashUtility

# SECURE IDENTITY: Generate keys if none exist
def get_keys():
    try:
        with open("node.key", "rb") as f:
            sk = ecdsa.SigningKey.from_string(f.read())
    except FileNotFoundError:
        sk = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
        with open("node.key", "wb") as f:
            f.write(sk.to_string())
    return sk

# NETWORK BROADCAST: Send block to another node
def broadcast_block(block, target_ip, port=5000):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((target_ip, port))
            s.sendall(json.dumps(block).encode())
    except Exception as e:
        print(f"[*] Broadcast failed to {target_ip}: {e}")

print("[*] CIVIC ADVOCATE NODE ONLINE.")
print(f"[*] Node Identity: {get_keys().verifying_key.to_string().hex()[:16]}...")
