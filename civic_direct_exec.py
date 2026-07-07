#!/usr/bin/env python3
import os
import smtplib
import glob
from email.message import EmailMessage

# Accessing credentials directly from system environment variables
EMAIL = os.environ.get("CIVIC_EMAIL")
PASS = os.environ.get("CIVIC_PASS")

def execute():
    if not EMAIL or not PASS:
        print("[!] SYSTEM ERROR: Credentials not found in environment variables. Set them and run again.")
        return

    notices = glob.glob("Notice_Violation_*.txt")
    if not notices:
        print("[!] No notices found to dispatch.")
        return

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL, PASS)
        for notice in notices:
            with open(notice, "r") as f:
                content = f.read()
            msg = EmailMessage()
            msg.set_content(content)
            msg["Subject"] = f"FORMAL NOTICE: Non-Compliance Record ID {os.path.basename(notice)}"
            msg["From"] = EMAIL
            msg["To"] = "official_email@cleburne.net"
            smtp.send_message(msg)
            print(f"[DISPATCHED] Notice {notice} sent to Cleburne authorities.")

if __name__ == "__main__":
    execute()
