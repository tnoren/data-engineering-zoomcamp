##2. Introduction to Prefect concepts##


```bash
docker run -it \
	-e POSTGRES_USER="root" \
	-e POSTGRES_PASSWORD="root" \
	-e POSTGRES_DB="ny_taxi" \
	-v c:/Users/user/git/data-engineering-zoomcamp/week_1_basics_n_setup/2_docker_sql/ny_taxi_postgres_data:/var/lib/postgresql/data \
	-p 192.168.1.57:5432:5432 \
	--network=pg-network \
	--name pg-database \
	postgres:13


docker run -it \
	-e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
	-e PGADMIN_DEFAULT_PASSWORD="root" \
	-p 192.168.1.57:8080:80 \
	--network=pg-network \
	--name pgadmin \
	dpage/pgadmin4

cd C:\Users\user\git\data-engineering-zoomcamp\week_2_workflow_orchestration

docker build -t prefect_ingest:v001 .

docker run -it \
	-p 192.168.1.57:4200:4200 \
	--network=pg-network \
	prefect_ingest:v001

docker container ls

docker exec c55ec7858815 prefect config set PREFECT_API_URL="http://192.168.1.57:4200/api"
docker exec c55ec7858815 prefect orion start --host 0.0.0.0

http://192.168.1.57:4200/blocks/catalog/sqlalchemy-connector/create

Block Name -> postgres-connector
Driver -> SyncDriver -> postgresql+psycopg2

postgres-connectorpostgres-connector    
```


#etl_web_to_gcs#
https://youtu.be/W-rMz_2GwqQ?list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&t=549