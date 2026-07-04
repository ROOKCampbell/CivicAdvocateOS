import pandas as pd
import hashlib
import datetime
import sqlite3

def hash_row(row):
        # Generates a cryptographic hash for every single row of state data
            row_string = ''.join(str(val) for val in row.values)
                return hashlib.sha512(row_string.encode('utf-8')).hexdigest()

            def ingest_verified_data(csv_path="trc_abstract_544.csv", db_path="forensic_ledger.db"):
                    df = pd.read_csv(csv_path)
                        
                            # Force the Truth Machine to tag every row with an immutable hash
                                df['sha512_signature'] = df.apply(hash_row, axis=1)
                                    df['ingestion_timestamp'] = datetime.datetime.now(datetime.timezone.utc)
                                        
                                            conn = sqlite3.connect(db_path)
                                                df.to_sql('verified_state_logs', conn, if_exists='append', index=False)
                                                    conn.close()
                                                        
                                                            print(f"SUCCESS: {len(df)} rows ingested. Hashed to the foundational log.")

                                                            if __name__ == "__main__":
                                                                    ingest_verified_data()
