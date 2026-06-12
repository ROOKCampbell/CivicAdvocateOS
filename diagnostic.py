import socket

def run_diagnostic():
    target_ip = "127.0.0.1"
    target_ports = [80, 443, 3306]
    print("[SYS] Diagnostic active: Probing registry heartbeat...")
    for port in target_ports:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            if s.connect_ex((target_ip, port)) == 0:
                print(f"[FOUND] Port {port} responding.")
            else:
                print(f"[STATUS] Port {port} silent.")

if __name__ == "__main__":
    run_diagnostic()
