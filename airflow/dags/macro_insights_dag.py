# -*- coding: utf-8 -*-
# DAG: S3 → dbt (seed/run/test) daily

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    "owner": "macro_insights",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="macro_insights_daily",
    description="Upload raw to S3, then dbt seed/run/test in ClickHouse",
    schedule_interval="0 2 * * *",  # daily at 02:00 (Belgrade)
    start_date=datetime(2025, 10, 1),
    catchup=False,
    max_active_runs=1,
    default_args=default_args,
    tags=["macro_insights", "dbt", "s3"],
) as dag:

    # 1) Upload raw CSVs to S3 (берём AWS_* и S3_BUCKET из окружения контейнера)
    upload_to_s3 = BashOperator(
        task_id="upload_to_s3",
        bash_command=(
            # жёсткая проверка, что креды действительно есть в окружении задачи
            "set -euo pipefail; "
            "test -n \"${AWS_ACCESS_KEY_ID:-}\" || { echo 'AWS_ACCESS_KEY_ID is missing' >&2; exit 1; }; "
            "test -n \"${AWS_SECRET_ACCESS_KEY:-}\" || { echo 'AWS_SECRET_ACCESS_KEY is missing' >&2; exit 1; }; "

            # Region и bucket с понятными дефолтами
            "export AWS_DEFAULT_REGION=\"${AWS_DEFAULT_REGION:-eu-central-1}\"; "
            "export S3_BUCKET=\"${S3_BUCKET:-macro-insights-raw-data}\"; "

            # Запуск загрузчика
            "python /opt/airflow/scripts/upload_to_s3.py "
            "--bucket \"$S3_BUCKET\" "
            "--region \"$AWS_DEFAULT_REGION\" "
            "--local-dir /opt/airflow/dbt/seeds "
            "--prefix raw"
        ),
    )

    # Общий префикс для dbt-команд: укажем profiles dir, остальное dbt возьмёт из env (CH_HOST/CH_USER/CH_PASSWORD/CH_DATABASE)
    DBT_PREFIX = "set -euo pipefail; export DBT_PROFILES_DIR=/opt/airflow/dbt/.ci; cd /opt/airflow/dbt/.ci && "

    dbt_seed = BashOperator(
        task_id="dbt_seed",
        bash_command=DBT_PREFIX + "dbt seed --profiles-dir /opt/airflow/dbt/.ci",
    )

    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command=DBT_PREFIX + "dbt run --profiles-dir /opt/airflow/dbt/.ci",
    )

    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command=DBT_PREFIX + "dbt test --profiles-dir /opt/airflow/dbt/.ci",
    )

    upload_to_s3 >> dbt_seed >> dbt_run >> dbt_test