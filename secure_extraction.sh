#!/bin/bash
# CivicAdvocate.OS - Forensic Cold Storage Extraction Utility
# Protocol: Copy -> Verify SHA-512 -> Secure Purge

SOURCE_DIR="secure_vault/archival_transit"
ARCHIVE_NAME="FSP_FINAL_DELIVERY_ABSTRACT_544.tar.gz"
HASH_NAME="FSP_FINAL_DELIVERY_ABSTRACT_544.tar.gz.sha512"

TARGET_MOUNT="$1"

if [ -z "$TARGET_MOUNT" ]; then
    echo "ERROR: Target mount point required."
    echo "Usage: ./secure_extraction.sh /path/to/external/drive"
    exit 1
fi

if [ ! -d "$TARGET_MOUNT" ]; then
    echo "ERROR: Hardware mount point '$TARGET_MOUNT' not found or not accessible."
    exit 1
fi

echo "--- [CivicAdvocate.OS] Initiating Secure Extraction ---"
echo "Target Hardware: $TARGET_MOUNT"

echo "[*] Cloning archive and cryptographic signatures to cold storage..."
cp "$SOURCE_DIR/$ARCHIVE_NAME" "$TARGET_MOUNT/"
cp "$SOURCE_DIR/$HASH_NAME" "$TARGET_MOUNT/"

echo "[*] Executing post-transfer SHA-512 verification on hardware..."
cd "$TARGET_MOUNT" || exit

if sha512sum -c "$HASH_NAME"; then
    echo "[+] MATCH CONFIRMED: Cold storage block is identical to local anchor."
    echo "[*] Executing cryptographic wipe of local transit artifacts..."
    cd - > /dev/null
    shred -u "$SOURCE_DIR/$ARCHIVE_NAME" 2>/dev/null || rm "$SOURCE_DIR/$ARCHIVE_NAME"
    shred -u "$SOURCE_DIR/$HASH_NAME" 2>/dev/null || rm "$SOURCE_DIR/$HASH_NAME"
    echo "[+] EXTRACTION COMPLETE. Local vault sanitized. Hardware isolated."
else
    echo "[-] FATAL ERROR: Cryptographic mismatch detected on target volume."
    echo "[-] Suspected hardware corruption or interception. Rolling back..."
    rm "$TARGET_MOUNT/$ARCHIVE_NAME"
    rm "$TARGET_MOUNT/$HASH_NAME"
    echo "[-] ABORTED. State machine preserved. Do not trust the target hardware."
    exit 1
fi
