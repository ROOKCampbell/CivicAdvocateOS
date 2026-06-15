import socket

# Configuration for Public Binding
HOST = '0.0.0.0'
PORT = 5000

# Initialize Socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen(5)

print(f"[*] Node active and listening on {HOST}:{PORT}...")

while True:
    conn, addr = server.accept()
    print(f"[+] Connection received from {addr}")
    conn.close()
