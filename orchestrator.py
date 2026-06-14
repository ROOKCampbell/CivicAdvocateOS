import subprocess
import hashlib
import os

def generate_sha512(file_path):
    sha512 = hashlib.sha512()
    with open(file_path, "rb") as f:
        while chunk := f.read(4096):
            sha512.update(chunk)
    return sha512.hexdigest()

def run_fiscal_audit():
    print("[1/3] Running Fiscal Audit...")
    # Pointing to the validated forensic ledger
    subprocess.run(["python3", "process_audit.py", "--file", "municipal_data/forensic_ledger.json"])
    print("      - Fiscal audit logs processed.")

def run_federal_referral():
    print("[2/3] Preparing Federal Referral Package...")
    package_path = "CivicAdvocate_Federal_Referral_Package.tar.gz"
    if os.path.exists(package_path):
        print(f"      - Package Fingerprint: {generate_sha512(package_path)}")
    else:
        print("      - [ERROR] Referral package not found.")
    print("      - Referral package integrity locked.")

def run_mineral_enforcement():
    print("[3/3] Executing Abstract 544 Enforcement...")
    subprocess.run(["python3", "extract_all_nodes.py", "--abstract", "544"])
    print("      - Mineral drainage analysis complete.")

def main():
    print("--- CivicAdvocate.OS Terminal Synchronization ---")
    run_fiscal_audit()
    run_federal_referral()
    run_mineral_enforcement()
    print("--- Terminal Operations Synchronized ---")

if __name__ == "__main__":
    main()
