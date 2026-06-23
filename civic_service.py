#!/usr/bin/env python3
import logging

# 1. Import your custom engine class from your newly renamed file!
from anti_mistake_engine import AntiMistakeEngine

# Set up logging for this app script
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)s] CivicApp: %(message)s')

# 2. Instantiate the engine inside this separate app
app_safety_layer = AntiMistakeEngine()

# 3. Define a real-world system operation that might fail
def process_voter_registration(voter_data):
    logging.info(f"Processing registration for: {voter_data['voter_name']}")
    # This will raise a KeyError if 'zip_code' is missing from the dictionary
    postal_zone = voter_data['zip_code']
    return f"Voter approved for Zone {postal_zone}"

# ==========================================================
# Operational Execution
# ==========================================================
if __name__ == "__main__":
    logging.info("Starting Civic Advocate registration system...")

    # Data block with a missing 'zip_code' mistake
    malformed_voter_record = {
        "voter_name": "Alice Vance",
        "age": 29
        # 'zip_code' is intentionally missing to simulate a data mistake
    }

    print("\n--- Running App Operation via Anti-Mistake Engine ---")
    # Instead of crashing the whole registration app, the engine catches the error
    final_status = app_safety_layer.execute_safely(process_voter_registration, malformed_voter_record)

    print(f"\nFinal Operation Output: {final_status}")
    print(f"Engine Anomalies Tracked: {app_safety_layer.fault_registry}\n")
