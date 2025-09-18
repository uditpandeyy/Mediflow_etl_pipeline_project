#!/usr/bin/env python3
"""
Load step: insert processed data into PostgreSQL tables.
"""
import os
import pandas as pd
from utils import get_db_connection, bulk_insert

ROOT = os.path.dirname(os.path.dirname(__file__))
TRANS_DIR = os.path.join(ROOT, "data", "transformed")
TRANS_FILE = os.path.join(TRANS_DIR, "transformed.csv")

def main():
    if not os.path.exists(TRANS_FILE):
        raise SystemExit("transformed.csv not found. Run transform.py first.")

    df = pd.read_csv(TRANS_FILE)

    conn = get_db_connection()
    cur = conn.cursor()

    # Example: load into patients table
    patients = df[["anon_mrn","patient_name","dob","gender"]].drop_duplicates("anon_mrn")
    bulk_insert(cur, "patients", ["mrn_hash","full_name","dob","gender"], patients.values.tolist())

    # Example: load into lab_results table
    labs = df[["lab_id","anon_mrn","encounter_id","test_name","value","unit","lab_date"]]
    bulk_insert(cur, "lab_results",
        ["lab_id","mrn_hash","encounter_id","test_name","result_value","units","result_date"],
        labs.values.tolist())

    conn.commit()
    cur.close()
    conn.close()
    print("[load] Insert complete.")

if __name__ == "__main__":
    main()
