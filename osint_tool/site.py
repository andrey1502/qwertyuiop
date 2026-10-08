import requests

from osint_tool.check import BaseCheck
from osint_tool.condition import Condition, BaseCondition
from osint_tool.http_client import HTTPClient


class Site:
    name: str
    checks: list[BaseCheck]

    def __init__(self, name: str, checks: list[BaseCheck]):
        self.name = name
        self.checks = checks

    def check_username(self, username):
        checks_result = [i.check_username(username) for i in self.checks]
        if 'found' in checks_result:
            return 'found'
        elif 'not_found' in checks_result:
            return 'not_found'
        else:
            return 'unknown'
