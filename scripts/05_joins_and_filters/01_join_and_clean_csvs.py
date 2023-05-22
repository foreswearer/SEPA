import glob
import os
import warnings

import numpy as np
import pandas as pd
from tqdm import tqdm

from scripts.utils.functions import extract_parameter_list_from_files

csv_dir_total = '../../data/csv'

tqdm.pandas()

warnings.filterwarnings("ignore")

properties_file = '../../data/properties/properties_geo_coded_elevations.csv'
distances_file = '../../data/properties/property_distance_to_station_elevations.csv'


def process_data(station_info_file: str, p: str):
    df_stations = pd.read_csv(station_info_file, low_memory=False)
    df_stations = df_stations.replace(np.nan, 0, regex=True)

    columns_to_drop = ['ts_id',
                       'station_no',
                       'station_name',
                       'hamlet',
                       'suburb',
                       'village',
                       'state',
                       'postcode',
                       'country']
    df_stations.drop(columns_to_drop, axis='columns', inplace=True)

    station_id = df_stations.pop('station_id')
    df_stations.insert(0, 'station_id', station_id)
    del station_id
    df_properties = pd.read_csv(properties_file, low_memory=False)
    df_properties = df_properties.replace(np.nan, 0, regex=True)

    columns_to_drop = ['Result-State',
                       'Result-Detail',
                       'address_1',
                       'address_2',
                       'town',
                       'postcode',
                       'postcode']
    df_properties.drop(columns_to_drop, axis='columns', inplace=True)
    del columns_to_drop

    latitude = df_properties.pop('latitude')
    longitude = df_properties.pop('longitude')
    uprn = df_properties.pop('uprn')

    df_properties.insert(0, 'latitude', longitude)
    df_properties.insert(0, 'longitude', latitude)
    df_properties.insert(0, 'uprn', uprn)

    del latitude, longitude, uprn

    df_distances = pd.read_csv(distances_file, low_memory=False)
    df_distances = df_distances.replace(np.nan, 0, regex=True)

    result = pd.merge(df_properties, df_distances, on='uprn')

    result = pd.merge(result, df_stations, left_on=f'closest_{parameter}_station_id', right_on='station_id')

    file_prefix = os.path.splitext(station_info_file)[0].split('/')[4][:6]

    output_file = f'{csv_dir_total}/{file_prefix}_properties.csv'
    if os.path.exists(output_file):
        os.remove(output_file)
        print(f'removing previous {output_file}...')
    else:
        print(f'{output_file} does not exist, creating it...')
    result.to_csv(output_file, index=False)


parameter_list = extract_parameter_list_from_files('../../data/json/max')

for parameter in tqdm(parameter_list):

    for filename in glob.glob(f'{csv_dir_total}/{parameter}_years_5_geocoded.csv'):
        # checking if it is a file
        if os.path.isfile(filename):
            process_data(filename, parameter)
