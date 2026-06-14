import os, time, shutil

# Configuration
STRIKE_PACKAGE_DIR = "./strike_packages"
ARCHIVE_DIR = "./federal_evidence_archive"

def archive_and_queue():
    """Moves detected breaches to an immutable archive for transmission."""
    if not os.path.exists(ARCHIVE_DIR): os.makedirs(ARCHIVE_DIR)
    
    while True:
        packages = [f for f in os.listdir(STRIKE_PACKAGE_DIR) if f.endswith(".json")]
        for package in packages:
            src = os.path.join(STRIKE_PACKAGE_DIR, package)
            dst = os.path.join(ARCHIVE_DIR, package)
            
            # Atomic move ensures the evidence is secured and the queue is cleared
            shutil.move(src, dst)
            print(f"Transmission Queue: Evidence {package} secured for Federal Audit.")
        
        time.sleep(300) # Monitor queue every 5 minutes

if __name__ == "__main__":
    archive_and_queue()
