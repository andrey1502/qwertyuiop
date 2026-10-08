from osint_tool.condition import Condition, OR, AND, NOT
from osint_tool.http_client import HTTPClient
from osint_tool.site import Site

if __name__ == '__main__':
    github = Site(
        url='https://github.com/{}/',
        found_conditions=[Condition('code', [200])],
        not_found_conditions=[AND(Condition('code', [404]),
                                  OR(NOT(Condition('code', [403])),
                                     Condition('text', ['not_found'])))]  # to show abilities
    )
    codeforces = Site(
        url='https://www.codeforces.com/profile/{}/',
        found_conditions=[Condition('code', [200])],
        not_found_conditions=[Condition('url', ['codeforces.com'])],
    )
    client = HTTPClient()
    print(github.check_username('andrey1502', client))
    print(github.check_username('ewsedfhgjhkj', client))
    print(codeforces.check_username('andrey1502', client))
    print(codeforces.check_username('ewsedfhgjhkj', client))
