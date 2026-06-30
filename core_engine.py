import os
import json

class ComplianceEngine:
    def __init__(self, target_path):
        self.target_path = target_path
        self.log_file = os.path.join(target_path, "registry/audit_log.json")

    def run_monitor(self):
        if os.path.exists(self.log_file):
            with open(self.log_file, 'r') as f:
                data = json.load(f)
                print(f"Engine Monitoring: {self.target_path}")
        else:
            print(f"Log file not found: {self.log_file}")

if __name__ == "__main__":
    # Initialize with current directory for testing
    engine = ComplianceEngine(".")
    engine.run_monitor()
