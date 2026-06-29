import hashlib
import json
import time
import os

class CivicAuditorAgent:
    def __init__(self, agent_id="AUDITOR_01"):
        self.agent_id = agent_id

    def audit_event(self, action, payload, status):
        entry = {
            "agent_id": self.agent_id,
            "timestamp": time.time(),
            "action": action,
            "payload": payload,
            "status": status
        }
        entry["hash"] = hashlib.sha512(json.dumps(entry, sort_keys=True).encode()).hexdigest()
        
        with open("integrity_vault.log", "a") as f:
            f.write(json.dumps(entry) + "\n")
        print(f"Audit Entry Created: {entry['hash']}")

if __name__ == "__main__":
    agent = CivicAuditorAgent()
    agent.audit_event("SYSTEM_INIT", {"status": "ACTIVE"}, "SUCCESS")
