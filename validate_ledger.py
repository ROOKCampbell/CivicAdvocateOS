import json, datetime
from ledger_utils import validate_single_block
from concurrent.futures import ProcessPoolExecutor

def run_validation():
    with open("manifest.json", "r") as f:
        blocks = json.load(f)
    
    # Simple loop for validation to maintain chain order
    last_hash = "0" * 128
    for block in blocks:
        success, b_id = validate_single_block(block, last_hash)
        if not success:
            print(f"[!] CHAIN BROKEN AT BLOCK {b_id}!")
            return
        last_hash = block['expected_hash']
        
    print("[*] FULL CHAIN INTEGRITY VERIFIED.")

if __name__ == "__main__":
    run_validation()
