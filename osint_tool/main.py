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


class Site:
    url: str
    found_conditions: list[Condition]
    not_found_conditions: list[Condition]

    def __init__(self, **kwargs):
        self.url = kwargs['url']
        self.found_conditions = kwargs['found_conditions']
        self.not_found_conditions = kwargs['not_found_conditions']

    def check_username(self, username):
        url = self.url.format(username)
        response = requests.get(url)
        if any([i.check(response) for i in self.found_conditions]):
            return 'found'
        elif any([i.check(response) for i in self.not_found_conditions]):
            return 'not_found'
        else:
            return 'unknown'


if __name__ == '__main__':
    github=Site(
        url='https://github.com/{}/',
        found_conditions=[Condition('code',[200])],
        not_found_conditions=[Condition('code',[404])],
    )
    print(github.check_username('andrey1502'))
    print(github.check_username('ewsedfhgjhkj'))