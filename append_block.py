import json, sys
from ledger_utils import HashUtility

def add_new_block(data):
    try:
        with open("manifest.json", "r") as f:
            blocks = json.load(f)
            last_hash = blocks[-1]['expected_hash']
            new_id = blocks[-1]['id'] + 1
    except (FileNotFoundError, IndexError):
        blocks = []
        last_hash = "0" * 128  # Genesis block
        new_id = 1

    # New hash includes previous hash + new data
    combined_data = last_hash + data
    new_hash = HashUtility.calculate_hash(combined_data)
    
    blocks.append({
        "id": new_id, 
        "data": data, 
        "prev_hash": last_hash, 
        "expected_hash": new_hash
    })
    
    with open("manifest.json", "w") as f:
        json.dump(blocks, f, indent=4)
    print(f"[*] BLOCK {new_id} APPENDED (Linked to {last_hash[:10]}...).")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        add_new_block(sys.argv[1])
    else:
        print("Usage: python3 append_block.py 'data'")
