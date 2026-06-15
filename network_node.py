import socket, json, threading, os
from ledger_utils import validate_single_block

def handle_peer(conn):
    data = conn.recv(4096)
    if not data: return
    
    # SYNC PROTOCOL: Return manifest to requester
    if data.strip() == b'SYNC_REQUEST':
        with open("manifest.json", "r") as f:
            conn.sendall(f.read().encode())
    else:
        block = json.loads(data.decode())
        # Add to manifest logic...
        print(f"[*] RECEIVED BLOCK {block['id']}")
    conn.close()

def start_node(port=5000):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', port))
    server.listen(5)
    print(f"[*] SYNC-ENABLED NODE ONLINE ON PORT {port}")
    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_peer, args=(conn,)).start()

if __name__ == "__main__":
    start_node()
