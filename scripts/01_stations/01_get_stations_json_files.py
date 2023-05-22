import json
import requests


def get_header_token():
    # specify target, key, header - N.B. set access_key to value issued to you
    token_url = 'https://timeseries.sepa.org.uk/KiWebPortal/rest/auth/oidcServer/token'
    access_key = 'Njc1YjIxZjgtNjQwOC00MGJiLWJjMTMtMTU2YWUzNGY1MGFkOjk5ZmU4Zjg2LTg0NTEtNDZmOS1hYTAxLWFlYjE4YjM3M2QxOQ=='
    auth_headers = {'Authorization': 'Basic ' + access_key}
    # POST token request to return response object
    response_token = requests.post(token_url, headers=auth_headers, data='grant_type=client_credentials')
    # retrieve access token from response object
    access_token = response_token.json()['access_token']
    # specify header
    head_dict = {'Authorization': 'Bearer ' + access_token}
    return head_dict


def get_time_series_url(years: int,
                        metric: str,
                        output_format: str,
                        return_fields: list[str]):
    # convert list to string with comma separated values
    return_fields = ','.join([str(elem) for elem in return_fields])

    url = (
        f'https://timeseries.sepa.org.uk/KiWIS/KiWIS?'
        f'service=kisters&'
        f'type=queryServices'
        f'&datasource=0&'
        f'request=gettimeseriesvalues&'
        f'metadata=true&'
        f'returnfields={return_fields}&'
        f'ts_path=1/*/*/LTV.HMonth.{metric}&'
        f'period=P{str(years)}Y&'
        f'format={output_format}'
    )

    return url


def get_timeseries_to_json_file(years: int,
                                metric: str,
                                directory_name: str):

    return_fields = ['Timestamp', 'Value', 'Quality Code']

    # Specify request URL
    request_url = get_time_series_url(years, metric, 'json', return_fields)
    head_dict = get_header_token()

    # GET data request as response object
    response_data = requests.get(request_url, headers=head_dict)

    # retrieve JSON data from response object
    data = response_data.json()

    for station in data:

        # extract station name
        station_name = station['station_name'].replace(' ', '_')

        # extract parameter type
        parametertype_name = station['parametertype_name']

        # compose the json file name
        json_file_name = f'{directory_name}/{station_name}_{metric}_{years}_{parametertype_name}.json'
        # save to a file
        with open(json_file_name, 'w') as outfile:
            outfile.write(json.dumps(station))


get_timeseries_to_json_file(5, 'Max', '../../data/json/max')
get_timeseries_to_json_file(5, 'Min', '../../data/json/min')
