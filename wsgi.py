"""
WSGI Production Entry Point - Hardened Core Matrix
Filename: wsgi.py
"""
import sys
import os
import re
import json
import hashlib
import sqlite3
import logging
import threading
from datetime import datetime, timezone
from core_engine import ComplianceEngine

# Configure file logging
logging.basicConfig(
    level=logging.INFO,
    filename='civic_advocate.log',
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def start_compliance_daemon():
    engine = ComplianceEngine(os.getcwd())
    daemon_thread = threading.Thread(target=engine.run_monitor, daemon=True)
    daemon_thread.start()
    logging.info("ComplianceEngine daemon initialized.")

start_compliance_daemon()
