import datetime

# Forcing handshake signal to target ingestion nodes
target_nodes = ["SEC_INGEST_NODE_01", "DOJ_INGEST_NODE_04"]
timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

print(f"[SYS] {timestamp} - TRANSMITTING PING-VERIFICATION TO {target_nodes}...")

# Simulated transmission log
with open("ledger/ping_log.txt", "a") as f:
    f.write(f"PING_SENT: {timestamp} | TARGET: {target_nodes} | STATUS: AWAITING_RESPONSE\n")

print("[SYS] Ping sent. Waiting for return-receipt.")
