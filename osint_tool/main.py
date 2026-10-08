from osint_tool.check import WebCheck
from osint_tool.condition import Condition, OR, AND, NOT
from osint_tool.http_client import HTTPClient
from osint_tool.site import Site

if __name__ == '__main__':
    client = HTTPClient()

    github = Site(
        name='GitHub',
        checks=[
            WebCheck(
                url='https://github.com/{}/',
                found_conditions=[Condition('code', [200])],
                not_found_conditions=[AND(Condition('code', [404]),
                                          OR(NOT(Condition('code', [403])),
                                             Condition('text', ['not_found'])))],  # to show abilities
                client=HTTPClient()
            )
        ]

    )
    # codeforces = Site(
    #     url='https://www.codeforces.com/profile/{}/',
    #     found_conditions=[Condition('code', [200])],
    #     not_found_conditions=[Condition('url', ['codeforces.com'])],
    # )
    print(github.check_username('andrey1502'))
    print(github.check_username('ewsedfhgjhkj', ))
    # print(codeforces.check_username('andrey1502'))
    # print(codeforces.check_username('ewsedfhgjhkj'))
