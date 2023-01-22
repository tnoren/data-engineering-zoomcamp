services:
	postgres:
		image: postgres:13
	environment:
		POSTGRES USER: airflow
		POSTGRES PASSWORD: airflow
		POSTGRES DB: airflow
	volumes:
		- postgres-db-volume:/var/lib/postgresql/data
	healthcheck:
		test: ["CMD", "pg_isready", "-U", "airflow"]
		interval: 5s
		retries: 5
	restart: always


docker network create pg-network

docker run -it \
	-e POSTGRES_USER="root" \
	-e POSTGRES_PASSWORD="root" \
	-e POSTGRES_DB="ny_taxi" \
	-v c:/Users/user/git/data-engineering-zoomcamp/week_1_basics_n_setup/2_docker_sql/ny_taxi_postgres_data:/var/lib/postgresql/data \
	-p 5432:5432 \
	--network=pg-network \
	--name pg-database \
	postgres:13

docker run -it \
	-e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
	-e PGADMIN_DEFAULT_PASSWORD="root" \
	-p 8080:80 \
	--network=pg-network \
	--name pgadmin \
	dpage/pgadmin4

# Yellow
URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz"

docker build -t taxi_ingest:v001 .	
docker run -it \
	--network=pg-network \
	taxi_ingest:v001 \
	--user=root	\
	--password=root \
	--host=pg-database \
	--port=5432 \
	--db=ny_taxi \
	--table_name=yellow_taxi_data \
	--url=${URL}

# Green
URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-01.csv.gz"

docker build -t taxi_ingest:v001 .	
docker run -it \
	--network=pg-network \
	taxi_ingest:v001 \
	--user=root	\
	--password=root \
	--host=pg-database \
	--port=5432 \
	--db=ny_taxi \
	--table_name=green_taxi_data \
	--url=${URL}	

python notebook.py \
	--user=root	\
	--password=root \
	--host=localhost \
	--port=5432 \
	--db=ny_taxi \
	--table_name=yellow_taxi_data \
	--url=${URL}

docker build -t taxi_ingest:v001 .	

# Taxi zone lookup
URL="https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv"

docker build -t taxi_ingest:v001 .	
docker run -it \
	--network=pg-network \
	taxi_ingest:v001 \
	--user=root	\
	--password=root \
	--host=pg-database \
	--port=5432 \
	--db=ny_taxi \
	--table_name=taxi_zone_lookup \
	--url=${URL}


# generate .gitignore 
find * -size +50M | cat > .gitignore