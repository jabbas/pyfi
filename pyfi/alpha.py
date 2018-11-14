from alpha_vantage.timeseries import TimeSeries


class Quote(object):

    def __init__(self, api_key, format='json'):
        self.ts = TimeSeries(key=api_key, output_format=format)

    def get(self, symbol):
        return self.ts.get_intraday(symbol=symbol,
                                    interval='1min',
                                    outputsize='compact')
