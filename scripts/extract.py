#!/usr/bin/env python3
"""
Extract step: write raw data files under data/raw
"""
import os
import csv
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(__file__))
OUT_DIR = os.path.join(ROOT, "data", "raw")
os.makedirs(OUT_DIR, exist_ok=True)

ehr_rows = [
    ["mrn", "patient_name", "dob", "gender", "phone", "email", "encounter_id", "encounter_date", "diagnosis_code", "provider"],
    ["mrn123", "Alice Smith", "1985-03-12", "F", "XXX-XXX-XXXX", "alice@example.com", "101", "2025-09-02", "A01.0", "dr. patel"],
    ["mrn456", "Bob Johnson", "1978-07-04", "M", "XXX-XXX-XXXX", "bob@example.com", "102", "2025-09-07", "B20", "dr. kumar"],
]

labs_rows = [
    ["lab_id", "encounter_id", "test_name", "value", "unit", "lab_date", "patient_mrn"],
    ["1001", "101", "Hemoglobin", "13.5", "g/dl", "2025-09-03", "mrn123"],
    ["1002", "102", "Cholesterol", "190.0", "mg/dl", "2025-09-08", "mrn456"],
    ["1003", "103", "Glucose", "95.0", "mg/dl", "2025-09-11", "mrn123"],
]

def write_csv(path, rows):
    with open(path, "w", newline="", encoding="utf8") as f:
        w = csv.writer(f)
        w.writerows(rows)

def main():
    ts = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    ehr_path = os.path.join(OUT_DIR, f"ehr_raw_{ts}.csv")
    labs_path = os.path.join(OUT_DIR, f"labs_raw_{ts}.csv")
    write_csv(ehr_path, ehr_rows)
    write_csv(labs_path, labs_rows)
    print(f"[extract] Wrote {ehr_path}")
    print(f"[extract] Wrote {labs_path}")

if __name__ == "__main__":
    main()

