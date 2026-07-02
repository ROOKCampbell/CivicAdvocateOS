from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from datetime import datetime

class AuditHandler(BaseHTTPRequestHandler):
    def log_to_file(self, data):
        # Appends the received JSON to a persistent file
        with open("audit_log.json", "a") as f:
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "payload": json.loads(data)
            }
            f.write(json.dumps(log_entry) + "\n")
            print(f"[DISK] Data saved to audit_log.json")

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Audit Server is Online.")

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        self.log_to_file(post_data)
        self.send_response(200)
        self.end_headers()

server = HTTPServer(('127.0.0.1', 5001), AuditHandler)
print("[SYS] Audit Server listening on port 5001...")
server.serve_forever()
