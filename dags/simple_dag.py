from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def print_hello():
    print("Hello from Airflow DAG!")

with DAG(
    dag_id="simple_dag",
    start_date=datetime(2025, 9, 10),
    schedule_interval="@daily",
    catchup=False,
) as dag:

    hello_task = PythonOperator(
        task_id="hello_task",
        python_callable=print_hello,
    )
