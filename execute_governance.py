import json, os

def execute_action(proposal_id, data):
    print(f"[*] THRESHOLD MET: Executing governance action for Proposal {proposal_id}...")
    # Example action: Update a system config file
    with open("system_state.json", "w") as f:
        json.dump({"active_rule": data, "status": "ENACTED"}, f)
    print("[*] SYSTEM STATE UPDATED SUCCESSFULLY.")

def check_threshold(threshold=1):
    with open("manifest.json", "r") as f:
        blocks = json.load(f)
    
    proposals = {b['id']: b['data'] for b in blocks if b.get('type') == 'PROPOSAL'}
    votes = [b for b in blocks if b.get('type') == 'VOTE']
    
    for pid, pdata in proposals.items():
        yay_count = sum(1 for v in votes if f"Proposal {pid}" in v['data'] and "YAY" in v['data'])
        if yay_count >= threshold:
            execute_action(pid, pdata)

if __name__ == "__main__":
    check_threshold()
