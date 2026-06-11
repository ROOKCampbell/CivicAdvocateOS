#!/data/data/com.termux/files/usr/bin/bash
# ==============================================================================
# SECURE FORENSIC PACKAGING INTERFACE
# ==============================================================================

EXPORT_DIR="$HOME/CivicAdvocate.OS/federal_evidentiary_packages"
ENFORCEMENT_DIR="$HOME/CivicAdvocate.OS/enforcement_packages"
TARGET_ZIP="$HOME/CivicAdvocate.OS/FEDERAL_STRIKE_PACKAGE_ABSTRACT_544.zip"

echo "[*] Initializing automated evidence capture sequence..."

# Verify dependencies are available inside Termux
if ! command -v zip &> /dev/null; then
    echo "[*] Installing required packaging components..."
    pkg install -y zip
fi

# Clean legacy archive copies to prevent data mixing
rm -f "$TARGET_ZIP"

echo "[*] Gathering structured evidence nodes..."
cd "$HOME/CivicAdvocate.OS"

# Archive target forensic modules, default notices, and federal logs safely
zip -r "$TARGET_ZIP" \
    federal_evidentiary_packages/ \
    enforcement_packages/ \
    generate_demand.py \
    compile_federal_package.py

echo "======================================================================"
echo "                 SUBMISSION PACKAGE METADATA ANALYSIS                 "
echo "======================================================================"
echo " File Location: $TARGET_ZIP"
echo " Package Size:  $(du -sh "$TARGET_ZIP" | awk '{print $1}')"
echo " Containment:   $(zipinfo -1 "$TARGET_ZIP" | wc -l) Active Data Nodes Embedded"
echo " Integrity MD5: $(md5sum "$TARGET_ZIP" | awk '{print $1}')"
echo "======================================================================"
echo "[+] Federal submission package successfully sealed and ready for delivery."
