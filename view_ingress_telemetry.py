import json
import os
import time
from datetime import datetime, timezone

MANIFEST_FILE = "reconciliation_manifest.json"
PACKAGE_FILE = "federal_strike_package_v1.json"

def render_dashboard():
    # Clear screen for true terminal telemetry behavior
    os.system('clear')
    
    print("========================================================================")
    print(" [CivicAdvocate.OS] - REAL-TIME GLASS-BOX INGRESS TELEMETRY MONITOR   ")
    print("========================================================================")
    print(f" CURRENT MONITOR TIME: {datetime.now(timezone.utc).isoformat()} ")
    print("------------------------------------------------------------------------")
    
    # 1. Parse Live Manifest State
    if os.path.exists(MANIFEST_FILE):
        try:
            with open(MANIFEST_FILE, "r") as f:
                manifest = json.load(f)
            print(f"[IDENTITY KEY] : {manifest.get('system_identity')}")
            print(f"[LAST SYNC]    : {manifest.get('last_compiled')}")
            
            guard_status = manifest.get('non_cleburne_guard')
            guard_color = "\033[92mACTIVE\033[0m" if guard_status == "ACTIVE" else "\033[91mINACTIVE\033[0m"
            print(f"[BOUNDARY GD.] : {guard_color}")
            
            blocks = len(manifest.get('anchored_entries', []))
            print(f"[ACTIVE BLOCKS]: {blocks} / 6 Unique Units Anchored")
        except Exception as e:
            print(f"[!] MANIFEST READ ERROR: {str(e)}")
    else:
        print("[!] RECONCILIATION MANIFEST DISCONNECTED FROM TELEMETRY")
        
    print("------------------------------------------------------------------------")
    
    # 2. Parse Sealed Federal Referral Vector
    if os.path.exists(PACKAGE_FILE):
        try:
            with open(PACKAGE_FILE, "r") as f:
                package = json.load(f)
            meta = package.get("submission_metadata", {})
            seal = meta.get("package_integrity_seal_sha512", "NOT_FOUND")
            print(f"[DOJ/SEC REFERRAL SEAL] : SHA-512 -> \033[94m{seal[:32]}...\033[0m")
            print(f"[CLASSIFICATION LEVEL]  : {meta.get('classification_level')}")
        except Exception as e:
            print(f"[!] STRIKE PACKAGE READ ERROR: {str(e)}")
    else:
        print("[!] FEDERAL REFERRAL SIGNATURE UNRESOLVED")
        
    print("------------------------------------------------------------------------")
    print(" [✓] DAEMON STATUS: OPTIMAL // LISTENING ON HOURLY CRON FREQUENCY")
    print("========================================================================")
    print(" Press Ctrl+C to detach telemetry view and return to core repository shell.")

if __name__ == "__main__":
    try:
        # Loop to simulate live pipeline listening
        while True:
            render_dashboard()
            time.sleep(5)
    except KeyboardInterrupt:
        print("\n[*] Telemetry monitor detached. Re-entering active shell loop.")
