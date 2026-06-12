import time
import random

def monitor_entities():
    entities = ["ALPHA", "BETA"]
    print("[SYS] Real-time surveillance active: Monitoring for liquidation signatures...")
    
    # Simulate tracking of asset movement across registries
    for _ in range(5):
        activity = random.choice(["NONE", "LIQUIDATION_ALERT", "ASSET_TRANSFER"])
        if activity != "NONE":
            print(f"[ALERT] {random.choice(entities)} detected performing: {activity}")
        time.sleep(2)

monitor_entities()
