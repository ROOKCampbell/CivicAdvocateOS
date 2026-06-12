#!/bin/bash
# CivicAdvocate.OS - Central Index Compilation Engine

INDEX_FILE="README.md"
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")

# 1. Initialize Master Layout
cat << EOF > "$INDEX_FILE"
# CivicAdvocate.OS Master Ledger Index
**System Generated:** $TIMESTAMP  
**Security Protocol:** Internal Audit Tracking Only  

---

## Verified Data Nodes & Manifests

| File Name | Date Generated | Classification | Status |
| :--- | :--- | :--- | :--- |
EOF

# 2. Parse Markdown Manifest Files Dynamically
for file in Manifest_Abstract544_Node_*.md; do
    # Check if files matching the pattern exist
    [ -e "$file" ] || continue

    # Extract critical ledger values from file bodies
    gen_date=$(grep -i "TIMESTAMP:" "$file" | head -n 1 | sed -E 's/.*TIMESTAMP:\*\* ([0-9]{4}-[0-9]{2}-[0-9]{2}).*/\1/')
    classification=$(grep -i "CLASSIFICATION:" "$file" | head -n 1 | sed -E 's/.*CLASSIFICATION:\*\* (.*)/\1/')
    status=$(grep -i "\* \*\*Status:\*\*" "$file" | head -n 1 | sed -E 's/.*Status:\*\* (.*)/\1/')

    # Fallback to default entries if fields are unpopulated
    [ -z "$gen_date" ] && gen_date="N/A"
    [ -z "$classification" ] && classification="UNKNOWN"
    [ -z "$status" ] && status="Awaiting Audit"

    # Append mapped parameters as an index row
    echo "| [$file]($file) | $gen_date | $classification | $status |" >> "$INDEX_FILE"
done

# 3. Append Ledger Footer Note
cat << EOF >> "$INDEX_FILE"

---
> **System Warning:** All listed file states are mapped directly from local workspace files. Tampering with file structures will invalidate downstream verification checks.
EOF

# 4. Set Execution Permissions & Log Confirmation
chmod 755 "$INDEX_FILE"
echo "--- [CivicAdvocate.OS] Master Ledger Index Compiled ---"
echo "Output Target: $INDEX_FILE"
