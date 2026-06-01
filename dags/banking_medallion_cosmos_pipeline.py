from __future__ import annotations

from datetime import datetime
from pathlib import Path

from airflow import DAG
from airflow.operators.empty import EmptyOperator

from cosmos import DbtTaskGroup, ProjectConfig, ProfileConfig, ExecutionConfig, RenderConfig
from cosmos.constants import ExecutionMode, LoadMode
from cosmos.profiles import PostgresUserPasswordProfileMapping


AIRFLOW_HOME = Path("/usr/local/airflow")
DBT_PROJECT_PATH = AIRFLOW_HOME / "dbt"
DBT_EXECUTABLE_PATH = AIRFLOW_HOME / "dbt_venv" / "bin" / "dbt"


profile_config = ProfileConfig(
    profile_name="airflow_cosmos_dbt_elt",
    target_name="dev",
    profile_mapping=PostgresUserPasswordProfileMapping(
        conn_id="postgres_dbt",
        profile_args={
            "schema": "dbt",
        },
    ),
)

execution_config = ExecutionConfig(
    execution_mode=ExecutionMode.LOCAL,
    dbt_executable_path=str(DBT_EXECUTABLE_PATH),
)

render_config = RenderConfig(
    load_method=LoadMode.DBT_LS,
)

with DAG(
    dag_id="banking_medallion_cosmos_pipeline",
    description="Pipeline dbt com staging, intermediate e marts orquestrado com Astronomer Cosmos",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    tags=["cosmos", "dbt", "postgres", "staging", "intermediate", "marts"],
    default_args={
        "retries": 1,
    },
) as dag:

    start = EmptyOperator(task_id="start")

    dbt_cosmos_pipeline = DbtTaskGroup(
        group_id="dbt_cosmos_pipeline",
        project_config=ProjectConfig(
            dbt_project_path=DBT_PROJECT_PATH,
        ),
        profile_config=profile_config,
        execution_config=execution_config,
        render_config=render_config,
        operator_args={
            "install_deps": True,
            "full_refresh": True,
        },
    )

    end = EmptyOperator(task_id="end")

    start >> dbt_cosmos_pipeline >> end