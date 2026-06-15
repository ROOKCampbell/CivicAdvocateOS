from flask import Flask, jsonify, request
import os

app = Flask(__name__)

# Security Configuration
API_KEY = "your-secure-secret-key"
LEDGER_PATH = "/data/data/com.termux/files/home/CivicAdvocate.OS/ledger/audit_trail.log"

def check_auth():
    """Verify the X-API-KEY header."""
    key = request.headers.get("X-API-KEY")
    return key == API_KEY

@app.route('/audit/latest', methods=['GET'])
def get_latest_audit():
    if not os.path.exists(LEDGER_PATH):
        return jsonify({"error": "Ledger file not found"}), 404
    
    with open(LEDGER_PATH, 'r') as f:
        lines = f.readlines()
        
    return jsonify({
        "status": "success",
        "entries": [line.strip() for line in lines[-5:]]
    })

@app.route('/audit/submit', methods=['POST'])
def submit_audit_entry():
    if not check_auth():
        return jsonify({"status": "error", "message": "Unauthorized"}), 401
    
    data = request.json
    entry = data.get("entry")
    
    if not entry:
        return jsonify({"status": "error", "message": "No entry provided"}), 400
    
    with open(LEDGER_PATH, 'a') as f:
        f.write(f"{entry}\n")
        
    return jsonify({"status": "success", "message": "Entry committed to ledger"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
