import glob
import os
import warnings

import numpy as np
import pandas as pd
from tqdm import tqdm

from scripts.utils.functions import extract_parameter_list_from_files


tqdm.pandas()

stations_file = '../../data/stations/stations_elevations.csv'
distances_file = '../../data/properties/property_distance_to_station.csv'

df_d = pd.read_csv(distances_file, low_memory=False)
df_d = df_d.replace(np.nan, 0, regex=True)

df_s = pd.read_csv(stations_file, low_memory=False)
df_s = df_s.replace(np.nan, 0, regex=True)[['station_id', 'elevation']]

id_cols = df_d.filter(regex='[az]*id$').columns

for col in id_cols:
    df_d = df_d.merge(df_s, how='left', left_on=col, right_on='station_id')
    new_col_name = f'{"_".join(col.split("_")[:-2])}_elevation'
    df_d['elevation'] = df_d['elevation'].round(2)
    df_d[new_col_name] = df_d['elevation']
    df_d.drop(['station_id', 'elevation'], axis='columns', inplace=True)

df_d.to_csv(f'{os.path.splitext(distances_file)[0]}_elevations.csv', index=False)

