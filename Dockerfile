FROM quay.io/astronomer/astro-runtime:12.1.1

USER root

RUN python -m venv /usr/local/airflow/dbt_venv \
    && /usr/local/airflow/dbt_venv/bin/pip install --no-cache-dir --upgrade pip \
    && /usr/local/airflow/dbt_venv/bin/pip install --no-cache-dir dbt-core==1.9.0 dbt-postgres==1.9.0

USER astro
