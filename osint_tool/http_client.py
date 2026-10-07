import requests

class HTTPClient:
    def get(self,url):
        return requests.get(url)