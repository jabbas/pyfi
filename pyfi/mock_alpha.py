import json


class Quote(object):

    def __init__(self, api_key='NONE', format='json', mock='mock.json'):
        with open(mock, 'r') as f:
            self.mock = json.load(f)

    def get(self, symbol='SABR'):
        return self.mock
