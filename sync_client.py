import socket
def sync(peer_ip, port=5000):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((peer_ip, port))
    client.sendall(b'SYNC_REQUEST')
    data = client.recv(40960)
    with open("manifest.json", "w") as f:
        f.write(data.decode())
    print("[*] SYNC COMPLETE.")
    client.close()
sync("127.0.0.1")
