import requests
import time
import hashlib
import json

def fetch_forensic_logs(api_key, contract_address, start_block, end_block, chain_id="42161"):
    """
    Ingests event logs via Etherscan V2, bypassing the 1,000-record cap.
    Defaulting to Arbitrum Mainnet (42161). For Sepolia drift monitoring, use 421614.
    """
    base_url = "https://api.etherscan.io/v2/api"
    forensic_ledger = []
    seen_log_ids = set()
    current_from = start_block

    print(f"Initializing V2 API Sync | Chain ID: {chain_id} | Range: {start_block} - {end_block}")

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
            response = requests.get(base_url, params=params, timeout=10)
            data = response.json()
        except requests.exceptions.RequestException as e:
            print(f"[!] Network disruption. Retrying in 5 seconds... Error: {e}")
            time.sleep(5)
            continue

        if data.get("status") == "1" and data.get("message") == "OK":
            logs = data.get("result", [])
            
            # Deduplication pass to ensure forensic purity
            for log in logs:
                log_id = f"{log.get('transactionHash')}-{log.get('logIndex')}"
                if log_id not in seen_log_ids:
                    seen_log_ids.add(log_id)
                    forensic_ledger.append(log)
            
            if len(logs) < 1000:
                # Full block range successfully secured
                break
            else:
                last_block_hex = logs[-1].get("blockNumber")
                last_block = int(last_block_hex, 16)
                
                # Lock the pointer to the last block to prevent dropping intra-block logs.
                if current_from == last_block:
                    # Failsafe for the extreme edge case where a single block contains >1,000 logs.
                    print("[!] WARNING: Cap exceeded within a single block. Manual intervention required.")
                    break 
                    
                current_from = last_block
                
                # Throttle to comply with the Free tier 5 calls/sec rate limit
                time.sleep(0.25) 
                
        elif data.get("status") == "0" and data.get("message") == "No records found":
            break
        else:
            print(f"[!] API Exception: {data.get('result')}")
            time.sleep(2)

    return forensic_ledger

def seal_ledger(ledger_data):
    """Locks the ingested payload with an immutable SHA-512 verification hash."""
    encoded_data = json.dumps(ledger_data, sort_keys=True).encode('utf-8')
    return hashlib.sha512(encoded_data).hexdigest()

# Execution Harness
# api_key = "YOUR_ETHERSCAN_API_KEY"
# target_address = "0x..." 
# ingested_logs = fetch_forensic_logs(api_key, target_address, 12000000, 12005000)
# genesis_hash = seal_ledger(ingested_logs)
# print(f"Ledger secured. SHA-512 Root: {genesis_hash}")
