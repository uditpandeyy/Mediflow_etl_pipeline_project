from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import pandas as pd
import psycopg2
from sqlalchemy import create_engine

# -------------------------------
# Default args for DAG
# -------------------------------
default_args = {
    'owner': 'udit',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# -------------------------------
# Database connection details
# -------------------------------
DB_HOST = "postgres"
DB_NAME = "mediflow"
DB_USER = "airflow"
DB_PASS = "airflow"
DB_PORT = "5432"

engine = create_engine(f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

# -------------------------------
# Extract function
# -------------------------------
def extract_data(**kwargs):
    raw_data = {
        "patient_id": [1, 2, 3],
        "name": ["Alice", "Bob", "Charlie"],
        "age": [29, 35, 50],
        "diagnosis": ["Diabetes", "Hypertension", "Asthma"]
    }
    df = pd.DataFrame(raw_data)
    df.to_csv("/opt/airflow/dags/extracted_data.csv", index=False)
    print("✅ Data extracted and saved as CSV")

# -------------------------------
# Transform function
# -------------------------------
def transform_data(**kwargs):
    df = pd.read_csv("/opt/airflow/dags/extracted_data.csv")
    df['name'] = df['name'].str.upper()
    df['age_group'] = pd.cut(df['age'], bins=[0, 18, 35, 50, 100],
                             labels=['Child', 'Youth', 'Adult', 'Senior'])
    df.to_csv("/opt/airflow/dags/transformed_data.csv", index=False)
    print("✅ Data transformed and saved as CSV")

# -------------------------------
# Load function
# -------------------------------
def load_data(**kwargs):
    df = pd.read_csv("/opt/airflow/dags/transformed_data.csv")
    df.to_sql('patients', con=engine, if_exists='replace', index=False)
    print("✅ Data loaded into PostgreSQL")

# -------------------------------
# DAG definition
# -------------------------------
with DAG(
    dag_id='mediflow_etl',
    default_args=default_args,
    description='Mediflow ETL pipeline',
    schedule_interval='@daily',
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=['mediflow', 'etl'],
) as dag:

    extract_task = PythonOperator(
        task_id='extract',
        python_callable=extract_data,
    )

    transform_task = PythonOperator(
        task_id='transform',
        python_callable=transform_data,
    )

    load_task = PythonOperator(
        task_id='load',
        python_callable=load_data,
    )

    # Task order
    extract_task >> transform_task >> load_task
