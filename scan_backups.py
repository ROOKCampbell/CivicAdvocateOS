#!/usr/bin/env python3
# CivicAdvocate.OS | Production Forensic Backup Sweep Engine
# Workflow: Overview -> Code -> Implementation

import os
import sys
import hashlib

BACKUP_ROOT = "/data/data/com.termux/files/home/civicadvocate/ledger/mainnet/backups"

def compute_sha512(file_path):
    """Calculates standard SHA-512 hash matrix for a file volume."""
    hasher = hashlib.sha512()
    try:
        with open(file_path, 'rb') as f:
            while chunk := f.read(8192):
                hasher.update(chunk)
        return hasher.hexdigest()
    except Exception as e:
        print(f"  [-] File Read Failure: {file_path} -> {str(e)}")
        return None

def verify_backup_snapshots():
    print("=== [Commencing Automated Backup Verification Sweep] ===")
    if not os.path.exists(BACKUP_ROOT):
        print(f"[-] Error: Target backup folder path missing at: {BACKUP_ROOT}")
        sys.exit(1)

    # Sweep archive subdirectories
    archives = [d for d in os.listdir(BACKUP_ROOT) if d.startswith("archive_")]
    print(f"[+] Isolated {len(archives)} distinct historical snapshots for verification.\n")

    for archive in sorted(archives):
        archive_path = os.path.join(BACKUP_ROOT, archive)
        manifest_path = os.path.join(archive_path, "manifest.sha512")
        print(f"Analyzing Archive Block: [{archive}]")

        if not os.path.exists(manifest_path):
            print("  [-] CRITICAL: manifest.sha512 missing from target snapshot directory.")
            print("-" * 70)
            continue

        # Parse saved signatures mapping
        manifest_entries = {}
        with open(manifest_path, 'r') as m:
            for line in m:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(maxsplit=1)
                if len(parts) == 2:
                    expected_hash, file_name = parts
                    manifest_entries[file_name] = expected_hash

        # Re-compute hashes for baseline verification
        all_passed = True
        for file_name, expected_hash in manifest_entries.items():
            actual_file_path = os.path.join(archive_path, file_name)
            
            if not os.path.exists(actual_file_path):
                print(f"  [-] FAILED: Target file component {file_name} is missing from disk.")
                all_passed = False
                continue

            calculated_hash = compute_sha512(actual_file_path)
            if calculated_hash == expected_hash:
                print(f"  [+] {file_name}: INTEGRITY VERIFIED")
            else:
                print(f"  [-] {file_name}: CHECKSUM CORRUPTED / MISMATCH")
                print(f"      Expected: {expected_hash}")
                print(f"      Actual:   {calculated_hash}")
                all_passed = False

        if all_passed:
            print(f"Status [{archive}]: SEAL SECURE")
        else:
            print(f"Status [{archive}]: COMPROMISED / INCOMPLETE")
        print("-" * 70)

if __name__ == "__main__":
    verify_backup_snapshots()
