import os
from pathlib import Path

# Targeting the known Cleburne / Bandy archive
archive_path = Path("/data/data/com.termux/files/home/CivicAdvocate.OS/ledger/text_archive")

def analyze_formats():
    if not archive_path.exists():
        print(f"SYSTEM HALT: Archive path not found at {archive_path}")
        return
    
    print(f"Scanning archive: {archive_path}\n")
    
    for file_path in archive_path.iterdir():
        if file_path.is_file():
            print(f"--- Node Identified: {file_path.name} ---")
            
            try:
                with open(file_path, 'r', errors='ignore') as f:
                    # Extract the first 3 lines to analyze the data structure
                    for i, line in enumerate(f):
                        if i < 3:
                            print(f"Line {i+1}: {line.strip()}")
                        else:
                            break
            except Exception as e:
                print(f"Read Error: {e}")
            print("-" * 40 + "\n")

if __name__ == "__main__":
    analyze_formats()
