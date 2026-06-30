import os
import json
import logging
from audit_watcher import start_watchdog

class ComplianceEngine:
    def __init__(self, target_path):
        self.target_path = target_path
        self.log_file = os.path.join(target_path, "registry/audit_log.json")
        # Initialize Watchdog
        start_watchdog("audit_scope.json")

    def run_monitor(self):
        if os.path.exists(self.log_file):
            with open(self.log_file, 'r') as f:
                data = json.load(f)
                logging.info(f"Engine Monitoring Active: {self.target_path}")
        else:
            logging.error(f"Log file not found: {self.log_file}")

if __name__ == "__main__":
    engine = ComplianceEngine(".")
    engine.run_monitor()
