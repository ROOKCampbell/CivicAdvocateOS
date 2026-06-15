import socket, json

def start_server(port=5000):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', port))
    server.listen(5)
    print(f"[*] Node listening on port {port}...")
    
    while True:
        conn, addr = server.accept()
        request = conn.recv(1024).decode()
        if request == 'SYNC_REQUEST':
            with open("manifest.json", "r") as f:
                data = f.read()
            conn.sendall(data.encode())
            print(f"[*] Sent ledger to {addr}")
        conn.close()

if __name__ == "__main__":
    start_server()
