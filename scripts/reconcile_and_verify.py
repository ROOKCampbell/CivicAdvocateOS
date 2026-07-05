import csv
import hashlib
import sys
import os
import glob

def find_best_file(number):
    """Recursively search for the best file match for a given Abstract number."""
    search_pattern = f"*{number}*production*.csv"
    matches = []
    
    # Walk home directory
    for root, _, files in os.walk(os.path.expanduser("~")):
        for file in files:
            # Match number + "production" + "csv"
            if str(number) in file and "production" in file and file.endswith(".csv"):
                matches.append(os.path.join(root, file))
    
    # Fallback to just number + csv if production not found
    if not matches:
        for root, _, files in os.walk(os.path.expanduser("~")):
            for file in files:
                if str(number) in file and file.endswith(".csv"):
                    matches.append(os.path.join(root, file))
                    
    if not matches:
        return None
        
    # Return the most recently modified file
    return max(matches, key=os.path.getmtime)

def get_sum(filename):
    """Extracts production_mcf sum from a CSV file."""
    total = 0.0
    try:
        with open(filename, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if 'production_mcf' in row:
                    total += float(row['production_mcf'])
        return total
    except Exception as e:
        print(f"FAILED TO PARSE: {filename} - {e}")
        return None

def main():
    f44 = find_best_file("544")
    f45 = find_best_file("545")

    if not f44 or not f45:
        print("CRITICAL: Could not automatically locate required files.")
        print(f"544 Found: {f44}")
        print(f"545 Found: {f45}")
        sys.exit(1)

    print(f"AUTO-LOCATED 544: {f44}")
    print(f"AUTO-LOCATED 545: {f45}")

    sum44 = get_sum(f44)
    sum45 = get_sum(f45)

    if sum44 is None or sum45 is None:
        sys.exit(1)

    delta = abs(sum44 - sum45)
    report = f"Abstract_544: {sum44}\nAbstract_545: {sum45}\nDelta: {delta}\n"
    sha = hashlib.sha512(report.encode()).hexdigest()

    log_name = "reconciliation_log.txt"
    with open(log_name, "w") as f:
        f.write(report + f"SHA512_ANCHOR: {sha}\n")

    print(f"RECONCILIATION COMPLETE. Delta: {delta}. Log: {log_name}. SHA512: {sha[:16]}...")

if __name__ == "__main__":
    main()
