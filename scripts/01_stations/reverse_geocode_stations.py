import pandas as pd
from geopy.geocoders import Nominatim

df = pd.read_csv('../../data/csv/min_5.csv')

locator = Nominatim(user_agent='myGeocoder')


def get_data_from_location(station):
    location = locator.reverse(station)

    variables = ['suburb', 'village', 'state', 'postcode', 'country']

    try:
        for v in variables:
            globals()[f"{v}"] = location.raw['address'][v]
    except KeyError:
        globals()[f"{v}"] = ''

    location_data = {
        'suburb': globals()['suburb'],
        'village': globals()['village'],
        'state': globals()['state'],
        'postcode': globals()['postcode'],
        'country': globals()['country']
    }

    return pd.Series(location_data)


df[['suburb', 'village', 'state', 'postcode', 'country']] = df.apply(
    lambda row: get_data_from_location([row.station_latitude, row.station_longitude]), axis=1)

df.to_csv('../../data/01_stations/01_stations.csv', index=None)
