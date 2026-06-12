import datetime
import os

nodes = ["GS_544_EXT", "GS_545_EXT"]
timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
base_dir = os.path.expanduser("~/CivicAdvocate.OS")

for node in nodes:
    filename = f"Notice_of_Lineage_Challenge_{node}.md"
    file_path = os.path.join(base_dir, filename)
    with open(file_path, "w") as f:
        f.write(f"# NOTICE OF LINEAGE CHALLENGE: {node}\n")
        f.write(f"DATE: {timestamp}\n\n")
        f.write("The above-referenced extraction node has been identified as lacking historical lineage certification.\n")
        f.write("This constitutes a violation of established mineral rights for the Silas Elbert Bandy Survey, Abstract 544.\n")
        f.write("FORMAL DEMAND: Immediate cessation of operations and submission of valid title proof.\n")
    print(f"[SYS] Challenge drafted: {file_path}")
