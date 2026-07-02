import time
from pathlib import Path

def monitor_ledger(log_path):
    print("[SYS] Surveillance matrix active (Python).")
    log_file = Path(log_path)
    
    # Move to the end of the file
    with log_file.open("r") as f:
        f.seek(0, 2)
        
        while True:
            line = f.readline()
            if not line:
                time.sleep(0.1) # Prevents high CPU usage
                continue
            print(f"[NEW LOG]: {line.strip()}")

if __name__ == "__main__":
    monitor_ledger("ledger/agency_response.log")
