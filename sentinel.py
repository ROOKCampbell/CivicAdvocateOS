import hashlib
import time
from pathlib import Path

# Point to your manually saved forensic file
LOCAL_FILE = Path("./current_record.html")
STORAGE_PATH = Path("./forensic_log")
HASH_FILE = STORAGE_PATH / "state_anchor.sha512"

def get_local_hash():
    return hashlib.sha512(LOCAL_FILE.read_bytes()).hexdigest()

def run_monitor():
    if not STORAGE_PATH.exists(): STORAGE_PATH.mkdir(parents=True, exist_ok=True)
    
    if not LOCAL_FILE.exists():
        print("[E] Evidence file not found. Place record in the OS directory.")
        return

    current_hash = get_local_hash()
    with open(HASH_FILE, "w") as f: f.write(current_hash)
    print(f"[*] Local Anchor Secured: {current_hash[:16]}...")
    
    while True:
        time.sleep(60)
        new_hash = get_local_hash()
        if new_hash != current_hash:
            print(f"[!] ALERT: Local state change detected.")
            current_hash = new_hash
            with open(HASH_FILE, "w") as f: f.write(current_hash)

if __name__ == "__main__":
    run_monitor()
