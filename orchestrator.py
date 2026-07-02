import threading
import time
import subprocess
from rich.live import Live
from rich.table import Table

def run_task(script_name, log_name):
    base_path = "/data/data/com.termux/files/home/CivicAdvocate.OS/bin/"
    log_path = "/data/data/com.termux/files/home/CivicAdvocate.OS/logs/"
    cmd = f"{base_path}{script_name} > {log_path}{log_name}.log 2>&1"
    subprocess.run(cmd, shell=True)

def generate_table():
    table = Table(title="CivicAdvocate.OS | Live Audit Status")
    table.add_column("Module", style="cyan")
    table.add_column("Status", style="magenta")
    table.add_column("Last Integrity Check", justify="right", style="green")
    table.add_row("RRC-544/545", "LOGGING_ACTIVE", time.strftime("%H:%M:%S"))
    table.add_row("JC-Sheriff", "LOGGING_ACTIVE", time.strftime("%H:%M:%S"))
    table.add_row("Tax-Nexus", "LOGGING_ACTIVE", time.strftime("%H:%M:%S"))
    return table

if __name__ == "__main__":
    threading.Thread(target=run_task, args=("audit_rrc.sh", "rrc_audit")).start()
    threading.Thread(target=run_task, args=("draft_final_notice.sh", "final_notice")).start()
    threading.Thread(target=run_task, args=("correlate_tax_nexus.sh", "tax_nexus")).start()
    
    with Live(generate_table(), refresh_per_second=1) as live:
        while True:
            time.sleep(1)
