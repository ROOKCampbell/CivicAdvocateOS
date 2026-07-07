#!/usr/bin/env python3
# CivicAdvocate.OS | Unstructured Docket Parsing Engine
# Workflow: Overview -> Code -> Implementation

import os
import re
import sys
import json

def parse_raw_legal_text(raw_text):
    """Processes unstructured legal and case data lines into structural JSON blocks."""
    # Production extraction regular expressions
    case_pattern = re.compile(r'(?:CASE|DOCKET|MATTER)\s*(?:NO\.?|#)?\s*([A-Za-z0-9\-\:]+)', re.IGNORECASE)
    date_pattern = re.compile(r'(\d{1,2}[/\-]\d{1,2}[/\-]\d{2,4}|\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{1,2},? \d{4})', re.IGNORECASE)
    mandamus_pattern = re.compile(r'(writ of mandamus|mandamus petition|order to show cause)', re.IGNORECASE)
    
    case_match = case_pattern.search(raw_text)
    date_match = date_pattern.search(raw_text)
    mandamus_check = mandamus_pattern.search(raw_text)
    
    extracted_data = {
        "case_id": case_match.group(1) if case_match else "PENDING_ASSIGNMENT",
        "timestamp_extracted": date_match.group(1) if date_match else "UNKNOWN",
        "classification": "WRIT_OF_MANDAMUS" if mandamus_check else "STANDARD_ADMINISTRATIVE_DOCKET",
        "raw_segment_summary": raw_text[:120].strip() + ("..." if len(raw_text) > 120 else "")
    }
    return extracted_data

def main():
    print("=== [CivicAdvocate.OS Docket Parser Initialized] ===")
    print("[*] Enter or paste your raw text block below. Press Ctrl+D when finished to parse:")
    
    raw_input = sys.stdin.read().strip()
    if not raw_input:
        print("[-] Error: Input buffer was empty. Aborting parse cycle.")
        sys.exit(1)
        
    structured_payload = parse_raw_legal_text(raw_input)
    
    print("\n=== [Forensic Structuring Complete] ===")
    print(json.dumps(structured_payload, indent=4))
    
    # Save a copy local to the active workspace for transport pipelines
    output_path = "/data/data/com.termux/files/home/civicadvocate/ledger/mainnet/staged_payload.json"
    with open(output_path, 'w') as f:
        json.dump(structured_payload, f, indent=4)
    print(f"\n[+] Staged payload locked to workspace track location: {output_path}")

if __name__ == "__main__":
    main()
