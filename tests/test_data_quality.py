#!/usr/bin/env python3
"""
Basic data quality tests for the ETL pipeline.
Run with:  pytest tests/
"""

import os
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(__file__))
RAW_DIR = os.path.join(ROOT, "data", "raw")
TRANS_DIR = os.path.join(ROOT, "data", "transformed")

def test_raw_files_exist():
    """Check raw extract files exist."""
    ehr = [f for f in os.listdir(RAW_DIR) if f.startswith("ehr_raw_")]
    labs = [f for f in os.listdir(RAW_DIR) if f.startswith("labs_raw_")]
    assert ehr, "No ehr_raw files found in data/raw"
    assert labs, "No labs_raw files found in data/raw"

def test_transformed_file_exists():
    """Check transformed file exists."""
    tf_path = os.path.join(TRANS_DIR, "transformed.csv")
    assert os.path.exists(tf_path), "transformed.csv not found"

def test_transformed_schema():
    """Validate schema of transformed.csv."""
    tf_path = os.path.join(TRANS_DIR, "transformed.csv")
    df = pd.read_csv(tf_path)
    expected_cols = [
        "lab_id","encounter_id","test_name","value","unit","lab_date",
        "anon_mrn","patient_name","dob","gender","diagnosis_code","provider"
    ]
    assert list(df.columns) == expected_cols, f"Schema mismatch. Found: {list(df.columns)}"

def test_no_empty_mrn():
    """Ensure anonymized MRNs are not null/blank."""
    tf_path = os.path.join(TRANS_DIR, "transformed.csv")
    df = pd.read_csv(tf_path)
    assert df["anon_mrn"].notna().all(), "Null MRNs found after anonymization"
    assert (df["anon_mrn"].str.strip() != "").all(), "Empty MRNs found after anonymization"

def test_value_ranges():
    """Example quality test: check numeric lab values are within plausible range."""
    tf_path = os.path.join(TRANS_DIR, "transformed.csv")
    df = pd.read_csv(tf_path)

    # Only test if 'value' column has numeric entries
    numeric_df = df[pd.to_numeric(df["value"], errors="coerce").notnull()]
    numeric_df["value"] = numeric_df["value"].astype(float)

    assert (numeric_df["value"] >= 0).all(), "Negative lab values detected"
    assert (numeric_df["value"] < 10000).all(), "Unrealistically large lab values detected"
