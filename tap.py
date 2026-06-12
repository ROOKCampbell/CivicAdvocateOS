import sys
from scapy.all import Ether, IP

print("[SYS] Listening for sync stream via stdin...")
for line in sys.stdin:
    print(f"[PACKET DETECTED] {line.strip()}")
