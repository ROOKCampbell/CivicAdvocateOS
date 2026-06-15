import json
with open("manifest.json", "r") as f:
    blocks = json.load(f)
proposals = [b for b in blocks if b.get('type') == 'PROPOSAL']
for p in proposals:
    votes = [b for b in blocks if b.get('type') == 'VOTE' and f"Proposal {p['id']}" in b['data']]
    yay = sum(1 for v in votes if "YAY" in v['data'])
    print(f"Law {p['id']}: '{p['data']}' | Votes: {yay}")
