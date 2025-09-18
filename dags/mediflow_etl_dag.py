
```python
from datetime import datetime, timedelta
from airflow import DAG
from airflow.models.baseoperator import chain
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.utils.task_group import TaskGroup
from airflow.models import Variable

default_args = {
    "owner": "data-eng",
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
    "email_on_failure": True,
    "email": ["alerts@mediflow.local"],
    "sla": timedelta(hours=2),
}

BATCH_SIZE = int(Variable.get("BATCH_SIZE", 1000))

with DAG(
    dag_id="mediflow_etl_pipeline",
    start_date=datetime(2025, 1, 1),
    schedule_interval="@hourly",
    catchup=False,
    max_active_runs=1,
    default_args=default_args,
    tags=["mediflow","etl","healthcare"],
) as dag:

    validate_sources = DockerOperator(
        task_id="validate_sources",
        image="python:3.9-slim",
        command="python -m app.utils.validate_sources",
        docker_url="unix://var/run/docker.sock",
        auto_remove=True,
        network_mode="bridge",
        mounts=[],
        environment={"LOG_LEVEL": "INFO"},
    )

    with TaskGroup(group_id="extract") as extract:
        extract_ehr = DockerOperator(
            task_id="extract_ehr",
            image="mediflow-extract:latest",
            command=f"python -m app.extract.ehr --batch-size {BATCH_SIZE} --since {{ ds }}",
            docker_url="unix://var/run/docker.sock",
            auto_remove=True,
            network_mode="bridge",
            environment={"SOURCE": "ehr"},
        )

        extract_claims = DockerOperator(
            task_id="extract_claims",
            image="mediflow-extract:latest",
            command=f"python -m app.extract.claims --batch-size {BATCH_SIZE} --since {{ ds }}",
            docker_url="unix://var/run/docker.sock",
            auto_remove=True,
            network_mode="bridge",
            environment={"SOURCE": "claims"},
        )

        extract_lab = DockerOperator(
            task_id="extract_lab",
            image="mediflow-extract:latest",
            command=f"python -m app.extract.lab --batch-size {BATCH_SIZE} --since {{ ds }}",
            docker_url="unix://var/run/docker.sock",
            auto_remove=True,
            network_mode="bridge",
            environment={"SOURCE": "lab"},
        )

    transform_all = DockerOperator(
        task_id="transform_all",
        image="mediflow-transform:latest",
        command="python -m app.transform.run --window {{ ds }}",
        docker_url="unix://var/run/docker.sock",
        auto_remove=True,
        network_mode="bridge",
        environment={"ANONYMIZE_PII": "true"},
    )

    dq_checks = DockerOperator(
        task_id="dq_checks",
        image="mediflow-transform:latest",
        command="python -m app.transform.dq_gate --min-score 0.90 --window {{ ds }}",
        docker_url="unix://var/run/docker.sock",
        auto_remove=True,
        network_mode="bridge",
    )

    with TaskGroup(group_id="load") as load:
        load_patients = DockerOperator(
            task_id="load_patients",
            image="mediflow-load:latest",
            command="python -m app.load.run --table patients --mode upsert --window {{ ds }}",
            docker_url="unix://var/run/docker.sock",
            auto_remove=True,
            network_mode="bridge",
        )
        load_encounters = DockerOperator(
            task_id="load_encounters",
            image="mediflow-load:latest",
            command="python -m app.load.run --table encounters --mode upsert --window {{ ds }}",
            docker_url="unix://var/run/docker.sock",
            auto_remove=True,
            network_mode="bridge",
        )
        load_labs = DockerOperator(
            task_id="load_labs",
            image="mediflow-load:latest",
            command="python -m app.load.run --table lab_results --mode upsert --window {{ ds }}",
            docker_url="unix://var/run/docker.sock",
            auto_remove=True,
            network_mode="bridge",
        )

    finalize_audit = DockerOperator(
        task_id="finalize_audit",
        image="mediflow-load:latest",
        command="python -m app.load.finalize_audit --window {{ ds }}",
        docker_url="unix://var/run/docker.sock",
        auto_remove=True,
        network_mode="bridge",
        trigger_rule="all_done",
    )

    chain(validate_sources, extract, transform_all, dq_checks, load, finalize_audit)
```

---
