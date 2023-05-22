import os

import numpy as np
import pandas as pd
import requests
from tqdm import tqdm

tqdm.pandas()


def get_elevation_from_location(location: str):
    response = requests.get(f'https://api.opentopodata.org/v1/eudem25m?locations={location}')
    data = response.json()

    return data['results'][0]['elevation']


def get_elevations_stations(csv_file: str):
    df = pd.read_csv(csv_file, low_memory=False)
    df = df.replace(np.nan, 0, regex=True)
    if not df.empty:
        df['elevation'] = df.progress_apply(
            lambda row: get_elevation_from_location(f'{row.station_latitude},{row.station_longitude}'), axis=1)

        df.to_csv(f'{os.path.splitext(csv_file)[0]}_elevations.csv', index=False)


def get_elevations_properties(csv_file: str):
    df = pd.read_csv(csv_file, low_memory=False)
    df = df.replace(np.nan, 0, regex=True)
    if not df.empty:
        df['elevation'] = df.progress_apply(
            lambda row: get_elevation_from_location(f'{row.latitude},{row.longitude}'), axis=1)

        df.to_csv(f'{os.path.splitext(csv_file)[0]}_elevations.csv', index=False)


# get stations elevation
print(f'getting stations elevation')
get_elevations_stations('../../data/stations/stations.csv')

# get properties elevation
print(f'getting properties elevation')
get_elevations_properties('../../data/properties/properties_geo_coded.csv')

