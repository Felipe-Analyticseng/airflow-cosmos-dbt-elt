# Airflow + Cosmos + dbt ELT

Projeto local de ELT com Apache Airflow, Astronomer Cosmos, dbt e Postgres.

A DAG principal orquestra um pipeline dbt em camadas:

- `staging`
- `intermediate`
- `marts`

Dag principal:

```text
banking_medallion_cosmos_pipeline
```

## Pre-requisitos

Instale e deixe rodando:

- Docker Desktop
- Astronomer CLI (`astro`)

Para conferir se o `astro` esta instalado:

```powershell
astro version
```

Entre na pasta do projeto:

```powershell
cd "C:\Users\Felipe\Desktop\Felipe\Estudos\airflow-cosmos-dbt-elt"
```

## Subir o Airflow local

```powershell
astro dev start
```

Esse comando sobe os containers locais do Airflow:

- Postgres
- Scheduler
- DAG Processor
- API Server / UI
- Triggerer

A UI do Airflow fica em:

```text
http://localhost:8080
```

Se a porta `8080` estiver ocupada, o Astro mostra outra URL no terminal, por exemplo `http://localhost:11131`.

Login padrao:

```text
usuario: admin
senha: admin
```

## Comandos uteis do Airflow

Listar DAGs:

```powershell
astro dev run dags list
```

Disparar a DAG principal:

```powershell
astro dev run dags trigger banking_medallion_cosmos_pipeline
```

Ver logs dos containers:

```powershell
astro dev logs
```

Entrar no shell do container Airflow:

```powershell
astro dev bash
```

Parar o ambiente:

```powershell
astro dev stop
```

Parar e remover os volumes locais:

```powershell
astro dev kill
```

Use `astro dev kill` quando quiser limpar o banco local do Airflow/Postgres e recomecar do zero.

## Rodar comandos dbt

O dbt deste projeto roda dentro de um virtualenv criado no container:

```text
/usr/local/airflow/dbt_venv/bin/dbt
```

Com o Airflow ja rodando, entre no container:

```powershell
astro dev bash
```

Dentro do container, rode:

```bash
cd /usr/local/airflow/dbt
/usr/local/airflow/dbt_venv/bin/dbt deps --profiles-dir .
/usr/local/airflow/dbt_venv/bin/dbt debug --profiles-dir .
/usr/local/airflow/dbt_venv/bin/dbt seed --profiles-dir .
/usr/local/airflow/dbt_venv/bin/dbt run --profiles-dir .
/usr/local/airflow/dbt_venv/bin/dbt test --profiles-dir .
```

Comando completo para recriar tudo:

```bash
cd /usr/local/airflow/dbt
/usr/local/airflow/dbt_venv/bin/dbt deps --profiles-dir .
/usr/local/airflow/dbt_venv/bin/dbt seed --profiles-dir .
/usr/local/airflow/dbt_venv/bin/dbt run --profiles-dir . --full-refresh
/usr/local/airflow/dbt_venv/bin/dbt test --profiles-dir .
```

## Ver o pipeline/grafo do dbt

O comando que gera a documentacao e o grafo do dbt e:

```bash
dbt docs generate
```

Neste projeto, rode dentro do container:

```powershell
astro dev bash
```

Depois:

```bash
cd /usr/local/airflow/dbt
/usr/local/airflow/dbt_venv/bin/dbt deps --profiles-dir .
/usr/local/airflow/dbt_venv/bin/dbt docs generate --profiles-dir .
```

Isso cria os arquivos da documentacao em:

```text
dbt/target
```

Para abrir no navegador pelo Windows/PowerShell, em outro terminal local:

```powershell
cd "C:\Users\Felipe\Desktop\Felipe\Estudos\airflow-cosmos-dbt-elt\dbt\target"
python -m http.server 8081
```

Abra:

```text
http://localhost:8081
```

Na pagina do dbt Docs, use a area de lineage/grafo para ver o pipeline visual.

## Estrutura principal

```text
dags/
  banking_medallion_cosmos_pipeline.py

dbt/
  dbt_project.yml
  profiles.yml
  seeds/
  models/
    staging/
    intermediate/
    marts/
```

## Conexao local

O Airflow usa a connection local:

```text
conn_id: postgres_dbt
host: postgres
database: postgres
user: postgres
password: postgres
port: 5432
```

As variaveis locais ficam no arquivo `.env`, que nao deve ser enviado para o GitHub.
