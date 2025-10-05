# -*- coding: utf-8 -*-
# DAG: S3 → dbt (seed/run/test) → DQ → marts → (опц.) BI refresh
# Примечание: все секреты берём из переменных окружения контейнера (docker-compose .env)

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    "owner": "macro_insights",
    "depends_on_past": False,
    "retries": 2,                               # ← как просили
    "retry_delay": timedelta(minutes=3),        # ← как просили
    # если захочешь email-алерты — заполни список и включи smtp в Airflow
    # "email": ["your_email@example.com"],
    # "email_on_failure": True,
}

with DAG(
    dag_id="macro_insights_daily",
    description="Upload raw to S3 → dbt seed/run/test → DQ → marts → (opt) BI refresh",
    schedule_interval="0 2 * * *",   # ежедневно в 02:00
    start_date=datetime(2025, 10, 1),
    catchup=False,
    max_active_runs=1,
    default_args=default_args,
    tags=["macro_insights", "dbt", "s3"],
) as dag:

    # 1) Загрузка сырых CSV в S3
    # Берём регион из ENV (AWS_DEFAULT_REGION), по умолчанию eu-central-1
    upload_to_s3 = BashOperator(
        task_id="upload_to_s3",
        bash_command=(
            "set -euo pipefail; "
            "python /opt/airflow/scripts/upload_to_s3.py "
            "--bucket macro-insights-raw-data "
            "--region ${AWS_DEFAULT_REGION:-eu-central-1} "
            "--local-dir /opt/airflow/dbt/seeds "
            "--prefix raw "
        ),
    )

    # 2) dbt seed (используем наш CI-профиль)
    dbt_seed = BashOperator(
        task_id="dbt_seed",
        bash_command=(
            "set -euo pipefail; "
            "cd /opt/airflow/dbt/.ci && dbt seed --profiles-dir /opt/airflow/dbt/.ci"
        ),
    )

    # 3) Основные трансформации
    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command=(
            "set -euo pipefail; "
            "cd /opt/airflow/dbt/.ci && dbt run --profiles-dir /opt/airflow/dbt/.ci"
        ),
    )

    # 4) Базовые тесты
    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command=(
            "set -euo pipefail; "
            "cd /opt/airflow/dbt/.ci && dbt test --profiles-dir /opt/airflow/dbt/.ci"
        ),
    )

    # 5) Дополнительный слой Data Quality (тесты с тегом dq)
    dq_check = BashOperator(
        task_id="dq_check",
        bash_command=(
            "set -euo pipefail; "
            "cd /opt/airflow/dbt/.ci && dbt test --select tag:dq --profiles-dir /opt/airflow/dbt/.ci"
        ),
    )

    # 6) Построение витрин (модели с тегом mart)
    build_marts = BashOperator(
        task_id="build_marts",
        bash_command=(
            "set -euo pipefail; "
            "cd /opt/airflow/dbt/.ci && dbt run --select tag:mart --profiles-dir /opt/airflow/dbt/.ci"
        ),
    )

    # 7) (Опционально) Обновление BI/кешей — запустится, только если файл существует
    refresh_bi = BashOperator(
        task_id="refresh_bi",
        bash_command=(
            "set -euo pipefail; "
            "if [ -f /opt/airflow/scripts/refresh_bi.py ]; then "
            "  python /opt/airflow/scripts/refresh_bi.py; "
            "else "
            "  echo 'No refresh_bi.py found, skipping'; "
            "fi"
        ),
        trigger_rule="all_done",  # можно сменить на "all_success", если нужно строгость
    )

    upload_to_s3 >> dbt_seed >> dbt_run >> dbt_test >> dq_check >> build_marts >> refresh_bi