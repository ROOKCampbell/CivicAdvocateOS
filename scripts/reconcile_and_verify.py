import csv
import hashlib
import sys
import os

def get_sum(filename):
    total = 0.0
    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            total += float(row['production_mcf'])
    return total

def reconcile(f44, f45):
    if not os.path.exists(f44) or not os.path.exists(f45):
        print(f"ERROR: Files not found in current directory: {f44} or {f45}")
        sys.exit(1)

    sum44 = get_sum(f44)
    sum45 = get_sum(f45)
    delta = abs(sum44 - sum45)

    report = f"Abstract_544: {sum44}\nAbstract_545: {sum45}\nDelta: {delta}\n"
    sha = hashlib.sha512(report.encode()).hexdigest()

    log_name = "reconciliation_log.txt"
    with open(log_name, "w") as f:
        f.write(report + f"SHA512_ANCHOR: {sha}\n")

    print(f"RECONCILIATION COMPLETE. Delta: {delta}. Log: {log_name}. SHA512: {sha[:16]}...")

if __name__ == "__main__":
    # Uses files in current dir by default, or accepts args
    f44 = sys.argv[1] if len(sys.argv) > 1 else 'Abstract_544.csv'
    f45 = sys.argv[2] if len(sys.argv) > 2 else 'Abstract_545.csv'
    reconcile(f44, f45)
