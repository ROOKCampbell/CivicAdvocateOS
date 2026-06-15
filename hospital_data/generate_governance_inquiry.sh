#!/bin/bash
# Generate Governance Inquiry for THR Board of Trustees
cat > governance_inquiry.txt <<END
TO: Texas Health Resources Board of Trustees / Compliance Committee
RE: Formal Inquiry - IRS Section 501(r)(3) Compliance
FACILITY: Texas Health Cleburne / Texas Health Huguley

I am conducting a forensic audit of community health benefit expenditures as 
reported in the most recent IRS Form 990, Schedule H. Under IRC Section 501(r)(3), 
Texas Health Resources is required to maintain a publicly accessible 
Community Health Needs Assessment (CHNA) and an adopted Implementation 
Strategy (IS) for each facility.

Please provide the direct URL or document path for the following:
1. Current 2023-2025 Implementation Strategy log for the referenced facilities.
2. Itemized expenditure reports supporting the Net Community Benefit Expense 
   reported in the most recent Schedule H.
3. Documentation of Board approval for the current implementation strategy 
   pursuant to IRS requirements.

Failure to provide these documents constitutes a compliance discrepancy 
within my master forensic ledger.
END
echo "Inquiry generated: governance_inquiry.txt"
