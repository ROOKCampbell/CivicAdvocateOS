import json

def generate_report():
    with open("manifest.json", "r") as f:
        blocks = json.load(f)
    
    print("=== CIVIC ADVOCATE.OS: OFFICIAL AUDIT LOG ===")
    proposals = [b for b in blocks if b.get('type') == 'PROPOSAL']
    
    for p in proposals:
        votes = [b for b in blocks if b.get('type') == 'VOTE' and f"Proposal {p['id']}" in b['data']]
        yay = sum(1 for v in votes if "YAY" in v['data'])
        nay = sum(1 for v in votes if "NAY" in v['data'])
        status = "ENACTED" if yay > nay else "PENDING/REJECTED"
        print(f"Law ID {p['id']}: '{p['data']}' | Votes: YAY:{yay} NAY:{nay} | Status: {status}")

if __name__ == "__main__":
    generate_report()
