
# 📊 Macro Insights — Data Platform MVP

End-to-end data platform prototype for macroeconomic analytics, built as a **minimal viable product (MVP)**.
The pipeline ingests raw data from API sources into **Amazon S3**, transforms it with **dbt**, and loads it into **ClickHouse** — ready for BI tools like **DataLens** or **Metabase**.

---

## 🚀 Architecture Overview

```mermaid
graph TD
    A[🌐 API Data Sources] --> B[S3 Bucket (raw)]
    B --> C[dbt: Transform & Model Data]
    C --> D[ClickHouse: Data Warehouse]
    D --> E[📊 BI Tools: Analytics & Dashboards]
```

---

## ⚙️ Pipeline Components

| Component        | Description                                                                 |
|------------------|-----------------------------------------------------------------------------|
| **S3**           | Raw data landing zone (e.g., GDP data from public APIs).                    |
| **dbt**          | Transformation, data modeling, and data quality tests.                     |
| **ClickHouse**   | High-performance analytical data warehouse.                                 |
| **Airflow**      | Orchestration: triggers data load, transformation, and validation tasks.   |
| **BI Tools**     | Visualization and insights (e.g., Yandex DataLens, Metabase).              |

✅ **MVP Pipeline Summary:**
API → S3 → dbt → ClickHouse → BI-ready

---

## 📸 Screenshots

### ✅ Airflow DAG — Successful Run
![Airflow DAG](assets/airflow_dag_run_success.png)

### 📁 S3 — Raw Data Landing
![S3 Bucket](assets/S3.png)

### 🗄️ ClickHouse — Analytical Table
![ClickHouse Table](assets/ClickHouse.png)

---

## 📊 Data Flow Example

1. `gdp.csv` is uploaded to S3 (`raw/YYYY-MM-DD/gdp.csv`).
2. dbt transforms the raw GDP data into a staging table (`stg_gdp`).
3. Final fact table (`fct_gdp_yoy`) calculates **year-over-year GDP growth**.
4. BI tools connect directly to ClickHouse for dashboards and analysis.

---

## 🧪 Data Quality

We use **dbt tests** to ensure data quality:

- `NOT NULL` checks for key fields
- Range validation for numeric values
- Custom test: no negative GDP values

Example custom test:

```sql
-- tests/non_negative_gdp.sql
SELECT *
FROM {{ ref('stg_gdp') }}
WHERE gdp_usd_bn < 0
```

---

## 🛠️ How to Run Locally

Clone the repo:

```bash
git clone https://github.com/eduardserbia/macro-insights.git
cd macro-insights
```

Start the stack:

```bash
docker compose up -d --build
```

Trigger the DAG:

```bash
docker compose exec airflow-webserver bash
airflow dags trigger macro_insights_daily
```

---

## 📈 Future Enhancements

- Add additional macroeconomic indicators (e.g., CPI, inflation)
- Build combined analytical marts with multiple metrics
- Add incremental loads
- Integrate CI/CD workflows for dbt
- Deploy to a managed Airflow environment (Astronomer / MWAA)

---

## 👤 Author

**Eduard Nikolaev** — Data Platform Architect / DataOps Engineer
🔗 [LinkedIn](https://www.linkedin.com/in/eduard-nikolaev/)
📍 Macro Insights — Data Platform MVP

---

## 📜 License

MIT License © 2025 Eduard Nikolaev
