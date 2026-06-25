import sys
import urllib.parse
import webbrowser

def main():
    print("=============================================================")
    print("                BATCH PAYLOAD DISPATCH ENGINE                ")
    print("=============================================================")
    
    # Pre-compiled multi-jurisdictional target repository
    targets = [
        "michael.marrero@cleburne.net",
        "ivy.peterson@cleburne.net",
        "citysecretary@cleburne.net",
        "greg.abbott@gov.texas.gov",
        "governor@state.tx.us"
    ]
    
    print("[+] Targeted Broadcast Repositories Loaded:")
    for email in targets:
        print(f"    - {email}")
    print("=============================================================")
    
    subject = input("Enter Subject Line: ").strip()
    if not subject:
        subject = "Administrative Notice of Default / Fiduciary Audit"
        print(f"[!] Defaulting subject to: {subject}")
        
    print("\nHow would you like to load the bill / payload body?")
    print("[1] Paste text directly into terminal")
    print("[2] Load content from a local text file")
    choice = input("Select option (1-2): ").strip()
    
    body_content = ""
    if choice == '1':
        print("\nEnter/paste your text below. (Type 'EOF' on a new line and press Enter when done):")
        lines = []
        while True:
            line = sys.stdin.readline()
            if line.strip() == 'EOF':
                break
            lines.append(line)
        body_content = "".join(lines)
    elif choice == '2':
        file_path = input("Enter the path to your text file (e.g., bill.txt): ").strip()
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                body_content = f.read()
            print(f"[+] Successfully loaded {len(body_content)} characters from file.")
        except Exception as e:
            print(f"[!] Failed to read file: {e}")
            sys.exit(1)
    else:
        print("[!] Invalid choice.")
        sys.exit(1)

    if not body_content.strip():
        print("[!] Payload body cannot be empty.")
        sys.exit(1)

    # Standard mailto structure uses commas to handle multiple recipients simultaneously
    recipient_string = ",".join(targets)
    encoded_subject = urllib.parse.quote(subject)
    encoded_body = urllib.parse.quote(body_content)
    
    mail_to_url = f"mailto:{recipient_string}?subject={encoded_subject}&body={encoded_body}"
    
    print("\n[+] Packing payload and initializing multi-cast handoff...")
    webbrowser.open(mail_to_url)
    print("[+] Operation successful. Handoff executed to native device mail architecture.")

if __name__ == "__main__":
    main()
