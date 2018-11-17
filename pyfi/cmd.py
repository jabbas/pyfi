from argparse import ArgumentParser
import sys
import logging

from .parser import InfluxStocks
from .alpha import Quote

logging.basicConfig(stream=sys.stderr,
                    format='%(asctime)s:%(levelname)s:%(name)s: - %(message)s')


def cmd():

    parser = ArgumentParser(description='Grab stocks prices into influxdb')

    parser.add_argument('--uri', '-u', type=str,
                        help='influxdb uri')
    parser.add_argument('--key', '-k', type=str, metavar='APIKEY',
                        help='https://www.alphavantage.co API key')

    parser.add_argument('--loglevel', '-l', type=str, metavar='LEVEL',
                        default='CRITICAL',
                        help='log level (default: CRITICAL)')

    parser.add_argument('symbol', metavar='SYMBOL', type=str, nargs='+',
                        help='Stocks symbol')

    args = parser.parse_args()

    try:
        log = logging.getLogger()
        log.setLevel(args.loglevel.upper())

        for symbol in args.symbol:
            stocks = InfluxStocks(symbol,
                                  uri=args.uri,
                                  quote=Quote(args.key))
            stocks.write()
    except Exception as e:
        if args.loglevel == 'DEBUG':
            raise e

        logging.critical(e)
