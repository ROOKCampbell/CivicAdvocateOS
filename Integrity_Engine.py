import yaml
import sys
import logging

def load_config(config_path='config.yaml'):
    try:
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
            return config
    except FileNotFoundError:
        logging.error(f"Configuration file {config_path} not found.")
        sys.exit(1)

def initialize_engine():
    mandate = load_config()
    primary_key = mandate['lineage_anchor']['primary_key']
    print(f"[*] Integrity Engine initialized. Lineage root: {primary_key}")
    return mandate

if __name__ == "__main__":
    current_mandate = initialize_engine()
