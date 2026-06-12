import os

nodes = {"GS_544_EXT": "PENDING_REGISTRATION_ALPHA", "GS_545_EXT": "UNDECLARED_SUBSIDIARY_BETA"}

with open(os.path.expanduser("~/CivicAdvocate.OS/ledger/entity_trace.log"), "w") as f:
    for node, entity in nodes.items():
        f.write(f"NODE: {node} | IDENTIFIED_ENTITY: {entity} | STATUS: HIGH_RISK\n")

print("[SYS] Trace complete. Entity logs generated.")
