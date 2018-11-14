from pytz import timezone
from datetime import datetime

from yurl import URL
from influxdb import InfluxDBClient

from .alpha import Quote


class WrongSchemeException(Exception):
    pass


class NoAPIKEYException(Exception):
    pass


def InfluxDB(uri):
    p = URL(uri)

    if p.scheme != 'influx':
        raise WrongSchemeException(uri)

    return InfluxDBClient(
            p.host,
            p.port or 8086,
            p.username,
            p.authorization,
            p.path.lstrip('/')
    )


class InfluxStocks(object):
    iso_format = '%Y-%m-%dT%H:%M:%SZ'
    utc = timezone('UTC')

    def __init__(self, symbol, uri, quote=None, api_key=None):
        if quote:
            self.quote = quote
        else:
            if api_key:
                self.quote = Quote(api_key)
            else:
                raise NoAPIKEYException

        self.symbol = symbol
        self.influx = InfluxDB(uri)
        self._last = None

        self.measurement = 'stocks_intraday'.format(symbol).lower()

    def fetch(self):
        (data, metadata) = self.quote.get(self.symbol)
        tz = timezone(list(metadata.values())[5])
        fetched_symbol = list(metadata.values())[1]

        for k in data.keys():
            dt = datetime.strptime(k, '%Y-%m-%d %H:%M:%S')
            dt = tz.localize(dt).astimezone(self.utc)

            (open, high, low, close, volume) = data[k].values()

            yield {
                'measurement': self.measurement,
                'tags': {
                    'symbol': fetched_symbol,
                },
                'time': dt,

                'fields': {
                    'open': float(open),
                    'high': float(high),
                    'low': float(low),
                    'close': float(close),
                    'volume': volume,
                }
            }

    def write(self):
        last = None
        influx_data = list()
        for d in self.fetch():
            if not last:
                last = self.last(d['tags']['symbol'])

            if d['time'] <= last:
                print('Skipping {}: {} <= {}'.format(
                                                     d['tags']['symbol'],
                                                     d['time'],
                                                     last))
            else:
                influx_data.append(d)

        self.influx.write_points(influx_data)

    def last(self, symbol, field='close'):
        if not self._last:
            query = "SELECT LAST({}) FROM {} WHERE symbol='{}'"
            res = self.influx.query(query.format('close',
                                                 self.measurement,
                                                 self.symbol))

            points = list(res.get_points())
            if points:
                point = points[0]
                self._last = datetime.strptime(point['time'], self.iso_format)
            else:
                self._last = datetime.fromtimestamp(0)
        return self._last.astimezone(self.utc)
