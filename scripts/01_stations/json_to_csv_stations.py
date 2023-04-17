import csv
import datetime
import json
import os

json_base_directory = '../../data/json'
today = datetime.date.today()
current_year = today.year
current_month = today.month


def convert(json_dir: str, csv_dir: str, metric: str, years: int):
    # open the csv file to write, it will consolidate all json files into one
    # with the name of the metric and the number of years
    csv_file_name = f'{csv_dir}/{metric}_{str(years)}.csv'
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
                  ]

        for year in range(years):
            for month in range(12):
                new_col = str(year + month).zfill(3)
                header.append(f'year_{new_col}')
                header.append(f'month_{new_col}')
                header.append(f'value_{new_col}')
                header.append(f'quality_code_{new_col}')

        writer.writerow(header)

        # iterate over json station information
        json_dir_total = f'{json_dir}/{metric.lower()}'
        for filename in os.listdir(json_dir_total):
            f = os.path.join(json_dir_total, filename)

            # checking if it is a file
            if os.path.isfile(f):
                with open(f) as json_file:
                    station_json_file = json.load(json_file)
                    for key in station_json_file:
                        exec('{KEY} = {VALUE}'.format(KEY=key, VALUE=repr(station_json_file[key])))

                    data_row = [station_json_file['ts_id'],
                                station_json_file['station_name'],
                                station_json_file['station_latitude'],
                                station_json_file['station_longitude'],
                                station_json_file['station_no'],
                                station_json_file['station_id'],
                                ]

                    for month in station_json_file['data']:
                        data_row.append(month[0].split("-")[0])
                        data_row.append(month[0].split("-")[1])
                        data_row.append(month[1])
                        data_row.append(month[2])

                    writer.writerow(data_row)


convert('../../data/json', '../../data/csv', 'min', 5)
convert('../../data/json', '../../data/csv', 'max', 5)
