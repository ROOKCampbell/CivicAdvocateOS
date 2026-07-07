#!/usr/bin/env python3
# CivicAdvocate.OS | Writ of Mandamus Template Generator
# Workflow: Overview -> Code -> Implementation

import os
import sys
import json
import urllib.request
import hmac
import hashlib
from datetime import datetime, timezone

PRIVATE_KEY = os.getenv("ARCHITECT_PRIVATE_KEY")
NODE_ADDRESS = os.getenv("NODE_ADDRESS")
MANDAMUS_OUT = "/data/data/com.termux/files/home/civicadvocate/ledger/mainnet/MANDAMUS_PETITION_TEMPLATE.txt"

def build_mandamus_petition():
    print("=== [CivicAdvocate.OS Writ of Mandamus Generator] ===")
    if not PRIVATE_KEY or not NODE_ADDRESS:
        print("[-] Error: Active cryptographic credentials missing from shell environment.")
        sys.exit(1)

    # Hardcoded Case Reality Mapping Data Fields
    relator_name = "BRANDON LYNN CAMPBELL"
    survey_description = "THE SILAS ELBERT BANDY SURVEY, ABSTRACT 544 (391.45 ACRES)"
    comptroller_claim_id = "27440378"
    probate_cause_no = "P195406969"

    template = f"""IN THE DISTRICT COURT OF TEXAS
JUDICIAL DISTRICT

EX REL. {relator_name},
Relator

v.

TEXAS UNCLAIMED PROPERTY DIVISION &
JOHNSON COUNTY CLERK RECORD CUSTODIANS,
Respondents

========================================================================
             PETITION FOR WRIT OF MANDAMUS - STATE MANDATE WRIT
========================================================================

TO THE HONORABLE JUDGE OF SAID COURT:

Comes now {relator_name}, Relator, proceeding pro se, and files this Petition for Writ of Mandamus compelling Respondents to execute their mandatory ministerial, non-discretionary statutory duties, and would respectfully show the Court the following:

I. STATEMENT OF RELEVANT CASE FOOTPRINT
1. Relator holds verified ancestral title and interest to {survey_description}, rooted securely under historic land patents and documented forensic heirship pathways.
2. Under Cause No. {probate_cause_no} within the probate records of Johnson County, and active Comptroller Unclaimed Property Claim ID {comptroller_claim_id}, Relator has asserted formal demands for the production of missing registry books and the release of liquidated suspense funds totaling $128,603.70+.
3. Respondents have failed or refused to supply standard access or perform final clerical closures, citing internal portal errors, title disputes, and administrative delays.

II. GROUNDS FOR MANDAMUS RELIEF
1. Relator has a clear legal right to the ministerial performance of the acts demanded. Relator possesses no other adequate legal remedy at law to secure immediate document access.
2. The duties of Respondents to accurately preserve public dockets and disburse un-disputed ancestral assets are strictly ministerial, absolute, and non-discretionary under Texas law.

PRAYER
Relator respectfully requests this Court to issue a Writ of Mandamus commanding Respondents to immediately produce all historic pre-1881 county registry volumes related to Abstract 544, conclude the administrative audit of pending Claim ID {comptroller_claim_id}, and grant such other relief to which Relator may be justly entitled.

Respectfully submitted,
By: _______________________________
    {relator_name}, Relator Pro Se
    Sovereign Identity Key Anchor: {NODE_ADDRESS}
"""

    with open(MANDAMUS_OUT, 'w') as f:
        f.write(template)
    os.chmod(MANDAMUS_OUT, 0o400) # Lock access posture to user read-only
    print(f"[+] Production template successfully structured and locked to path:\n    {MANDAMUS_OUT}")

    # Build ledger tracking payload block
    payload = {
        "network": "mainnet",
        "docket": "ABSTRACT-544-LEGAL",
        "action": "MANDAMUS_TEMPLATE_COMPILED",
        "file_hash": hashlib.sha256(template.encode('utf-8')).hexdigest()
    }

    serialized = json.dumps(payload, sort_keys=True).encode('utf-8')
    sig = hmac.new(bytes.fromhex(PRIVATE_KEY), serialized, hashlib.sha256).hexdigest()
    
    package = {"payload": payload, "signer": NODE_ADDRESS, "signature": sig}
    req = urllib.request.Request(
        'http://localhost:8080/v1/ledger/append',
        data=json.dumps(package).encode('utf-8'),
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    try:
        with urllib.request.urlopen(req) as res:
            print(f"[+] Legal State Flush Complete: {res.read().decode('utf-8').strip()}")
    except Exception as e:
        print(f"[-] Failed auto-committing legal flush block: {e}")

if __name__ == "__main__":
    build_mandamus_petition()
