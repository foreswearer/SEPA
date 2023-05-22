import glob
import os

import geopy.distance
import numpy as np
import pandas as pd
from tqdm import tqdm

from scripts.utils.functions import extract_parameter_list_from_files

csv_dir_total = '../../data/csv'
stations_file = '../../data/stations/stations.csv'
properties_file = '../../data/properties/properties_geo_coded.csv'
distances_file = '../../data/properties/property_distance_to_station.csv'

df_stations = pd.read_csv(stations_file, low_memory=False)
df_stations = df_stations.replace(np.nan, 0, regex=True)

# add as columns as parameters with booleans if they have or not the parameter

parameter_list = extract_parameter_list_from_files('../../data/json/max')

df_stations = df_stations[['station_id', 'station_latitude', 'station_longitude']]

df_properties = pd.read_csv(properties_file, low_memory=False)
df_properties = df_properties.replace(np.nan, 0, regex=True)
df_properties = df_properties[['uprn', 'latitude', 'longitude']]

del stations_file, properties_file

# TODO automate creation of columns based on parameters. Now it's manual and hardcoded
df = pd.DataFrame(columns=['uprn'] +
                          [f'closest_{p}_station_id' for p in parameter_list] +
                          [f'distance_{p}_km' for p in parameter_list])

for _, prop in tqdm(df_properties.iterrows()):

    coords_p = (prop.latitude, prop.longitude)

    distances = []
    station_ids = []
    closest_id_station = None
    distance_km = None

    # get lists of stations per parameter
    for p in parameter_list:

        # initialize for each p
        distances = []
        station_ids = []
        closest_id_station = None
        distance_km = None

        for filename in glob.glob(csv_dir_total + f'/{p}_years_5.csv'):
            # checking if it is a file
            if os.path.isfile(filename):
                df1 = pd.read_csv(filename)
                df_stations[p] = df_stations.apply(lambda row: np.int64(row.station_id) in list(df1.station_id),
                                                   axis='columns')
            del df1
        # transpose and drop first column (the name of the variables) it looks like
        # and filtering by stations with this type of parameter
        df_stations_t = df_stations[df_stations[p]].set_index('station_id').T.rename_axis('station_id').reset_index()
        df_stations_t = df_stations_t.iloc[:2, 1:]
        df_stations_t = df_stations_t.astype(str)

        # creating a list of dataframe columns
        columns_stations = list(df_stations_t)

        for i in columns_stations:
            coords_s = (df_stations_t[i][0], df_stations_t[i][1])
            distances.append(geopy.distance.geodesic(coords_p, coords_s).km)
            station_ids.append(i)
        distance_km = min(distances)
        closest_station_index = distances.index(distance_km)
        globals()[f'distance_{p}_km'] = distance_km
        globals()[f'closest_{p}_station_id'] = station_ids[closest_station_index]

    df.loc[len(df)] = [prop.uprn] + [globals()[f'closest_{p}_station_id'] for p in parameter_list] + [
        globals()[f'distance_{p}_km'] for p in parameter_list]

df['uprn'] = np.floor(df['uprn']).astype(int)
for p in parameter_list:
    df[f'closest_{p}_station_id'] = np.floor(df[f'closest_{p}_station_id']).astype(int)
    df[f'distance_{p}_km'] = np.floor(df[f'distance_{p}_km']).round(2)

df.to_csv(distances_file, index=False)
