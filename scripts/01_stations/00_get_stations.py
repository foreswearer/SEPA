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


def get_stations_url(output_format: str):
    url = (
        f'https://timeseries.sepa.org.uk/KiWIS/KiWIS?'
        f'service=kisters&'
        f'type=queryServices&'
        f'data-source=0&'
        f'request=getStationList'
        f'&station-name=*&'
        f'format={output_format}'
    )
    return url


def get_stations_to_file(filename: str):

    # Specify request URL
    request_url = get_stations_url('csv')
    head_dict = get_header_token()

    # GET data request as response object
    response_data = requests.get(request_url, headers=head_dict)

    # retrieve JSON data from response object
    data = response_data.content
    csv_file = open(filename, 'wb')
    csv_file.write(data.replace(b';', b','))
    csv_file.close()


get_stations_to_file('../../data/stations/stations.csv', low_memory=False)
