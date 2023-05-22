import csv
import datetime
import glob
import json
import os
import tqdm

from scripts.utils.functions import extract_parameter_list_from_files

json_base_directory = '../../data/json'
csv_base_directory = '../../data/csv'
today = datetime.date.today()
current_year = today.year
current_month = today.month


def convert(json_dir: str, csv_dir: str, years: int, p: str):
    # open the csv_separated file to write, it will consolidate all json files into one
    # with the name of the metric as column and the number of years
    csv_file_name = f'{csv_dir}/{p}_years_{str(years)}.csv'
    try:
        os.remove(csv_file_name)
        print(f'removed previous {csv_file_name} file')
    except FileNotFoundError:
        print(f'{csv_file_name} does not exist, no need to remove')

    with open(csv_file_name, 'w', newline='\n') as csv_file:

        # loop the writer
        writer = csv.writer(csv_file)

        # first line is the header
        header = ['ts_id',
                  'station_name',
                  'station_latitude',
                  'station_longitude',
                  'station_no',
                  'station_id',
                  'metric'
                  ]
        # possible parameters
        # we create a grid that can be filled or not
        # it is very important then the order
        for year in range(years):
            for month in range(12):
                new_col = str(year).zfill(2) + str(month).zfill(2)
                header.append(f'{p}_year_{new_col}')
                header.append(f'{p}_month_{new_col}')
                header.append(f'{p}_value_{new_col}')
                header.append(f'{p}_quality_code_{new_col}')

        writer.writerow(header)

        for metric in ['max', 'min']:
            # iterate over json station information
            json_dir_total = f'{json_dir}/{metric.lower()}'

            for filename in glob.glob(json_dir_total + '/*' + p + '.json'):
                # checking if it is a file
                if os.path.isfile(filename):
                    with open(filename) as json_file:
                        station_json_file = json.load(json_file)

                        data_row = [station_json_file['ts_id'],
                                    station_json_file['station_name'],
                                    station_json_file['station_latitude'],
                                    station_json_file['station_longitude'],
                                    station_json_file['station_no'],
                                    station_json_file['station_id'],
                                    metric
                                    ]

                        for month in station_json_file['data']:
                            data_row.append(month[0].split("-")[0])
                            data_row.append(month[0].split("-")[1])
                            data_row.append(month[1])
                            data_row.append(month[2])

                        writer.writerow(data_row)


parameter_list = extract_parameter_list_from_files('../../data/json/max')

for parameter in parameter_list:
    convert(json_base_directory, csv_base_directory, 5, parameter)
