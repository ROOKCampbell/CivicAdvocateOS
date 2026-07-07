#!/usr/bin/env python3
import json
import os
import smtplib
import glob
from email.message import EmailMessage

# Accessing stored credentials from local system config
CONFIG_PATH = os.path.expanduser("~/.civic_config")

def execute():
    if not os.path.exists(CONFIG_PATH):
        print("[!] Error: Configuration file not found at " + CONFIG_PATH)
        return

    with open(CONFIG_PATH, "r") as f:
        config = json.load(f)

    notices = glob.glob("Notice_Violation_*.txt")
    if not notices:
        print("[!] No notices found to dispatch.")
        return

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(config["sender_email"], config["password"])
        for notice in notices:
            with open(notice, "r") as f:
                content = f.read()
            msg = EmailMessage()
            msg.set_content(content)
            msg["Subject"] = f"FORMAL NOTICE: {os.path.basename(notice)}"
            msg["From"] = config["sender_email"]
            msg["To"] = "official_email@cleburne.net"
            smtp.send_message(msg)
            print(f"[DISPATCHED] {notice}")

if __name__ == "__main__":
    execute()
