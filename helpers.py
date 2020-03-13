import requests
import logging
import warnings
import os
from urllib.parse import urljoin
from requests_toolbelt.utils import dump
from urllib3.exceptions import InsecureRequestWarning

BASE_URL = "https://api.github.com"

API_TOKEN = os.getenv('TOKEN')


def validate_response(resp, payload):
    pay_files = payload['files'].keys()
    resp_files = resp['files'].keys()
    # Validation of file names
    assert pay_files == resp_files
    assert payload['description'] == resp['description']
    assert payload['public'] == resp['public']


class Api:
    def __init__(self):
        self.timeout = 10
        self.log = logging.getLogger(__name__)
        self.api_url = BASE_URL

    def make_request(self, endpoint, method='get', headers=None, params=None, body=None, timeout=None):
        request_url = urljoin(self.api_url, endpoint)
        if timeout is None:
            timeout = self.timeout

        warnings.filterwarnings('ignore', category=InsecureRequestWarning)
        response = requests.request(
            method=method,
            url=request_url,
            params=params,
            headers=headers,
            json=body,
            verify=False,
            timeout=timeout
        )
        warnings.resetwarnings()
        data = dump.dump_all(response)
        self.log.info(data)
        return response

    def create(self, **kwargs):
        headers = {'Authorization': f'token {API_TOKEN}'}
        params = {'scope': 'gist'}
        path = "/gists"
        return self.make_request(endpoint=path, method='POST', headers=headers, params=params, **kwargs)

    def read(self, gist_id, **kwargs):
        path = "/gists/" + gist_id
        return self.make_request(endpoint=path, method='GET', **kwargs)

    def update(self, gist_id, **kwargs):
        headers = {'Authorization': f'token {API_TOKEN}'}
        params = {'scope': 'gist'}
        path = "/gists/" + gist_id
        return self.make_request(endpoint=path, method='PATCH', headers=headers, params=params, **kwargs)

    def delete(self, gist_id, **kwargs):
        headers = {'Authorization': f'token {API_TOKEN}'}
        params = {'scope': 'gist'}
        path = "/gists/" + gist_id
        return self.make_request(endpoint=path, method='DELETE', headers=headers, params=params, **kwargs)

    def read_all(self, **kwargs):
        headers = {'Authorization': f'token {API_TOKEN}'}
        params = {'scope': 'gist'}
        path = "/gists"
        return self.make_request(endpoint=path, method='GET', headers=headers, params=params, **kwargs)
