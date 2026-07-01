import asyncio
import yaml
import time
import hashlib
import os

def load_config():
    with open('config.yaml', 'r') as f:
        return yaml.safe_load(f)

class IntegrityEngine:
    def get_file_hash(self, filepath):
        if not os.path.exists(filepath): return None
        sha512 = hashlib.sha512()
        with open(filepath, 'rb') as f:
            while chunk := f.read(8192):
                sha512.update(chunk)
        return sha512.hexdigest()

    def verify_baseline(self):
        # Nodes to audit
        nodes = ["bandy_abstract_544_true_production.csv", "bandy_survey_tenure.csv"]
        for node in nodes:
            if not os.path.exists(node):
                print(f"[!] ALERT: Missing Node: {node}")
                return False
        return True

async def run_heartbeat():
    config = load_config()
    engine = IntegrityEngine()
    print("[*] Heartbeat initialized. MULTI-NODE AUDITING ENABLED.")
    while config['persistence_settings']['autonomous_mode'] == "ENABLED":
        status = engine.verify_baseline()
        print(f"[*] Audit Cycle Complete. Baseline integrity: {status} at {time.ctime()}")
        await asyncio.sleep(config['persistence_settings']['heartbeat_interval'])

if __name__ == "__main__":
    asyncio.run(run_heartbeat())
