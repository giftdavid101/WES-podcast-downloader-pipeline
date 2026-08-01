from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator


default_args = {
    "owner": "gift",
    "depends_on_past": False,
    "retries": 1,
}

with DAG(
    dag_id="podcast_downloader_pipeline",
    description="Mental Health Podcast Data Pipeline",
    default_args=default_args,
    start_date=datetime(2026, 7, 31),
    schedule=None,
    catchup=False,
    tags=["podcast", "mental-health"],
) as dag:

    fetch_metadata = BashOperator(
        task_id="fetch_metadata",
        bash_command="python /opt/airflow/scripts/fetch_feed.py",
    )

    transform_silver = BashOperator(
        task_id="transform_silver",
        bash_command="python /opt/airflow/scripts/transform_silver.py",
    )

    build_gold = BashOperator(
        task_id="build_gold",
        bash_command="python /opt/airflow/scripts/build_gold.py",
    )

    fetch_metadata >> transform_silver >> build_gold