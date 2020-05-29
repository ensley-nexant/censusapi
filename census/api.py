import json
import os
from urllib.parse import urlencode, quote

import pandas as pd
import urllib3
from dotenv import load_dotenv, find_dotenv


def query(http, variables, geography='tract', state=None):
    if geography == 'zip':
        geography = 'zip code tabulation area'
    elif geography != 'tract':
        raise ValueError('geography must be "tract" or "zip"')

    if state is None:
        state = '*'

    base_url = 'https://api.census.gov/data/2018/acs/acs5/'
    if isinstance(variables, str):
        variables = [variables]
    params = {
        'get': f'GEO_ID,NAME,{",".join(variables)}',
        'for': geography
    }

    if geography == 'tract':
        params['in'] = f'state:{state}'

    params['key'] = os.getenv('CENSUS_API_KEY')

    url = base_url + '?' + urlencode(params, safe='/:,*', quote_via=quote)
    # print(url)
    return http.request('GET', url)


def get_variable_list():
    base_url = 'https://api.census.gov/data/2018/acs/acs5/'
    df = pd.read_html(base_url + 'variables.html')[0]
    df = df.drop('Unnamed: 8', axis=1)
    return df


class ACSDataset:
    def __init__(self):
        load_dotenv(find_dotenv())
        self.KEY = os.getenv('CENSUS_API_KEY')
        self.http = urllib3.PoolManager()
        self.response = None

    def load(self, variables, geography, state=None):
        self.response = query(self.http, variables, geography, state)

    def to_pandas(self):
        formatted_response = json.loads(self.response.data.decode('utf-8'))
        df = pd.DataFrame(columns=formatted_response[0], data=formatted_response[1:])
        df = df.set_index('GEO_ID')
        return df

    def to_csv(self, fp, data=None):
        if data is None:
            data = self.to_pandas()
        data.to_csv(fp)
