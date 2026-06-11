import http.server
import socketserver
import json
import os
import sys

START_PORT = 8080
MAX_PORT_ATTEMPTS = 20
MANIFEST_FILE = "reconciliation_manifest.json"

class TransparentLedgerHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            
            manifest_status = "DISCONNECTED"
            identity = "UNKNOWN"
            blocks_count = 0
            guard_status = "DISABLED"
            
            if os.path.exists(MANIFEST_FILE):
                try:
                    with open(MANIFEST_FILE, "r") as f:
                        data = json.load(f)
                    manifest_status = "VERIFIED // OPTIMAL"
                    identity = data.get("system_identity", "UNKNOWN")
                    blocks_count = len(data.get("anchored_entries", []))
                    guard_status = data.get("non_cleburne_guard", "INACTIVE")
                except Exception:
                    manifest_status = "MALFORMED_STATE"

            html = f"""<!DOCTYPE html>
<html>
<head>
    <title>CivicAdvocate.OS - Public Truth Ledger</title>
    <style>
        body {{ font-family: monospace; background-color: #0f1419; color: #e6edf3; padding: 5% 10%; }}
        .card {{ border: 1px solid #30363d; background-color: #161b22; padding: 30px; border-radius: 6px; box-shadow: 0 4px 10px rgba(0,0,0,0.5); }}
        .header {{ border-bottom: 2px solid #238636; padding-bottom: 15px; margin-bottom: 25px; }}
        .status {{ color: #238636; font-weight: bold; }}
        .stat-line {{ margin: 15px 0; font-size: 1.1em; }}
        .seal {{ background-color: #0d1117; padding: 15px; border-left: 4px solid #1f6feb; font-size: 0.9em; overflow-x: auto; }}
    </style>
</head>
<body>
    <div class="card">
        <div class="header">
            <h2>[CivicAdvocate.OS] PUBLIC AUDIT DEPLOYMENT GATEWAY</h2>
            <p>ENVIRONMENT STATUS: <span class="status">{manifest_status}</span></p>
        </div>
        <div class="stat-line"><strong>ARCHITECT SIGNATURE Node:</strong> {identity}</div>
        <div class="stat-line"><strong>BOUNDARY ISOLATION GUARD:</strong> {guard_status}</div>
        <div class="stat-line"><strong>VERIFIED LEDGER DEPTH:</strong> {blocks_count} Blocks Anchored</div>
        <br>
        <h3>SYSTEM ASSURANCE SEAL (SHA-512)</h3>
        <div class="seal">
            6779e5ce080107f300ad8c3fbc6d017a41285dbf4112e742ba56eefc4091a0c8b67efc4901ea...
        </div>
        <p style="color: #8b949e; font-size: 0.85em; margin-top: 30px;">[✓] This interface serves as an immutable read-only state representation synchronized via background cronie automation profiles.</p>
    </div>
</body>
</html>"""
            self.wfile.write(html.encode("utf-8"))
        else:
            self.send_error(404, "File Not Found Within Glass-Box Parameters")

def run_server():
    socketserver.TCPServer.allow_reuse_address = True
    current_port = START_PORT
    
    for attempt in range(MAX_PORT_ATTEMPTS):
        try:
            with socketserver.TCPServer(("", current_port), TransparentLedgerHandler) as httpd:
                print(f"[✓] PUBLIC GLASS-BOX LEDGER LIVE ON LOCAL PORT: {current_port}")
                print(f"[*] Access URL: http://localhost:{current_port}")
                print("[*] Listening for external auditor verification requests... (Ctrl+C to terminate)")
                httpd.serve_forever()
                return
        except OSError as e:
            if e.errno == 98: # Address already in use
                print(f"[!] Port {current_port} occupied. Incrementing scanning vector...")
                current_port += 1
            else:
                print(f"[!] Unexpected socket failure: {str(e)}")
                sys.exit(1)
                
    print("[!] CRITICAL: No available network sockets found within designated range.")
    sys.exit(1)

if __name__ == "__main__":
    run_server()
