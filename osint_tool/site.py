import requests
from osint_tool.condition import Condition
from osint_tool.http_client import HTTPClient


class Site:
    url: str
    found_conditions: list[Condition]
    not_found_conditions: list[Condition]

    def __init__(self, **kwargs):
        self.url = kwargs['url']
        self.found_conditions = kwargs['found_conditions']
        self.not_found_conditions = kwargs['not_found_conditions']

    def check_username(self, username, client: HTTPClient):
        url = self.url.format(username)
        response = client.get(url)
        if any([i.check(response) for i in self.found_conditions]):
            return 'found'
        elif any([i.check(response) for i in self.not_found_conditions]):
            return 'not_found'
        else:
            return 'unknown'
