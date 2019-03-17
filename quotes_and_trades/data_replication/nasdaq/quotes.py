import csv
import io

import requests

TIMEFRAME_5_DAYS = '5d'
TIMEFRAME_1_MONTH = '1m'
TIMEFRAME_3_MONTH = '3m'
TIMEFRAME_6_MONTH = '6m'
TIMEFRAME_1_YEAR = '1y'
TIMEFRAME_18_MONTH = '18m'
TIMEFRAME_2_YEAR = '2y'
TIMEFRAME_3_YEAR = '3y'
TIMEFRAME_4_YEAR = '4y'
TIMEFRAME_5_YEAR = '5y'
TIMEFRAME_6_YEAR = '6y'
TIMEFRAME_7_YEAR = '7y'
TIMEFRAME_8_YEAR = '8y'
TIMEFRAME_9_YEAR = '9y'
TIMEFRAME_10_YEAR = '10y'


def get(ticker, timeframe=TIMEFRAME_3_MONTH):
    try:
        return parse_quotes(download_quotes(ticker, timeframe))
    except Exception:
        # If we've got any exception return empty quotes
        return parse_quotes('"date","close","volume","open","high","low"')


def download_quotes(ticker, timeframe=TIMEFRAME_3_MONTH):
    """
    Downloads quotes for ticker.
    :param ticker: Ticker
    :param timeframe: Any of TIMEFRAME_* values
    :return: Downloaded quotes as csv text.
    """
    s = requests.Session()
    response = s.post(
        "https://www.nasdaq.com/symbol/%s/historical" % ticker.lower(),
        data="%s|true|%s" % (timeframe, ticker.upper()),
        headers={'Content-Type': 'application/json'},
        stream=True
    )
    return response.text


def parse_quotes(text):
    dialect = csv.Sniffer().sniff(text)
    return csv.DictReader(
        io.StringIO(text),
        dialect=dialect,
    )
