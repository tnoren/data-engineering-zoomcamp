from pathlib import Path
from prefect import  flow, task
from prefect_gcp.cloud_storage import GcsBucket
import pandas as pd

@task(name='Fetch dataset')
def fetch(dataset_url:str) -> pd.DataFrame:
    """Read taxi data from web into pandas DataFrame"""

    df = pd.read_csv(dataset_url)

    return df



@flow(name='etl_web_to_gcs')
def etl_web_to_gcs() -> None:
    """The main ETL function"""
    color = 'yellow'
    year = 2021
    month = 1
    dataset_file = f'{color}_tripdata_{year}-{month:02}'
    dataset_url = f'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/{color}/{dataset_file}.csv.gz'
    test =        'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-01.csv.gz'

    print(test)
    print(dataset_url)

    df = fetch(dataset_url)

if __name__ == '__main__':
    etl_web_to_gcs()