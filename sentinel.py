import hashlib, os, time, json

BASELINE_FILE = "/data/data/com.termux/files/home/CivicAdvocate.OS/truth_mandate_baseline.json"
STRIKE_PACKAGE_DIR = "./strike_packages"

def get_hash(path):
    sha512 = hashlib.sha512()
    with open(path, "rb") as f:
        while chunk := f.read(65536): sha512.update(chunk)
    return sha512.hexdigest()

def issue_federal_strike(node_path):
    if not os.path.exists(STRIKE_PACKAGE_DIR): os.makedirs(STRIKE_PACKAGE_DIR)
    report = {
        "event": "INTEGRITY_BREACH",
        "node": node_path,
        "status": "PENDING_FEDERAL_REFERRAL",
        "timestamp": time.ctime()
    }
    report_path = f"{STRIKE_PACKAGE_DIR}/strike_{int(time.time())}.json"
    with open(report_path, "w") as f: json.dump(report, f, indent=4)
    print(f"Strike Package generated for: {node_path}")

def run_sentinel():
    print("Truth Mandate Sentinel: Active")
    with open(BASELINE_FILE, "r") as f: baseline = json.load(f)
    while True:
        for path, original_hash in baseline["nodes"].items():
            if not os.path.exists(path) or get_hash(path) != original_hash:
                issue_federal_strike(path)
        time.sleep(60)

if __name__ == "__main__":
    run_sentinel()
