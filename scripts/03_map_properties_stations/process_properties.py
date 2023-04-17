from types import NoneType

import pandas as pd
import numpy as np
import csv
from geopy.geocoders import Nominatim
from tqdm import tqdm

input_file = '../../data/properties/properties.csv'
output_file = '../../data/properties/properties_geo_coded.csv'  # 54495it [7:34:23,  2.00it/s]


def geo_code(input_file_, output_file_):
    df_properties = pd.read_csv(input_file_, low_memory=False)

    f = open(output_file_, 'w')
    writer = csv.writer(f)

    geolocator = Nominatim(timeout=10, user_agent="myGeolocator")

    df_properties = df_properties.replace(np.nan, '', regex=True)

    df_properties = df_properties.assign(latitude=0)
    df_properties = df_properties.assign(longitude=0)

    writer.writerow(df_properties.columns)

    for index, row in tqdm(df_properties.iterrows()):
        complete_address = [row.address_1, row.address_2, row.town, row.postcode, row.country]

        gcode = geolocator.geocode(complete_address, exactly_one=True, )

        if gcode is not None:
            row.latitude = gcode.latitude
            row.longitude = gcode.longitude
            writer.writerow(row)

    f.close()


geo_code(input_file, output_file)
