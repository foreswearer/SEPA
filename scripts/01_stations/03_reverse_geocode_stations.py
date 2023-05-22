import glob
import os

import numpy as np
import pandas as pd
from geopy.geocoders import Nominatim
from tqdm import tqdm

from scripts.utils.functions import extract_parameter_list_from_files

locator = Nominatim(user_agent='myGeocoder')

csv_dir_total = '../../data/csv'

tqdm.pandas()


def get_data_from_location(station):
    location = locator.reverse(station)

    variables = ['hamlet', 'suburb', 'village', 'state', 'postcode', 'country']

    for v in variables:
        try:
            globals()[f"{v}"] = location.raw['address'][v]
        except KeyError:
            globals()[f"{v}"] = ''

    location_data = {
        'hamlet': globals()['hamlet'],
        'suburb': globals()['suburb'],
        'village': globals()['village'],
        'state': globals()['state'],
        'postcode': globals()['postcode'],
        'country': globals()['country']
    }

    return pd.Series(location_data)


parameter_list = extract_parameter_list_from_files('../../data/json/max')


def get_geo_info(csv_file: str):
    df = pd.read_csv(csv_file, low_memory=False)
    df = df.replace(np.nan, 0, regex=True)
    if not df.empty:
        df[['hamlet', 'suburb', 'village', 'state', 'postcode', 'country']] = df.progress_apply(
            lambda row: get_data_from_location([row.station_latitude, row.station_longitude]), axis=1)

        df.to_csv(f'{os.path.splitext(csv_file)[0]}_geocoded.csv', index=False)


json_base_directory = '../../data/json'

for parameter in parameter_list:

    for filename in glob.glob(csv_dir_total + f'/{parameter}_years_5.csv'):
        # checking if it is a file
        if os.path.isfile(filename):
            get_geo_info(filename)
