import json, time, os

def clear_screen():
    print("\033[H\033[J", end="")

def refresh():
    while True:
        clear_screen()
        print("=== CIVIC ADVOCATE.OS: UNIVERSAL TRUTH MONITOR ===")
        try:
            with open("manifest.json", "r") as f:
                blocks = json.load(f)
                depth = len(blocks)
                last_id = blocks[-1]['id']
            print(f"Chain Depth: {depth} | Last Block: #{last_id}")
        except:
            print("Chain Status: INITIALIZING...")

        print("\n--- RECENT AUDIT EVENTS ---")
        try:
            with open("audit.log", "r") as f:
                print("".join(f.readlines()[-5:]))
        except:
            print("No logs yet.")
        
        time.sleep(2)

if __name__ == "__main__":
    refresh()
