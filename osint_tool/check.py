from osint_tool.condition import BaseCondition
from osint_tool.http_client import HTTPClient


class BaseCheck:
    def check_username(self, username):
        pass


class WebCheck(BaseCheck):
    url: str
    client: HTTPClient
    found_conditions: list[BaseCondition]
    not_found_conditions: list[BaseCondition]

    def __init__(self, url: str, found_conditions: list[BaseCondition], not_found_conditions: list[BaseCondition],
                 client: HTTPClient):
        self.url = url
        self.found_conditions = found_conditions
        self.not_found_conditions = not_found_conditions
        self.client = client

    def check_username(self, username):
        url = self.url.format(username)
        response = self.client.get(url)
        if any([i.check(response) for i in self.found_conditions]):
            return 'found'
        elif any([i.check(response) for i in self.not_found_conditions]):
            return 'not_found'
        else:
            return 'unknown'

class APICheck(BaseCheck):
    url: str
    client: HTTPClient
    url: str
    client: HTTPClient
    found_conditions: list[BaseCondition]
    not_found_conditions: list[BaseCondition]

    def __init__(self, url: str, found_conditions: list[BaseCondition], not_found_conditions: list[BaseCondition],
                 client: HTTPClient):
        self.url = url
        self.found_conditions = found_conditions
        self.not_found_conditions = not_found_conditions
        self.client = client

    def check_username(self, username):
        pass