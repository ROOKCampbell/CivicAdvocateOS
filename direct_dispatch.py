import sys
import urllib.parse
import webbrowser

def main():
    print("=============================================================")
    print("                DIRECT PAYLOAD DISPATCH UTILITY               ")
    print("=============================================================")
    
    target_email = input("Enter Target Email Address: ").strip()
    if not target_email:
        print("[!] Target email is required.")
        sys.exit(1)
        
    subject = input("Enter Subject Line: ").strip()
    
    print("\nHow would you like to load the message/bill body?")
    print("[1] Paste text directly into terminal")
    print("[2] Load content from a local text file")
    choice = input("Select option (1-2): ").strip()
    
    body_content = ""
    if choice == '1':
        print("\nEnter/paste your message text below. (Type 'EOF' on a new line and press Enter when done):")
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

    # Convert payloads to secure URL format
    encoded_subject = urllib.parse.quote(subject)
    encoded_body = urllib.parse.quote(body_content)
    
    mail_to_url = f"mailto:{target_email}?subject={encoded_subject}&body={encoded_body}"
    
    print("\n[+] Triggering local architecture handoff...")
    webbrowser.open(mail_to_url)
    print("[+] Operation complete. Check your device's native mail client window.")

if __name__ == "__main__":
    main()
