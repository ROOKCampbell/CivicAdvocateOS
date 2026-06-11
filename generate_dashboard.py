#!/usr/bin/env python3
import json
import os
from datetime import datetime, timezone

LEDGER_FILE = os.path.expanduser("~/truth_mandate/ledger/mission_ledger.jsonl")
DASHBOARD_FILE = os.path.expanduser("~/CivicAdvocate.OS/transparency_dashboard.html")

def build_dashboard():
    records = []
    if not os.path.exists(LEDGER_FILE):
        return

    with open(LEDGER_FILE, 'r') as f:
        for line in f:
            try:
                records.append(json.loads(line))
            except:
                continue

    # Take latest 10 for dashboard view
    latest = records[-10:] if len(records) > 10 else records
    latest.reverse()

    html = f"""
    <html>
    <head>
        <title>CivicAdvocate.OS - Forensic Transparency Dashboard</title>
        <style>
            body {{ font-family: monospace; background: #000; color: #0f0; padding: 20px; }}
            .card {{ border: 1px solid #0f0; padding: 15px; margin-bottom: 10px; }}
            .header {{ font-size: 1.5em; border-bottom: 2px solid #0f0; margin-bottom: 20px; }}
            .hash {{ color: #888; font-size: 0.8em; word-break: break-all; }}
            .status {{ font-weight: bold; color: #fff; }}
        </style>
    </head>
    <body>
        <div class="header">SYSTEM STATUS: ACTIVE | MANDATE: TRUTH | ASSET: ABSTRACT 544</div>
        <p>Last Update: {datetime.now(timezone.utc).isoformat()}</p>
    </body>
    </html>
    """
    
    # Simple table injection for audit records
    for r in latest:
        payload = r.get("payload_data", {})
        html += f"""
        <div class="card">
            <div>AUDIT ID: {r.get('audit_id')} | SOURCE: {r.get('intake_id')}</div>
            <div class="status">STATUS: {payload.get('commingling_alert_flag', 'CLEAR')}</div>
            <div>VARIANCE: {payload.get('variance_detected', 0)} BBLS</div>
            <div class="hash">SHA-512: {r.get('checksum')}</div>
        </div>
        """
    
    html += "</body></html>"
    
    with open(DASHBOARD_FILE, "w") as f:
        f.write(html)
    print(f"[+] Glass-Box Dashboard Generated: {DASHBOARD_FILE}")

if __name__ == "__main__":
    build_dashboard()
