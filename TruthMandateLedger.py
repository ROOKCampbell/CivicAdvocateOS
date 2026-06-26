mport hashlib
import json
import os
import datetime

class TruthMandateLedger:
        def __init__(self, ledger_path="ledger.json"):
                    self.ledger_path = ledger_path
                            self.ledger = self._load_ledger()

                                def _load_ledger(self):
                                            if os.path.exists(self.ledger_path):
                                                            with open(self.ledger_path, 'r') as f:
                                                                                return json.load(f)
                                                                                    return {"records": []}

                                                                                    def _generate_hash(self, data_dict):
                                                                                                """Generates an immutable SHA-512 hash for the record."""
                                                                                                        # Convert dict to a deterministic string
                                                                                                                serialized_data = json.dumps(data_dict, sort_keys=True).encode('utf-8')
                                                                                                                        return hashlib.sha512(serialized_data).hexdigest()

                                                                                                                        def ingest_record(self, record_type, fields):
                                                                                                                                    """Ingests and anchors a new record to the ledger."""
                                                                                                                                            entry = {
                                                                                                                                                                "timestamp": datetime.datetime.utcnow().isoformat(),
                                                                                                                                                                            "type": record_type,
                                                                                                                                                                                        "data": fields
                                                                                                                                                                                                }
                                                                                                                                                    
                                                                                                                                                    # Add integrity check
                                                                                                                                                            entry["integrity_hash"] = self._generate_hash(entry["data"])
                                                                                                                                                                    
                                                                                                                                                                            self.ledger["records"].append(entry)
                                                                                                                                                                                    self._save_ledger()
                                                                                                                                                                                            print(f"Record successfully ingested: {entry['integrity_hash'][:16]}...")

                                                                                                                                                                                                def _save_ledger(self):
                                                                                                                                                                                                            with open(self.ledger_path, 'w') as f:
                                                                                                                                                                                                                            json.dump(self.ledger, f, indent=4)

                                                                                                                                                                                                                            # Usage Logic
                                                                                                                                                                                                                            if __name__ == "__main__":
                                                                                                                                                                                                                                    ledger = TruthMandateLedger()

                                                                                                                                                                                                                                        # Example: Ingesting Silas Elbert Bandy Abstract 544
                                                                                                                                                                                                                                            bandy_data = {
                                                                                                                                                                                                                                                            "abstract_id": "544",
                                                                                                                                                                                                                                                                    "survey_name": "Silas Elbert Bandy",
                                                                                                                                                                                                                                                                            "original_grantor": "State of Texas",
                                                                                                                                                                                                                                                                                    "patent_date": "1888-01-01",
                                                                                                                                                                                                                                                                                            "notes": "Primary land node for mineral drainage audit."
                                                                                                                                                                                                                                                                                                }

                                                                                                                                                                                                                                                ledger.ingest_record("Land_Grant", bandy_data)
