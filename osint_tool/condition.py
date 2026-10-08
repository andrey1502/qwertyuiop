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
    condition1: BaseCondition
    condition2: BaseCondition

    def __init__(self, condition1: BaseCondition, condition2: BaseCondition):
        self.condition1 = condition1
        self.condition2 = condition2

    def check(self, response: requests.Response):
        return self.condition1.check(response) and self.condition2.check(response)


class OR(BaseCondition):
    condition1: BaseCondition
    condition2: BaseCondition

    def __init__(self, condition1: BaseCondition, condition2: BaseCondition):
        self.condition1 = condition1
        self.condition2 = condition2

    def check(self, response: requests.Response):
        return self.condition1.check(response) or self.condition2.check(response)


class NOT(BaseCondition):
    condition: BaseCondition

    def __init__(self, condition1: BaseCondition):
        self.condition = condition1

    def check(self, response: requests.Response):
        return not self.condition.check(response)
