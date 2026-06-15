import json, datetime, sys
from ledger_utils import validate_single_block
from concurrent.futures import ProcessPoolExecutor

def run_validation():
    try:
        with open("manifest.json", "r") as f:
            blocks = json.load(f)
    except FileNotFoundError:
        print("[-] NO MANIFEST FOUND.")
        return

    last_hash = "0" * 128
    valid_chain = True
    
    print("[*] PERFORMING CRYPTOGRAPHIC CHAIN VERIFICATION...")
    
    with open("audit.log", "a") as log:
        for block in blocks:
            success, b_id = validate_single_block(block, last_hash)
            
            status = "SUCCESS" if success else "CRITICAL FAILURE"
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log.write(f"[{timestamp}] Block {b_id}: {status}\n")
            
            if not success:
                print(f"[!] CHAIN BROKEN AT BLOCK {b_id}!")
                valid_chain = False
                break
                
            print(f"[Block {b_id}] Verification: {status}")
            last_hash = block['expected_hash']
            
    if valid_chain:
        print("[*] FULL CHAIN INTEGRITY VERIFIED.")
        with open("last_sync.txt", "w") as f:
            f.write(str(blocks[-1]['id']))

if __name__ == "__main__":
    run_validation()
