from alpha_vantage.timeseries import TimeSeries
import logging
logging = logging.getLogger(__name__)


class Quote(object):

    def __init__(self, api_key, format='json'):
        logging.debug('Initialize {}'.format(self.__class__.__name__))
        self.ts = TimeSeries(key=api_key, output_format=format)

    def get(self, symbol):
        logging.info('Getting quotes data for {}'.format(symbol))
        return self.ts.get_intraday(symbol=symbol,
                                    interval='1min',
                                    outputsize='compact')
