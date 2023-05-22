import branca.colormap as cmp
import folium
import numpy as np
import pandas as pd

from scripts.utils.functions import extract_parameter_list_from_files

stations_file = '../../data/stations/stations.csv'
properties_file = '../../data/properties/properties_geo_coded.csv'
distances_file = '../../data/properties/property_distance_to_station.csv'

stations_map = folium.Map(prefer_canvas=True)

df_stations = pd.read_csv(stations_file, low_memory=False)
df_stations = df_stations.replace(np.nan, 0, regex=True)

df_properties = pd.read_csv(properties_file, low_memory=False)
df_properties = df_properties.replace(np.nan, 0, regex=True)

df_distances = pd.read_csv(distances_file, low_memory=False)
df_distances = df_distances.replace(np.nan, 0, regex=True)

df_p = df_properties[['uprn', 'latitude', 'longitude']]
del df_properties
df_s = df_stations[['station_id', 'station_latitude', 'station_longitude']]
del df_stations
df_p = pd.merge(df_p, df_distances, on='uprn')


def get_threshold(the_list: list, pct: int, bins: int):
    hist, edges = np.histogram(the_list, bins=bins, range=(0, max(the_list)), density=False)
    prop_n = len(df_p)
    pct10 = prop_n / (pct * bins)
    idx_min = next(x for x, val in enumerate(hist) if val < pct10)
    return edges[idx_min]


distance_linear_color = cmp.LinearColormap(
    ['green', 'red'],
    vmin=min(df_p.distance_Precip_km),
    vmax=get_threshold(df_p.distance_Precip_km, 10, 100),
    caption='distance to closest station'
)


def plot_stations(point):
    folium.CircleMarker(location=(point.station_latitude, point.station_longitude),
                        radius=3,
                        fill=True,
                        color='blue',
                        weight=1,
                        fill_opacity=0.8).add_to(folium.FeatureGroup(name='Stations').add_to(stations_map))


def plot_properties(point, parameter):
    folium.CircleMarker(location=(point.latitude, point.longitude),
                        radius=2,
                        fill=True,
                        color=distance_linear_color(point[f'distance_{parameter}_km']),
                        weight=1,
                        fill_opacity=0.8).add_to(
        folium.FeatureGroup(name=f'Properties distance to closest {parameter} in kilometers').add_to(stations_map))


df_s.apply(plot_stations, axis=1)

# loop all parameters to point sets of stations

parameter_list = extract_parameter_list_from_files('../../data/json/max')

for p in parameter_list:
    df_p.apply(lambda point: plot_properties(point, p), axis=1)

for style in ['openstreetmap',
              'stamenwatercolor',
              'stamenterrain',
              'stamentoner',
              'cartodbpositron'
              ]:
    folium.TileLayer(style).add_to(stations_map)

folium.LayerControl().add_to(stations_map)
stations_map.fit_bounds(stations_map.get_bounds())
stations_map.save(f'../../maps/stations.html')
