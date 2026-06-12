from scapy.all import sniff, IP, TCP
import datetime

# Configuration: Target the synchronization heartbeat
# Adjust 'eth0' or 'wlan0' based on your active interface (check with 'ip a')
INTERFACE = "wlan0" 

def packet_callback(packet):
    if packet.haslayer(IP) and packet[IP].dst != "127.0.0.1":
        # Capture payload of outbound synchronization packets
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("registry_tap.log", "a") as f:
            f.write(f"\n[{timestamp}] Data Packet Detected:\n")
            f.write(f"Src: {packet[IP].src} -> Dst: {packet[IP].dst}\n")
            f.write(f"Payload: {str(packet.payload)}\n")
            f.write("-" * 30 + "\n")
        print(f"[{timestamp}] Transmission captured from {packet[IP].src}")

print("[SYS] Interceptor armed. Monitoring for 1:00 AM sync...")
# Filtering for TCP traffic associated with registry egress
sniff(iface=INTERFACE, filter="tcp", prn=packet_callback, store=0)
