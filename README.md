## Project Information
This project (POC) is designed to understand the integration of MLOps tools such as DVC, MLflow, and Apache Airflow, and to build an ETL pipeline so you can learn how to create an industry-grade ETL flow using these tools.

### ETL Pipeline Overview 🔧
In this ETL pipeline we perform the following steps:

1. **Data Extraction**: Extract data from the free NASA APOD API (you can also extract from databases, other APIs, or flat files). We first inspect the API response (for example via Postman) to decide which fields are important.

2. **Data Transformation**: Clean and pre-process the data and convert it to JSON so it can be stored in a database (`PostgreSQL`). I use the free NASA API: first we check responses in Postman to see what features the data contains and then decide which features/columns and data types we need when creating the database schema.

3. **Data Loading**: Load the transformed JSON data into a `PostgreSQL` database for storage and further analysis.

### Tools Used ✅
- **Apache Airflow / Astro** — for orchestrating and scheduling the ETL pipeline (deployed on AWS in this project).
- **MLflow** — for tracking experiments and model artifacts.
- **DVC** — we understand DVC but we are not implementing it in this ETL pipeline yet (Data Version Control is useful for dataset versioning and managing data dependencies).
- **Docker / Docker Compose** — to containerize services and run `PostgreSQL` locally or in deployment.

> Note: This ETL pipeline is also deployed on AWS using Docker Compose and Astro.

### Connections & Configuration 🔗
- **HTTP** connection for the NASA APOD API
- **PostgreSQL** connection for the database

Relevant files:
- `docker-compose.yml` (services)
- `airflow_settings.yaml` (Airflow config)
- `dags/etl.py` (ETL DAG)

### Quick Start — Run locally 💡
1. Install prerequisites: Docker & Docker Compose, Python (if running helpers locally).
2. Configure any environment variables / connections (HTTP, PostgreSQL).
3. Run `docker-compose up` to start services.
4. Check Airflow UI and trigger the `etl` DAG (see `dags/etl.py`).

### Notes & Tips 📝
- Always inspect API responses (Postman or curl) before finalizing the DB schema.
- Keep transformed data in JSON so it maps naturally to document-like fields and is easy to load into PostgreSQL JSON columns if needed.
- DVC can be added later to version large datasets and pipeline inputs — we currently only conceptually cover it.

Thank you for exploring this MLOps ETL pipeline project! Feel free to reach out for any questions or contributions. 🚀