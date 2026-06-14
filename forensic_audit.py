import hashlib, os, json, datetime
AUDIT_LOG_DIR = "./municipal_data"
BASELINE_FILE = "/data/data/com.termux/files/home/CivicAdvocate.OS/truth_mandate_baseline.json"
def get_timestamp(): return datetime.datetime.now().isoformat()
def compute_sha512(file_path):
    sha512 = hashlib.sha512()
    with open(file_path, "rb") as f:
        while chunk := f.read(65536): sha512.update(chunk)
    return sha512.hexdigest()
def initialize_forensic_node():
    if not os.path.exists(AUDIT_LOG_DIR): os.makedirs(AUDIT_LOG_DIR)
    baseline = {"timestamp": get_timestamp(), "nodes": {}}
    for root, _, files in os.walk(AUDIT_LOG_DIR):
        for name in files:
            path = os.path.join(root, name)
            baseline["nodes"][path] = compute_sha512(path)
    with open(BASELINE_FILE, "w") as f: json.dump(baseline, f, indent=4)
    print(f"Truth Mandate baseline established at {BASELINE_FILE}")
if __name__ == "__main__": initialize_forensic_node()
