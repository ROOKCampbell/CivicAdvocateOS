from ledger_utils import validate_single_block
from concurrent.futures import ProcessPoolExecutor

# Mock data - Replace this with your file loading logic
blocks = [
    {'id': 1, 'data': 'data_chunk_1', 'expected_hash': '...'},
    {'id': 2, 'data': 'data_chunk_2', 'expected_hash': '...'}
]

def run_validation(block_list):
    print("[*] STARTING PARALLEL VALIDATION...")
    with ProcessPoolExecutor() as executor:
        results = list(executor.map(validate_single_block, block_list))
    
    for success, block_id in results:
        status = "SUCCESS" if success else "FAILED"
        print(f"[Block {block_id}] Verification: {status}")

if __name__ == "__main__":
    run_validation(blocks)
