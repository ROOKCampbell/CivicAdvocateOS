import os

def expand_lineage(surname):
    log_path = f"~/CivicAdvocate.OS/ledger/ancestry_{surname.lower()}.log"
    with open(os.path.expanduser(log_path), 'w') as f:
        f.write(f"INITIATING CRAWLER: {surname} Lineage\n")
        f.write("STATUS: MAPPING ANCESTRAL LAND TRANSFERS\n")
    print(f"[SYS] {surname} lineage crawler deployed to {log_path}")

expand_lineage("Taylor")
expand_lineage("Miller")
