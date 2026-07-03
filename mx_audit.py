import dns.resolver

# Initialize a custom resolver and bypass /etc/resolv.conf
audit_resolver = dns.resolver.Resolver(configure=False)

# Declare authoritative fallback nodes (e.g., Google, Cloudflare)
audit_resolver.nameservers = ['8.8.8.8', '1.1.1.1'] 

# Execute the forensic MX query using the hardened resolver
try:
    answers = audit_resolver.resolve('example.com', 'MX')
    for rdata in answers:
        print(f"MX Record: {rdata.exchange} | Preference: {rdata.preference}")
except Exception as e:
    print(f"[!] Audit failed: {e}")	

