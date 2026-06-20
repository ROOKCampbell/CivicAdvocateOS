import os
import re
import sys
import hashlib
import json
from typing import Dict, Any

class LedgerAppendEngine:
    """
    Automated Disk Sync Layer for CIVICADVOCATE.OS.
    Appends normalized GLO entries to ledger_store and dynamically updates validation targets.
    """
    def __init__(self, workspace_dir: str = "/data/data/com.termux/files/home/CivicAdvocate.OS"):
        self.workspace_dir = workspace_dir
        self.storage_dir = os.path.join(workspace_dir, "ledger_store")
        self.validator_path = os.path.join(workspace_dir, "forensic_validator.py")

    def calculate_sha512(self, payload: str) -> str:
        """Calculates absolute hash signature over a raw text block."""
        return hashlib.sha512(payload.encode('utf-8')).hexdigest()

    def get_next_block_index(self) -> int:
        """Scans ledger_store to find the next sequential file index slot."""
        if not os.path.exists(self.storage_dir):
            return 1
        
        max_idx = 0
        for file_name in os.listdir(self.storage_dir):
            match = re.match(r"block_(\d+)\.json", file_name)
            if match:
                idx = int(match.group(1))
                if idx > max_idx:
                    max_idx = idx
        return max_idx + 1

    def write_and_sync_ledger(self, canonical_payload_str: str) -> bool:
        """Writes data block to disk and updates target hashes in validator source code."""
        try:
            next_idx = self.get_next_block_index()
            file_name = f"block_{next_idx:02d}.json"
            file_path = os.path.join(self.storage_dir, file_name)

            # 1. Enforce target filesystem write override capabilities locally
            if os.path.exists(file_path):
                os.chmod(file_path, 0o744)

            # 2. Write the canonical zero-whitespace record string natively
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(canonical_payload_str)
            os.chmod(file_path, 0o444) # Lock down newly appended block data immediately
            print(f"[+] Appended record cleanly to: ledger_store/{file_name}")

            # 3. Calculate definitive signature directly from the written text asset
            new_block_hash = self.calculate_sha512(canonical_payload_str)

            # 4. Lift validation file protection layers to allow structural updates
            if os.path.exists(self.validator_path):
                os.chmod(self.validator_path, 0o744)
            else:
                sys.stderr.write("[-] Path configuration missing: forensic_validator.py not found.\n")
                return False

            with open(self.validator_path, 'r', encoding='utf-8') as f:
                validator_code = f.read()

            # 5. Parse out target registry and map new hash definition keys
            target_marker = "target_hashes = {"
            if target_marker not in validator_code:
                sys.stderr.write("[-] Validator update mismatch: Target dictionary hook missing.\n")
                return False

            # Inject the sequential entry directly inside the mapping declaration block
            injection_str = f"{target_marker}\n        {next_idx}: \"{new_block_hash}\","
            updated_code = validator_code.replace(target_marker, injection_str)

            # 6. Save modified validator logic
            with open(self.validator_path, 'w', encoding='utf-8') as f:
                f.write(updated_code)
            
            os.chmod(self.validator_path, 0o555) # Freeze execution permissions again
            print(f"[+] Dynamic validation array locked entry key: {next_idx}")
            return True

        except Exception as e:
            sys.stderr.write(f"[-] Ledger synchronization error sequence failed: {str(e)}\n")
            return False

if __name__ == "__main__":
    # Test vector input representing raw ingestion model returned from step 1
    canonical_glo_record = '{"abstract":"Abstract 544","file_number":"GLO-TX-00544","grantee":"SILAS E. BANDY","ingestion_timestamp":1782000000,"page_number":"312","patent_number":"NO. 124 VOL 9","survey":"Silas Elbert Bandy Survey","volume_id":"9-B"}'
    
    sync_engine = LedgerAppendEngine()
    success = sync_engine.write_and_sync_ledger(canonical_glo_record)
    print(f"[+] Transaction verification tracking state: {success}")
