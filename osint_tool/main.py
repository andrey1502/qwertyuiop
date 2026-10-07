from osint_tool.condition import Condition
from osint_tool.http_client import HTTPClient
from osint_tool.site import Site

if __name__ == '__main__':
    github=Site(
        url='https://github.com/{}/',
        found_conditions=[Condition('code',[200])],
        not_found_conditions=[Condition('code',[404])],
    )
    client=HTTPClient()
    print(github.check_username('andrey1502',client))
    print(github.check_username('ewsedfhgjhkj',client))