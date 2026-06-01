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

## Roteiro da demonstracao

Sequencia sugerida para apresentar o lab:

1. Subir o ambiente Astro.
2. Rodar o dbt geral.
3. Rodar o dbt por camadas.
4. Gerar e abrir o dbt Docs para mostrar o grafo.
5. Abrir o Airflow no navegador e disparar a DAG.

## 1. Subir o ambiente Astro

No PowerShell, dentro da pasta do projeto:

```powershell
astro dev start
```

Esse comando sobe os containers locais do Airflow:

- Postgres
- Scheduler
- DAG Processor
- API Server / UI
- Triggerer

Se a porta `8080` estiver ocupada, o Astro mostra outra URL no terminal, por exemplo `http://localhost:11131`.

Login padrao do Airflow:

```text
usuario: admin
senha: admin
```

## 2. Entrar no container do Airflow

Com o Astro rodando, entre no shell do container:

```powershell
astro dev bash
```

Dentro do container, entre na pasta do projeto dbt:

```bash
cd /usr/local/airflow/dbt
```

O executavel do dbt esta em:

```text
/usr/local/airflow/dbt_venv/bin/dbt
```

Para limpar o terminal dentro do container:

```bash
clear
```

## 3. dbt rodando geral

Dentro do container, rode:

```bash
cd /usr/local/airflow/dbt
/usr/local/airflow/dbt_venv/bin/dbt debug --profiles-dir .
/usr/local/airflow/dbt_venv/bin/dbt seed --profiles-dir .
/usr/local/airflow/dbt_venv/bin/dbt run --profiles-dir .
/usr/local/airflow/dbt_venv/bin/dbt test --profiles-dir .
```

Opcional, para recriar as tabelas do zero:

```bash
/usr/local/airflow/dbt_venv/bin/dbt run --profiles-dir . --full-refresh
```

## 4. dbt rodando por camadas

Rodar somente a camada `staging`:

```bash
/usr/local/airflow/dbt_venv/bin/dbt run --profiles-dir . --select staging
```

Rodar somente a camada `intermediate`:

```bash
/usr/local/airflow/dbt_venv/bin/dbt run --profiles-dir . --select intermediate
```

Rodar somente a camada `marts`:

```bash
/usr/local/airflow/dbt_venv/bin/dbt run --profiles-dir . --select marts
```

Rodar as camadas em sequencia para a demo:

```bash
cd /usr/local/airflow/dbt
/usr/local/airflow/dbt_venv/bin/dbt seed --profiles-dir .
/usr/local/airflow/dbt_venv/bin/dbt run --profiles-dir . --select staging
/usr/local/airflow/dbt_venv/bin/dbt run --profiles-dir . --select intermediate
/usr/local/airflow/dbt_venv/bin/dbt run --profiles-dir . --select marts
/usr/local/airflow/dbt_venv/bin/dbt test --profiles-dir .
```

## 5. Gerar e servir o dbt Docs

Dentro do container, gere a documentacao e o grafo:

```bash
cd /usr/local/airflow/dbt
/usr/local/airflow/dbt_venv/bin/dbt docs generate --profiles-dir .
```

O comando acima gera os arquivos em:

```text
/usr/local/airflow/dbt/target
```

Saia do container:

```bash
exit
```

No PowerShell, copie o `target` gerado no container para a pasta local do projeto.

Primeiro veja o id/nome do container:

```powershell
docker ps
```

Depois copie o `target`, trocando `<container_id>` pelo id do container onde voce rodou o `dbt docs generate`:

```powershell
docker cp <container_id>:/usr/local/airflow/dbt/target .\dbt\target
```

Entre na pasta local do `target`:

```powershell
cd "C:\Users\Felipe\Desktop\Felipe\Estudos\airflow-cosmos-dbt-elt\dbt\target"
```

Sirva os arquivos no navegador:

```powershell
python -m http.server 8081
```

Se `python` nao funcionar no Windows, use:

```powershell
py -m http.server 8081
```

Abra no navegador:

```text
http://localhost:8081
```

Na pagina do dbt Docs, use a area de lineage/grafo para mostrar o pipeline visual.

Observacao: o comando abaixo tambem existe, mas dentro do Docker/Astro pode falhar por porta ou bind de rede:

```bash
/usr/local/airflow/dbt_venv/bin/dbt docs serve --profiles-dir .
```

Por isso, para a demo, o fluxo mais confiavel e:

```text
dbt docs generate -> docker cp target -> python -m http.server 8081
```

## 6. Ativar o Airflow e rodar no browser

Abra a UI do Airflow no navegador.

URL padrao:

```text
http://localhost:8080
```

Se o Astro mostrar outra URL no terminal, use a URL exibida por ele.

Login:

```text
admin
admin
```

Na UI:

1. Procure a DAG `banking_medallion_cosmos_pipeline`.
2. Abra a DAG.
3. Clique no botao de play/trigger para executar.
4. Acompanhe pela Grid ou Graph View.
5. Clique nas tasks para ver os logs.

Tambem da para disparar pelo terminal:

```powershell
astro dev run dags trigger banking_medallion_cosmos_pipeline
```

Listar DAGs:

```powershell
astro dev run dags list
```

Ver erros de importacao de DAG:

```powershell
astro dev run dags list-import-errors
```

Ver logs dos containers:

```powershell
astro dev logs
```

## Parar ou limpar o ambiente

Parar o ambiente:

```powershell
astro dev stop
```

Parar e remover volumes locais:

```powershell
astro dev kill
```

Use `astro dev kill` quando quiser limpar o banco local do Airflow/Postgres e recomecar do zero.

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
