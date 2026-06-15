import json, sys, ecdsa, socket
from ledger_utils import HashUtility

# 1. Identity Logic
def get_keys():
    try:
        with open("node.key", "rb") as f:
            sk = ecdsa.SigningKey.from_string(f.read())
    except FileNotFoundError:
        sk = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
        with open("node.key", "wb") as f:
            f.write(sk.to_string())
    return sk

# 2. Networking Logic
def broadcast_block(block, peers=["127.0.0.1"]):
    for peer_ip in peers:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((peer_ip, 5000))
                s.sendall(json.dumps(block).encode())
                print(f"[*] BLOCK BROADCASTED TO {peer_ip}")
        except Exception as e:
            print(f"[*] PEER {peer_ip} UNAVAILABLE: {e}")

# 3. Main Logic
def add_and_broadcast(data):
    sk = get_keys()
    with open("manifest.json", "r") as f:
        blocks = json.load(f)
    
    last_hash = blocks[-1]['expected_hash']
    new_hash = HashUtility.calculate_hash(last_hash + data)
    signature = sk.sign(new_hash.encode()).hex()
    
    new_block = {
        "id": blocks[-1]['id'] + 1,
        "data": data,
        "prev_hash": last_hash,
        "expected_hash": new_hash,
        "signature": signature,
        "pub_key": sk.verifying_key.to_string().hex()
    }
    
    blocks.append(new_block)
    with open("manifest.json", "w") as f:
        json.dump(blocks, f, indent=4)
        
    broadcast_block(new_block)

if __name__ == "__main__":
    add_and_broadcast(sys.argv[1])
