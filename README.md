# Mediflow ETL Pipeline

A complete end-to-end ETL pipeline for healthcare data (**extract → transform → load**) with:

- **Apache Airflow** for orchestration  
- **PostgreSQL** as the target database  
- **Prometheus + Grafana** for monitoring and visualization  
- **Docker Compose** for containerized deployment  

---

## 🚀 Quick Start (Local Development)

> Run from the repo root. Tested on Linux / WSL / macOS.

### 1️⃣ Setup environment
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 2️⃣ Prepare data directories
```
mkdir -p data/raw data/processed data/transformed
touch data/raw/.gitkeep data/processed/.gitkeep data/transformed/.gitkeep
```

### 3️⃣ Configure environment variables
```
cp .env.example .env
# edit .env with database credentials, SECRET_KEY, etc.
export $(grep -v '^#' .env | xargs)
```

### 4️⃣ Start Airflow + Monitoring
```
cd docker/airflow
docker compose up -d
```

### 5️⃣ Initialize Airflow database (only first time)
docker compose exec airflow-init airflow db init
docker compose exec airflow-webserver airflow users create \
  --username admin \
  --firstname Admin \
  --lastname User \
  --role Admin \
  --email admin@example.com \
  --password admin

### 6️⃣ (Optional) Build ETL images for DockerOperator
```
docker build -t mediflow-extract:latest docker/extract
docker build -t mediflow-transform:latest docker/transform
docker build -t mediflow-load:latest docker/load
```

### 🌐 Access Services

Airflow UI → http://localhost:8080
 (login: admin/admin)

Grafana → http://localhost:3000
 (login: admin/admin)

Prometheus → http://localhost:9090

### 🔄 Run ETL Manually (without Airflow)
# 1. Extract
```
python scripts/extract.py
```

# 2. Transform
```
python scripts/transform.py
```

# 3. Load into Postgres
```
python scripts/load.py
```

### 🧪 Running Tests
```
pytest tests/
```

### 📊 Monitoring Setup

Prometheus scrapes Airflow and system metrics (prometheus.yml config).

Grafana dashboard (airflow_dashboard.json) visualizes:

DAG run stats

Task durations

Success/failure counts

### 📁 Required Files Before Running
.env.example (placeholder secrets) → create your .env file from this.
.gitkeep in data/raw, data/processed, data/transformed to keep dirs in Git.
docker/extract, docker/transform, docker/load (if running ETL via DockerOperator).
docker/airflow/init.sql if initializing DB schema manually.

### ⚙️ Troubleshooting
- ** Airflow "database not initialized" → run docker compose exec airflow-init airflow db init.**
- ** Permission denied: /opt/airflow/logs → fix log folder permissions:**
- ** sudo chmod -R 777 docker/airflow/logs**

Prometheus config error → ensure prometheus.yml path is valid in docker-compose.yml.
Grafana no dashboards → ensure grafana/provisioning is mounted correctly.

### 🛡️ Security Notes

Never commit .env with real credentials.
Use strong values for SECRET_KEY and FERNET_KEY.
For production, store secrets in Vault, AWS Secrets Manager, or Kubernetes Secrets.



👤 Author
Udit Pandey
Computer Engineering Graduate | Data & Software Projects

---
