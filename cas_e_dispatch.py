#!/usr/bin/env python3
"""
Civic Advocate Service (CAS) - E-Dispatch Module
Description: Automates the electronic signing and dispatch of notices to 
             public officials via SMTP.
"""

import smtplib
import os
import glob
from email.message import EmailMessage

# --- CONFIGURATION ---
# Replace with your actual SMTP credentials or environment variables
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465
SENDER_EMAIL = "your_email@gmail.com"
SENDER_PASSWORD = "your_app_password" 
RECIPIENT_EMAIL = "official_email@cleburne.net" # Target official's email
# ---------------------

def send_electronic_notice(file_path):
    with open(file_path, "r") as f:
        content = f.read()
    
    msg = EmailMessage()
    msg.set_content(content)
    msg["Subject"] = f"FORMAL NOTICE: Non-Compliance Record ID {os.path.basename(file_path)}"
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECIPIENT_EMAIL

    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as smtp:
            smtp.login(SENDER_EMAIL, SENDER_PASSWORD)
            smtp.send_message(msg)
        print(f"[E-DISPATCH] Success: Notice {file_path} transmitted to {RECIPIENT_EMAIL}.")
    except Exception as e:
        print(f"[E-DISPATCH] Failed: {e}")

if __name__ == "__main__":
    # Finds all generated notices and sends them
    notices = glob.glob("Notice_Violation_Record_*.txt")
    if not notices:
        print("[!] No notices found to dispatch.")
    else:
        for notice in notices:
            send_electronic_notice(notice)
