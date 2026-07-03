import dns.resolver
import hashlib
import datetime

def audit_mx_fqdn_forensic(domain_name):
    print(f"--- CivicAdvocate.OS: Initiating Forensic MX Audit for [{domain_name}] ---")
    
    # Initialize the ledger entry
    audit_log = f"Timestamp: {datetime.datetime.now(datetime.timezone.utc).isoformat()}\nTarget: {domain_name}\n"
    
    try:
        # Querying the MX records
        mx_records = dns.resolver.resolve(domain_name, 'MX')
        
        for rdata in mx_records:
            record_entry = f"Priority: {rdata.preference} | Target FQDN: {rdata.exchange}"
            print(record_entry)
            audit_log += record_entry + "\n"
            
        # Generate SHA-512 hash of the audit result for the Truth Mandate ledger
        ledger_hash = hashlib.sha512(audit_log.encode()).hexdigest()
        print(f"\n[Cryptographic Hash (SHA-512) - Ledger Secured]\n{ledger_hash}")
            
	
        print(f"[!] No MX records found for {domain_name}. Data dropped.")
    except dns.resolver.NXDOMAIN:
        print(f"[!] The FQDN {domain_name} does not exist. Data dropped.")
    except Exception as e:
        print(f"[!] Audit failed: {e}")

# Target domain to audit (Replace with target domain)
audit_mx_fqdn_forensic("example.com")
