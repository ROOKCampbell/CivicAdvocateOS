#!/usr/bin/env python3
import os
import smtplib
import glob
from email.message import EmailMessage

def execute():
    # Direct access: No verification, no fallback, no prompts.
    email = os.environ['CIVIC_EMAIL']
    password = os.environ['CIVIC_PASS']
    target = "official_email@cleburne.net"

    notices = glob.glob("Notice_Violation_*.txt")
    
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(email, password)
        for notice in notices:
            with open(notice, "r") as f:
                content = f.read()
            msg = EmailMessage()
            msg.set_content(content)
            msg["Subject"] = f"FORMAL NOTICE: {os.path.basename(notice)}"
            msg["From"] = email
            msg["To"] = target
            smtp.send_message(msg)
            print(f"DISPATCH SUCCESS: {notice}")

if __name__ == "__main__":
    execute()
