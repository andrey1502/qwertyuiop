import requests


class Condition:
    type: str
    condition: None

    def __init__(self, condition_type: str, condition):
        self.type = condition_type
        self.condition = condition

    def check(self, response: requests.Response):
        if self.type == 'code':
            return response.status_code in self.condition
        elif self.type == 'text':
            return any([i in response.text for i in self.condition])
        elif self.type == 'url':
            return response.url in self.condition
        else:
            raise Exception(f'Unknown condition type: {self.type}')
