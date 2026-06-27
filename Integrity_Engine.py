import hashlib
import os

def generate_ledger(directory, ledger_file):
    print(f'[*] Calibrating directory: {directory}')
    with open(ledger_file, 'w') as f:
        for root, dirs, files in os.walk(directory):
            for name in files:
                if name in [ledger_file, 'Integrity_Engine.py', 'watchdog_log.txt']:
                    continue
                
                filepath = os.path.join(root, name)
                sha512 = hashlib.sha512()
                try:
                    with open(filepath, 'rb') as file_to_hash:
                        while chunk := file_to_hash.read(8192):
                            sha512.update(chunk)
                    f.write(f'{sha512.hexdigest()}  {filepath}\n')
                except Exception as e:
                    print(f'[!] Could not hash {filepath}: {e}')

    print(f'[+] Calibration complete. Ledger saved to: {ledger_file}')

if __name__ == '__main__':
    generate_ledger('.', 'integrity.ledger')
