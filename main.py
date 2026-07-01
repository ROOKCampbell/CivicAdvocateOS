import asyncio
import yaml
import time
from integrity_engine import IntegrityEngine

async def run_heartbeat():
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    engine = IntegrityEngine()
    
    print("[*] Heartbeat initialized. Monitoring enabled.")
    while config['persistence_settings']['autonomous_mode'] == "ENABLED":
        if not engine.verify_baseline():
            print("[!!!] ANOMALY DETECTED: Triggering remediation protocol.")
        else:
            print(f"[*] Integrity verified at {time.ctime()}")
        
        await asyncio.sleep(config['persistence_settings']['heartbeat_interval'])

if __name__ == "__main__":
    asyncio.run(run_heartbeat())
