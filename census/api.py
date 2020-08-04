import json
import os

import pandas as pd
import requests
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
_BASE_URL = 'https://api.census.gov/data/2018/acs/acs5'


def construct_params(variables, geography, state='*', county='*'):
    if isinstance(variables, str):
        variables = [variables]

    include_in = True
    if geography == 'state':
        state = None
        county = None
        include_in = False
    elif geography == 'county':
        county = None

    params = {
        'get': ','.join(variables),
        'for': f'{geography}:*',
        'key': os.getenv('CENSUS_API_KEY'),
    }

    if include_in:
        levels = {'state': state, 'county': county}
        params['in'] = [f'{k}:{v}' for k, v in levels.items() if v is not None]

    return params


def query(variables, geography='tract', state='*', county='*'):
    params = construct_params(variables, geography, state, county)
    r = requests.get(_BASE_URL, params)
    r.raise_for_status()
    return r


def query_to_df(response):
    response_json = json.loads(response.text)
    df = pd.DataFrame(data=response_json[1:], columns=response_json[0])
    return df


def get_state_fips():
    r = query(['GEO_ID', 'NAME'], 'state')
    return query_to_df(r).sort_values('NAME')


def get_county_fips(state):
    r = query(['GEO_ID', 'NAME'], 'county', state=state)
    return query_to_df(r).sort_values('NAME')


def get_variable_list():
    df = pd.read_html(_BASE_URL + '/variables.html')[0]
    df = df.drop('Unnamed: 8', axis=1)
    return df
