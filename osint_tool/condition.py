import requests


class BaseCondition:
    def check(self, response: requests.Response) -> bool:
        pass


class Condition(BaseCondition):
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


class AND(BaseCondition):
    conditions: list[BaseCondition]

    def __init__(self, *conditions):
        self.conditions = list(conditions)

    def check(self, response: requests.Response):
        return all([i.check(response) for i in self.conditions])


class OR(BaseCondition):
    conditions: list[BaseCondition]

    def __init__(self, *conditions):
        self.conditions = list(conditions)

    def check(self, response: requests.Response):
        return any([i.check(response) for i in self.conditions])


class NOT(BaseCondition):
    condition: BaseCondition

    def __init__(self, condition1: BaseCondition):
        self.condition = condition1

    def check(self, response: requests.Response):
        return not self.condition.check(response)
