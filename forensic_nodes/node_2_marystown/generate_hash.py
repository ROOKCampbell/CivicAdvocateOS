import hashlib

def generate_ledger_hash(file_path):
    sha512_hash = hashlib.sha512()
    try:
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha512_hash.update(byte_block)
        return sha512_hash.hexdigest()
    except FileNotFoundError:
        return "ERROR: Target vault ledger archive not found at specified path."

ledger_path = "/data/data/com.termux/files/home/downloads/.marystown_core_vault/Marystown_Genesis_Master_Ledger.tar.gz"
print("--- [CivicAdvocate.OS] Immutable Hash Generated ---")
print(f"NODE: {ledger_path}")
print(f"SHA-512: {generate_ledger_hash(ledger_path)}")
