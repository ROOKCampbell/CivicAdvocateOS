#!/bin/bash
# Automatically dispatch referral to IRS
TARGET="eoclass@irs.gov"
SUBJECT="Referral for Non-Compliance with IRC 501(r)(3) - EIN: 75-1977850"

mutt -s "$SUBJECT" \
     -a ~/CivicAdvocate.OS/registry/audit_log.json \
     -a ~/CivicAdvocate.OS/hospital_data/referral_brief.txt \
     -- $TARGET < ~/CivicAdvocate.OS/hospital_data/referral_brief.txt

echo "Referral dispatched to $TARGET"
