import os
import hashlib

def get_integrity_status(ledger_file='forensic_ledger.sha512'):
    if not os.path.exists(ledger_file):
        return "NO LEDGER FOUND", "N/A", "danger"
    
    verified_entries = []
    has_mismatch = False
    
    with open(ledger_file, 'r') as f:
        lines = f.readlines()
        if not lines:
            return "EMPTY LEDGER", "N/A", "warning"
            
    # Check all entries but grab the last one for high-level summary
    for line in lines:
        parts = line.strip().split(' | ')
        if len(parts) != 3:
            continue
        timestamp, filename, anchored_hash = parts
        
        # Verify current file hash against anchor
        if os.path.exists(filename):
            sha512 = hashlib.sha512()
            with open(filename, 'rb') as f_in:
                while chunk := f_in.read(65536):
                    sha512.update(chunk)
            current_hash = sha512.hexdigest()
            
            if current_hash != anchored_hash:
                has_mismatch = True
        else:
            has_mismatch = True
            
    latest_ts, latest_file, latest_hash = lines[-1].strip().split(' | ')
    
    if has_mismatch:
        return "CRITICAL MISMATCH / DRIFT DETECTED", latest_hash, "danger"
    return "VERIFIED / SYSTEM NOMINAL", latest_hash, "success"

def compile_html():
    status, final_hash, context_class = get_integrity_status()
    
    # Mapping Bootstrap alert colors
    bg_color = "#d4edda" if context_class == "success" else "#f8d7da"
    text_color = "#155724" if context_class == "success" else "#721c24"
    border_color = "#c3e6cb" if context_class == "success" else "#f5c6cb"

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>CivicAdvocate.OS Transparency Dashboard</title>
    <style>
        body {{ font-family: monospace; background-color: #121212; color: #e0e0e0; padding: 20px; }}
        .container {{ max-width: 900px; margin: 0 auto; }}
        .card {{ background-color: #1e1e1e; border: 1px solid #333; padding: 20px; border-radius: 5px; }}
        .badge {{ padding: 10px; border-radius: 3px; display: inline-block; font-weight: bold;
                  background-color: {bg_color}; color: {text_color}; border: 1px solid {border_color}; }}
        .hash-box {{ background-color: #000; padding: 10px; border: 1px solid #444; overflow-x: auto; color: #00ff00; }}
        h1, h3 {{ color: #ffffff; }}
        hr {{ border: 0; border-top: 1px solid #333; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>CivicAdvocate.OS Real-Time Audit Ledger</h1>
        <p>System Region Baseline: Cleburne, TX</p>
        <hr>
        <div class="card">
            <h3>System Status</h3>
            <div class="badge">{status}</div>
            
            <h3>Active Root Cryptographic Anchor (SHA-512)</h3>
            <div class="hash-box">{final_hash}</div>
            
            <p style="font-size: 0.8em; color: #888; margin-top: 15px;">
                Verification pipeline executed natively inside [Advocate_Env] sandbox execution parameters.
            </p>
        </div>
    </div>
</body>
</html>
"""
    with open("transparency_dashboard.html", "w") as f:
        f.write(html_content)
    print("[DASHBOARD] transparency_dashboard.html updated successfully with live ledger state.")

if __name__ == "__main__":
    compile_html()
