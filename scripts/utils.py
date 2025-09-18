#!/usr/bin/env python3
"""
Utility functions: hashing, stable UUIDs, database connection
"""
import hashlib
import uuid
import psycopg2
from psycopg2.extras import execute_values

def anonymize_mrn(mrn: str) -> str:
    """Hash MRN deterministically with SHA256."""
    if not mrn or mrn.strip() == "":
        return ""
    return hashlib.sha256(mrn.encode("utf-8")).hexdigest()

def stable_uuid(namespace: str, value: str) -> str:
    """Generate a stable UUID5 from a namespace + value."""
    return str(uuid.uuid5(uuid.UUID(namespace), value))

def get_db_connection():
    """
    Connect to Postgres DB using environment variables.
    Requires: POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT
    """
    import os
    conn = psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB", "mediflow"),
        user=os.getenv("POSTGRES_USER", "airflow"),
        password=os.getenv("POSTGRES_PASSWORD", "airflow"),
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=os.getenv("POSTGRES_PORT", "5432"),
    )
    return conn

def bulk_insert(cursor, table, columns, rows):
    """Bulk insert rows into a table."""
    sql = f"INSERT INTO {table} ({', '.join(columns)}) VALUES %s"
    execute_values(cursor, sql, rows)
