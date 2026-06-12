import os
LOG_PATH = os.path.expanduser("~/CivicAdvocate.OS/rrc_cleburne_production.log")

if os.path.exists(LOG_PATH):
    with open(LOG_PATH, 'r') as f:
        lines = f.readlines()
        print(f"Total lines in log: {len(lines)}")
        for i, line in enumerate(lines[:10]):
            print(f"Line {i}: {line.strip()}")
else:
    print("Log file not found.")
