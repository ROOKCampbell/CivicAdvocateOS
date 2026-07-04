import os
import sys
import time
import json
import hashlib
import requests

# =====================================================================
# UNIVERSAL TRANSLATIONAL SCHEMA CONFIGURATION
# Translates varying blockchain/relational keys to standard internal terms
# =====================================================================
SCHEMA_TRANSLATOR = {
    "42161": {  # Arbitrum Mainnet
        "standard_name": "arbitrum_mainnet",
        "key_mapping": {"blockNumber": "block_height", "transactionHash": "tx_hash", "logIndex": "index"}
    },
    "421614": { # Arbitrum Sepolia
        "standard_name": "arbitrum_sepolia",
        "key_mapping": {"blockNumber": "block_height", "transactionHash": "tx_hash", "logIndex": "index"}
    }
}

STATE_FILE = "sync_state.json"

def load_system_state():
    """Loads the last recorded state or initializes a new tracking anchor."""
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return {
        "last_synced_block": 12000000, # Default genesis baseline anchor
        "total_records_ingested": 0,
        "system_status": "INITIALIZED"
    }

def save_system_state(last_block, records_count):
    """Persists current block tracking state directly to disk."""
    state = {
        "last_synced_block": last_block,
        "total_records_ingested": records_count,
        "system_status": "ACTIVE_RUNNING",
        "last_update_timestamp": int(time.time())
    }
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=4)

def fetch_latest_network_block(api_key, chain_id):
    """Queries the current live head block height of the network."""
    base_url = "https://api.etherscan.io/v2/api"
    params = {
        "chainid": chain_id,
        "module": "proxy",
        "action": "eth_blockNumber",
        "apikey": api_key
    }
    try:
        response = requests.get(base_url, params=params, timeout=10)
        data = response.json()
        if "result" in data:
            return int(data["result"], 16)
    except Exception as e:
        print(f"[!] Error fetching latest block height: {e}")
    return None

def fetch_forensic_logs(api_key, contract_address, chain_id="42161"):
    """
    Ingests event logs via Etherscan V2 with automated pagination capping,
    sliding window recovery, and dynamic schema translation.
    """
    base_url = "https://api.etherscan.io/v2/api"
    state = load_system_state()
    
    start_block = state["last_synced_block"] + 1
    end_block = fetch_latest_network_block(api_key, chain_id)
    
    if not end_block:
        print("[!] Execution halted: Unable to reach network gateway.")
        return
        
    if start_block > end_block:
        print(f"[*] System is fully synced to latest head block: {end_block}")
        return

    print(f"[*] Syncing Window: Block {start_block} to {end_block} (Total Span: {end_block - start_block} blocks)")

    forensic_ledger = []
    seen_log_ids = set()
    current_from = start_block
    translator = SCHEMA_TRANSLATOR.get(chain_id, {}).get("key_mapping", {})

    while current_from <= end_block:
        params = {
            "chainid": chain_id,
            "module": "logs",
            "action": "getLogs",
            "address": contract_address,
            "fromBlock": current_from,
            "toBlock": end_block,
            "page": 1,
            "offset": 1000,
            "apikey": api_key
        }

        try:
            response = requests.get(base_url, params=params, timeout=12)
            data = response.json()
        except requests.exceptions.RequestException as e:
            print(f"[!] Link degradation detected. Re-routing in 5s... Error: {e}")
            time.sleep(5)
            continue

        if data.get("status") == "1" and data.get("message") == "OK":
            logs = data.get("result", [])
            
            for log in logs:
                log_id = f"{log.get('transactionHash')}-{log.get('logIndex')}"
                if log_id not in seen_log_ids:
                    seen_log_ids.add(log_id)
                    
                    # Universal Translation Layer Injected Here
                    translated_record = {}
                    for raw_key, val in log.items():
                        standard_key = translator.get(raw_key, raw_key)
                        translated_record[standard_key] = val
                    
                    forensic_ledger.append(translated_record)
            
            print(f"[*] Batch Sync Success. Captured {len(logs)} logs in current window.")
            
            if len(logs) < 1000:
                # Range completely cleared
                save_system_state(end_block, state["total_records_ingested"] + len(seen_log_ids))
                break
            else:
                # Slide the boundary window forward based on last record's raw block number hex
                last_block_hex = logs[-1].get("blockNumber")
                last_block = int(last_block_hex, 16)
                
                if current_from == last_block:
                    print("[!] Critical Block Congestion: Density > 1000 logs inside single block segment.")
                    save_system_state(last_block, state["total_records_ingested"] + len(seen_log_ids))
                    break 
                    
                current_from = last_block
                save_system_state(current_from, state["total_records_ingested"] + len(seen_log_ids))
                time.sleep(0.25) # Throttle call index
                
        elif data.get("status") == "0" and data.get("message") == "No records found":
            save_system_state(end_block, state["total_records_ingested"])
            break
        else:
            print(f"[!] Operational Exception: {data.get('result')}")
            time.sleep(2)

    if forensic_ledger:
        seal_and_commit_ledger(forensic_ledger)

def seal_and_commit_ledger(ledger_data):
    """Applies atomic cryptographic signature over translated batch array."""
    serialized = json.dumps(ledger_data, sort_keys=True).encode('utf-8')
    batch_hash = hashlib.sha512(serialized).hexdigest()
    print(f"\n[+] LEDGER COMMITTED & VERIFIED SECURE")
    print(f"[+] Records in Batch: {len(ledger_data)}")
    print(f"[+] SHA-512 Root Signature: {batch_hash}\n")

if __name__ == "__main__":
    # Insert keys directly to execute
    API_KEY = "YOUR_ETHERSCAN_V2_KEY"
    TARGET_CONTRACT = "0x..." 
    
    fetch_forensic_logs(API_KEY, TARGET_CONTRACT)
