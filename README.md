# Mediflow ETL Pipeline

An end-to-end **ETL pipeline** for healthcare data (Extract → Transform → Load) orchestrated with **Apache Airflow**, with monitoring using **Prometheus + Grafana**, and **PostgreSQL** as the target database.

---

## 📂 Project Structure
mediflow-etl-pipeline/
│
├── dags/
│ ├── simple_dag.py
│ ├── mediflow_etl_dag.py
│ └── init.py
│
├── data/
│ ├── raw/ # inbound extracts
│ ├── processed/ # intermediate files
│ └── transformed/ # final transformed data
│
├── docker/airflow/
│ ├── docker-compose.yml
│ ├── prometheus.yml
│ ├── grafana/
│ │ ├── provisioning/
│ │ │ ├── datasources/
│ │ │ │ └── datasource.yml
│ │ │ └── dashboards/
│ │ │ └── dashboard.yml
│ │ ├── dashboards/
│ │ │ └── airflow_dashboard.json
│ │ └── Dockerfile
│
├── scripts/
│ ├── extract.py
│ ├── transform.py
│ ├── load.py
│ └── utils.py
│
├── tests/
│ └── test_data_quality.py
│
├── requirements.txt
├── README.md
└── .gitignore


> **Note:** Add `.gitkeep` files in empty folders (`data/raw`, `data/processed`, `data/transformed`) to ensure they exist in git.  

---

## 🚀 Getting Started (Local Development)

### 1. Clone repo
git clone https://github.com/<your-username>/mediflow-etl-pipeline.git
cd mediflow-etl-pipeline

### 2. Setup Python environment
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

### 3. Environment variables

Copy .env.example → .env and update with real values:

SECRET_KEY=changeme
POSTGRES_USER=airflow
POSTGRES_PASSWORD=airflow
POSTGRES_DB=airflow


Load them:

export $(grep -v '^#' .env | xargs)

### 4. Start Airflow & services
cd docker/airflow
docker compose up -d


Initialize Airflow DB (only first time):

docker compose exec airflow-init airflow db init
docker compose exec airflow-webserver airflow users create \
  --username admin \
  --firstname Admin \
  --lastname User \
  --role Admin \
  --email admin@example.com \
  --password admin

### 5. Build ETL images (if using DockerOperator)
docker build -t mediflow-extract:latest docker/extract
docker build -t mediflow-transform:latest docker/transform
docker build -t mediflow-load:latest docker/load

### 🌐 Access Services
Airflow UI: http://localhost:8080

login → admin / admin

Grafana: http://localhost:3000

login → admin / admin

Prometheus: http://localhost:9090

### ⚙️ Running ETL manually (without Airflow)

### Extract:
python scripts/extract.py

### Transform:
python scripts/transform.py

### Load:
python scripts/load.py

### 🧪 Run Tests
pytest tests/

### 📊 Monitoring
Metrics are exported to Prometheus.
Dashboards are available in Grafana (docker/airflow/grafana/dashboards/airflow_dashboard.json).
You can import the JSON into Grafana or let provisioning handle it.

### 🛠 Troubleshooting
service "airflow-webserver" is not running
### Check logs:
docker compose logs airflow-webserver

Usually caused by DB not being initialized (airflow db init) or permission issues with mounted logs/.

### Log permission errors
Ensure docker/airflow/logs/ is writable by container UID (default 50000):

sudo chown -R 50000:0 docker/airflow/logs


### Prometheus config errors
Ensure prometheus.yml is a valid file and mapped correctly in docker-compose.yml.

### 📄 Requirements
See requirements.txt
. Includes:
apache-airflow==2.7.1
pandas
sqlalchemy
psycopg2-binary
prometheus-client
pytest
docker

### 🔐 Security
Do not commit .env with real secrets.

Use AIRFLOW__CORE__FERNET_KEY in production.

Manage secrets via Vault / AWS SSM for production.

### 📌 Roadmap

 Local Airflow DAGs

 ETL scripts (extract, transform, load)

 Docker Compose stack with Airflow + Postgres + Grafana + Prometheus

 Add CI/CD workflow (.github/workflows/ci.yml)

 Add Kubernetes deployment

### 👤 Author
Udit Pandey
Computer Science Engineering Graduate | Data Science & ETL Projects

---
