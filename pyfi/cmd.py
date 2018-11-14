from argparse import ArgumentParser

from .parser import InfluxStocks
from .alpha import Quote


def cmd():
    parser = ArgumentParser(description='Grab stocks prices into influxdb')

    parser.add_argument('--uri', '-u', type=str,
                        help='influxdb uri')
    parser.add_argument('--key', '-k', type=str, metavar='APIKEY',
                        help='https://www.alphavantage.co API key')

    parser.add_argument('symbol', type=str, nargs='+',
                        help='Stocks symbol')

    args = parser.parse_args()

    for symbol in args.symbol:
        stocks = InfluxStocks(symbol,
                              uri=args.uri,
                              quote=Quote(args.key))
        stocks.write()
