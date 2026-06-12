import hashlib
import os

FILE_PATH = os.path.expanduser("~/CivicAdvocate.OS/Systemic_Drainage_Impact_Summary_FINAL_2026-06-11.md")

def generate_seal():
    sha512 = hashlib.sha512()
    with open(FILE_PATH, 'rb') as f:
        sha512.update(f.read())
    
    seal = sha512.hexdigest()
    with open(os.path.expanduser("~/CivicAdvocate.OS/system_seal.txt"), 'w') as s:
        s.write(f"SYSTEM_SEAL_HASH: {seal}\n")
        s.write("TIMESTAMP: 2026-06-11 23:25:00\n")
        s.write("STATUS: LOCKED_FOR_TRANSIT")
        
    print(f"[SYS] Cryptographic seal generated: {seal[:16]}...")
    print("[SYS] System locked for federal transit.")

if __name__ == "__main__":
    generate_seal()
