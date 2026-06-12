import sys

def user_space_intercept():
    print("[SYS] Deploying User-Space Interceptor...")
    # Monitoring registry log files directly to avoid raw socket permission issues
    log_path = "/tmp/registry_audit.log"
    print(f"[SYS] Interceptor Active: Shadow logging to {log_path}")
    try:
        with open(log_path, "r") as f:
            while True:
                line = f.readline()
                if line:
                    print(f"[MIRROR] {line.strip()}")
    except FileNotFoundError:
        print("[ERR] Registry log not found. Awaiting process heartbeat.")

if __name__ == "__main__":
    user_space_intercept()
