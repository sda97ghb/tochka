from multiprocessing.dummy import Pool as ThreadPool

from django.db import IntegrityError

from .nasdaq import quotes as nasdaq_quotes, trades as nasdaq_trades
from ..models import Ticker, Quote, Trade
import datetime


def replicate(number_of_threads=4):
    tickers = get_tickers()
    print(tickers)
    create_tickers_in_database(tickers)
    replicate_quotes(tickers, number_of_threads)
    replicate_trades(tickers, number_of_threads)


def get_tickers():
    with open('quotes_and_trades/data_replication/tickers.txt', 'r') as tickers_file:
        return [line.strip() for line in tickers_file.readlines()]


def create_tickers_in_database(tickers):
    for ticker in tickers:
        try:
            Ticker(name=ticker).save()
        except IntegrityError:
            # Ticker already exists
            pass


def replicate_quotes(tickers, number_of_threads):
    thread_pool = ThreadPool(number_of_threads)
    thread_pool.map(replicate_ticker_quotes, tickers)
    thread_pool.close()
    thread_pool.join()


def replicate_ticker_quotes(ticker):
    quotes = nasdaq_quotes.get(ticker)
    save_quotes_in_database(ticker, quotes)


def save_quotes_in_database(ticker, quotes):
    db_ticker = get_db_ticker(ticker)
    for quote in quotes:
        print(quote)
        try:
            db_quote = make_db_quote(quote, db_ticker)
            db_quote.save()
        except ValueError:
            # Incorrect data format, for example time in the data field
            pass
        except IntegrityError:
            # Quote already exists
            pass


def get_db_ticker(ticker):
    return Ticker.objects.filter(name=ticker)[0]


def make_db_quote(quote, db_ticker):
    # Quote example:
    #   OrderedDict([('date', '2018/12/27'), ('close', '156.1500'), ('volume', '51608850.0000'),
    #                ('open', '155.8400'), ('high', '156.7700'), ('low', '150.0700')])
    return Quote(
        ticker=db_ticker,
        date=datetime.datetime.strptime(quote['date'], '%Y/%m/%d'),
        open=float(quote['open']),
        close=float(quote['close']),
        low=float(quote['low']),
        high=float(quote['high']),
        volume=int(float(quote['open']))
    )


def replicate_trades(tickers, number_of_threads):
    thread_pool = ThreadPool(number_of_threads)
    thread_pool.map(replicate_ticker_trades, tickers)
    thread_pool.close()
    thread_pool.join()


def replicate_ticker_trades(ticker):
    trades = nasdaq_trades.get(ticker)
    if trades.is_empty:
        print('There is no trades for ticker %s' % ticker)
    else:
        delete_all_trades_from_db(ticker)
        save_trades_in_database(ticker, trades)


def delete_all_trades_from_db(ticker):
    get_db_ticker(ticker).trade_set.all().delete()


def save_trades_in_database(ticker, trades):
    db_ticker = get_db_ticker(ticker)
    for trade in trades:
        print(trade)
        try:
            db_trade = make_db_trade(trade, db_ticker)
            db_trade.save()
        except ValueError:
            # Incorrect data format, for example time in the data field
            pass


def make_db_trade(trade, db_ticker):
    # Trade example:
    #   {
    #       'Insider': 'BELL JAMES A',
    #       'Relation': 'Director',
    #       'Last Date': '02/01/2019',
    #       'Transaction Type': 'Option Execute',
    #       'OwnerType': 'direct',
    #       'Shares Traded': '1,521',
    #       'Last Price': None,
    #       'Shares Held': '7,464'
    #   }
    return Trade(
        ticker=db_ticker,
        insider=trade['Insider'],
        relation=trade['Relation'],
        last_date=datetime.datetime.strptime(trade['Last Date'], '%m/%d/%Y'),
        transaction_type=trade['Transaction Type'],
        owner_type=trade['OwnerType'],
        shares_traded=int(trade['Shares Traded'].replace(',', '')),
        last_price=parse_nullable_float(trade['Last Price']),
        shares_held=int(trade['Shares Held'].replace(',', ''))
    )


def parse_nullable_float(str):
    if str is None:
        return None
    else:
        return float(str)

# from quotes_and_trades.data_replication.data_replication import replicate
# replicate()
