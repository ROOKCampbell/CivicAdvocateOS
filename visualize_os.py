import json, time, os
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Configure dark theme dashboard
plt.style.use('dark_background')
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
fig.suptitle('CivicAdvocate.OS - Universal Truth Dashboard', fontsize=16)

def animate(i):
    # Quadrant 1: Ledger Depth & Status
    try:
        with open("manifest.json", "r") as f:
            blocks = json.load(f)
            depth = len(blocks)
            last_id = blocks[-1]['id'] if blocks else 0
    except (FileNotFoundError, json.JSONDecodeError):
        depth = 0
        last_id = 0

    ax1.clear()
    ax1.barh(['Chain Depth'], [depth], color='#00ff00')
    ax1.set_xlim(0, max(20, depth + 5))
    ax1.set_title(f"System Status: OPTIMAL | Node ID: 0xAbC... | Last Block: #{last_id}")
    ax1.grid(axis='x', linestyle='--', alpha=0.5)

    # Quadrant 2: Audit Event Log (Simulated)
    try:
        with open("audit.log", "r") as f:
            logs = f.readlines()[-10:] # Last 10 lines
    except FileNotFoundError:
        logs = ["[*] Initializing audit trail..."]

    ax2.clear()
    ax2.axis('off')
    log_text = "".join(logs)
    ax2.text(0.01, 0.99, f"--- AUDIT EVENT LOG ---\n\n{log_text}", 
             transform=ax2.transAxes, fontsize=10, va='top', family='monospace')

# Run visualization (updates every 2 seconds)
ani = animation.FuncAnimation(fig, animate, interval=2000)
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()
