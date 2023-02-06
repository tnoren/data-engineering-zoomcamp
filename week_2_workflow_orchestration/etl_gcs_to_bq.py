from pathlib import Path
from prefect import  flow, task
from prefect_gcp import GcpCredentials
from prefect_gcp.cloud_storage import GcsBucket
import pandas as pd



@task(log_prints=True)
def extract_from_gcs(color:str, year:int, month:int) -> Path:
    """Download trip data from GCS"""
    gcs_path = f'data/{color}/{color}_tripdata_{year}-{month:02}'
    gcs_block = GcsBucket.load('zoom-gcs')
    gcs_block.get_directory(from_path=gcs_path, local_path=f'./')
    
    return Path(f'{gcs_path}')

@task(log_prints=True)    
def transform(path: Path) -> pd.DataFrame:
    """Data cleaning example"""
    df = pd.read_parquet(f'{path}.parquet')
    print(f'pre: missing passenger count: {df["passenger_count"].isna().sum()}')
    df['passenger_count'].fillna(0, inplace=True)
    print(f'post: missing passenger count: {df["passenger_count"].isna().sum()}')
    
    return df

@task(log_prints=True)
def write_bq(df: pd.DataFrame) -> None:
    """Write DataFrame to BigQuery"""

    gcp_cred_block = GcpCredentials.load('zoom-gcp-creds')
    cred = gcp_cred_block.get_credentials_from_service_account()

    df.to_gbq(
        destination_table='zoomcamp.rides',
        # project_id='dtc-de-course-375300',
        credentials=cred,
        chunksize=500_000,
        if_exists='append',
        progress_bar=True
    )

@flow(log_prints=True)
def etl_gcs_to_bq():
    """Main ETL flow to load data to Big Query"""
    color = 'yellow'
    year = 2021
    month= 1

    path = extract_from_gcs(color, year, month)
    df = transform(path)
    write_bq(df)

if __name__ == '__main__':
    etl_gcs_to_bq()