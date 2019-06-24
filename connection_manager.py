import requests


class ConnectionManager:
    URL = ""

    def __init__(self, url):
        self.URL = url

    def make_request(self, path="", parameters=None):
        if parameters is None:
            return requests.get(self.URL + path).json()
        return requests.get(self.URL+path, params=parameters).json()

    def post_data(self, path="", data={}):
        return requests.post(self.URL+path, json=data).json()