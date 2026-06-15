import json, sys, ecdsa, os
from ledger_utils import HashUtility

def get_keys():
    with open("node.key", "rb") as f:
        return ecdsa.SigningKey.from_pem(f.read())

def get_last_hash(blocks):
    # Fallback logic for different schema versions
    last_block = blocks[-1]
    return last_block.get('expected_hash', last_block.get('signature', '0'))

def cast_vote(proposal_id, vote):
    sk = get_keys()
    with open("manifest.json", "r") as f:
        blocks = json.load(f)
    
    proposal = next((b for b in blocks if b['id'] == proposal_id and b.get('type') == 'PROPOSAL'), None)
    if not proposal:
        print("[!] ERROR: Proposal ID not found.")
        return

    # Create VOTE block using robust hash retrieval
    new_block = {
        "id": blocks[-1]['id'] + 1,
        "type": "VOTE",
        "data": f"Vote {vote} for Proposal {proposal_id}",
        "prev_hash": get_last_hash(blocks),
        "pub_key": sk.verifying_key.to_string().hex()
    }
    new_block["signature"] = sk.sign(json.dumps(new_block, sort_keys=True).encode()).hex()
    
    blocks.append(new_block)
    with open("manifest.json", "w") as f:
        json.dump(blocks, f, indent=4)
    print(f"[*] VOTE '{vote}' RECORDED FOR PROPOSAL {proposal_id}.")

if __name__ == "__main__":
    with open("manifest.json", "r") as f:
        blocks = json.load(f)
    
    if len(sys.argv) == 3:
        cast_vote(int(sys.argv[1]), sys.argv[2])
    else:
        print("--- ACTIVE PROPOSALS ---")
        for b in blocks:
            if b.get('type') == 'PROPOSAL':
                print(f"ID: {b['id']} | Data: {b['data']}")
        print("\nUsage: python3 vote_proposal.py [ID] [YAY/NAY]")
