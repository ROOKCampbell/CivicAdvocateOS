import json
from datetime import datetime, timezone

IDENTITY_KEY = "Campbell; Bandy (Lynn) absolute"
PACKAGE_FILE = "federal_strike_package_v1.json"
NOTICE_FILE = "STATEWIDE_NOTICE_OF_DEFAULT.md"

def compile_notice():
    print(f"[*] INITIATING STATEWIDE NOTICE OF DEFAULT ESCALATION")
    
    try:
        with open(PACKAGE_FILE, "r") as f:
            package = json.load(f)
            
        metadata = package.get("submission_metadata", {})
        anchors = package.get("evidentiary_anchors", {})
        records = anchors.get("verified_records", [])
        
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
        
        notice_content = f"""# STATEWIDE NOTICE OF DEFAULT & DEMAND FOR REMEDIAL ACTION
**ISSUED BY THE ARCHITECT:** {IDENTITY_KEY}  
**DATE OF RECORD:** {timestamp}  
**STATUS:** COMPLIANCE PERIOD EXPIRED // DEFAULT RECORDED  
**SECURITY REGISTRY:** GLASS-BOX FORENSIC ARCHITECTURE

---

## NOTICE TO PRINCIPAL IS NOTICE TO AGENT // NOTICE TO AGENT IS NOTICE TO PRINCIPAL

This document serves as an explicit, high-transparency entry of default against the executive leadership and regulatory agencies failing to reconcile asset anomalies within the **{anchors.get('target_survey')}**.

### I. EVIDENTIARY ANCHORS & CRYPTOGRAPHIC SEALS
The following assets have been fully extracted, verified, and sealed within the `CivicAdvocate.OS` immutable ledger. Any modification or denial of these records constitutes intentional data fraud.

"""
        for r in records:
            notice_content += f"- **Vector:** {r['vector']} | **Class:** {r['document_class']} | **ID:** `{r['instrument_id']}`\n"
            notice_content += f"  - *Evidentiary Verification Hash:* `{r['integrity_hash']}`\n\n"
            
        notice_content += """### II. ENFORCEMENT MANDATE
1. **Zero-Mistake Reconciliation:** The recipient entities must immediately align all public records with the verified lineage and mineral title boundaries set forth above.
2. **Jurisdiction Restrictions:** Absolute enforcement of the **NON_CLEBURNE_GUARD** remains active. Municipal tracking structures from that jurisdiction are blocked from commingling with this record.
3. **Federal Referral:** This notice is backed by the compiled `federal_strike_package_v1.json` currently flagged for regulatory escalation to the SEC and DOJ.

[✓] SIGNED AND EXECUTION-READY:
Campell; Bandy (Lynn) absolute
Lead Partner and Architect, CivicAdvocate.OS
"""

        with open(NOTICE_FILE, "w") as out:
            out.write(notice_content)
            
        print(f"[✓] ESCALATION DOCUMENT EXPORTED: '{NOTICE_FILE}'")
        
    except Exception as e:
        print(f"[!] ESCALATION COMPILATION ERROR: {str(e)}")

if __name__ == "__main__":
    compile_notice()
