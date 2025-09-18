#!/usr/bin/env python3
"""
Transform step: anonymize, normalize, and join raw data.
Output: data/transformed/transformed.csv
"""
import os, glob
import pandas as pd
from datetime import datetime
from utils import anonymize_mrn

ROOT = os.path.dirname(os.path.dirname(__file__))
RAW_DIR = os.path.join(ROOT, "data", "raw")
OUT_DIR = os.path.join(ROOT, "data", "transformed")
os.makedirs(OUT_DIR, exist_ok=True)

def load_latest_csv(pattern):
    matches = sorted(glob.glob(os.path.join(RAW_DIR, pattern)))
    return matches[-1] if matches else None

def main():
    ehr_file = load_latest_csv("ehr_raw_*.csv")
    labs_file = load_latest_csv("labs_raw_*.csv")
    if not ehr_file or not labs_file:
        raise SystemExit("Raw files not found. Run extract.py first.")

    ehr_df = pd.read_csv(ehr_file)
    labs_df = pd.read_csv(labs_file)

    ehr_df["anon_mrn"] = ehr_df["mrn"].apply(anonymize_mrn)
    labs_df["anon_mrn"] = labs_df["patient_mrn"].apply(anonymize_mrn)

    merged = labs_df.merge(
        ehr_df,
        left_on="encounter_id",
        right_on="encounter_id",
        how="left",
        suffixes=("", "_ehr"),
    )

    transformed = merged[[
        "lab_id","encounter_id","test_name","value","unit","lab_date",
        "anon_mrn","patient_name","dob","gender","diagnosis_code","provider"
    ]]

    out_file = os.path.join(OUT_DIR, "transformed.csv")
    transformed.to_csv(out_file, index=False)
    print(f"[transform] Wrote {out_file} ({len(transformed)} rows)")

if __name__ == "__main__":
    main()
