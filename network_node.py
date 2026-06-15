import socket, json, threading, os
from ledger_utils import validate_single_block

def update_manifest(new_block):
    # Load local state
    if os.path.exists("manifest.json"):
        with open("manifest.json", "r") as f:
            blocks = json.load(f)
    else:
        blocks = []

    # Consensus Rule: Only append if it extends the chain
    if not blocks or new_block['id'] > blocks[-1]['id']:
        blocks.append(new_block)
        with open("manifest.json", "w") as f:
            json.dump(blocks, f, indent=4)
        print(f"[*] CONSENSUS: BLOCK {new_block['id']} ACCEPTED AS NEW TRUTH.")
    else:
        print(f"[*] CONSENSUS: REJECTED STALE OR CONFLICTING DATA.")

def handle_peer(conn):
    data = conn.recv(4096)
    if data:
        block = json.loads(data.decode())
        print(f"[*] RECEIVED BLOCK {block['id']} FROM PEER.")
        update_manifest(block)
    conn.close()

def start_node(port=5000):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', port))
    server.listen(5)
    print(f"[*] UNIVERSAL ADVOCATE P2P NODE ONLINE ON PORT {port}")
    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_peer, args=(conn,)).start()

if __name__ == "__main__":
    start_node()
