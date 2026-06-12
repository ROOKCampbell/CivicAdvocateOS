import hashlib
import time
import requests
from pathlib import Path

TARGET_URL = "https://web.archive.org/web/20260611000000/https://www.jocotx.org/"
STORAGE_PATH = Path("./forensic_log")
HASH_FILE = STORAGE_PATH / "state_anchor.sha512"

def ensure_directory():
    if not STORAGE_PATH.exists():
        STORAGE_PATH.mkdir(parents=True, exist_ok=True)

def get_snapshot():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive'
    }
    response = requests.get(TARGET_URL, headers=headers, timeout=15)
    return hashlib.sha512(response.content).hexdigest()

def run_monitor():
    ensure_directory()
    print(f"[*] Initializing Protocol Zero Surveillance on {TARGET_URL}")
    try:
        current_hash = get_snapshot()
        with open(HASH_FILE, "w") as f:
            f.write(current_hash)
        print(f"[*] Initial anchor secured.")
    except Exception as e:
        print(f"[E] Initial acquisition failed: {e}")
        return
    while True:
        time.sleep(300)
        try:
            new_hash = get_snapshot()
            if new_hash != current_hash:
                print(f"[!] ALERT: State change detected")
                current_hash = new_hash
                with open(HASH_FILE, "w") as f:
                    f.write(current_hash)
        except Exception as e:
            print(f"[E] Error during polling: {e}")

if __name__ == "__main__":
    run_monitor()
