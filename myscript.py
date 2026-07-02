#!/usr/bin/env python3
import argparse
import subprocess
import sys
from pathlib import Path

def main():
    # 1. SETUP THE SCRIPT ARGUMENTS (Replaces $1, $2, etc.)
    parser = argparse.ArgumentParser(description="My robust Python automation script.")
    parser.add_argument("target", help="The primary file or directory to act on")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose output")

    args = parser.parse_args()

    # 2. BASIC LOGIC (Replaces standard Bash if-statements)
    if args.verbose:
        print(f"DEBUG: Starting script with target: {args.target}")

    # 3. RUNNING A SYSTEM COMMAND SAFELY (Replaces standard Bash execution)
    try:
        if args.verbose:
            print("Running a system command...")
        
        # Example: Running the 'echo' command safely
        subprocess.run(["echo", f"Success! Acting on {args.target}"], check=True)
        
    except subprocess.CalledProcessError as e:
        print(f"ERROR: Command failed with exit code {e.returncode}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
