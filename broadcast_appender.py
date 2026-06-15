import json, sys, ecdsa, socket, os
from ledger_utils import HashUtility

def get_keys():
    if not os.path.exists("node.key"):
        sk = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
        with open("node.key", "wb") as f:
            f.write(sk.to_pem())
        return sk
    with open("node.key", "rb") as f:
        return ecdsa.SigningKey.from_pem(f.read())

def add_governance_block(data, btype="PROPOSAL"):
    sk = get_keys()
    with open("manifest.json", "r") as f:
        blocks = json.load(f)
    
    new_block = {
        "id": blocks[-1]['id'] + 1,
        "type": btype,
        "data": data,
        "prev_hash": blocks[-1]['expected_hash'],
        "pub_key": sk.verifying_key.to_string().hex()
    }
    # Sign the JSON string of the block
    new_block["signature"] = sk.sign(json.dumps(new_block, sort_keys=True).encode()).hex()
    
    blocks.append(new_block)
    with open("manifest.json", "w") as f:
        json.dump(blocks, f, indent=4)
    print(f"[*] {btype} BLOCK {new_block['id']} SIGNED.")

if __name__ == "__main__":
    add_governance_block(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "PROPOSAL")
