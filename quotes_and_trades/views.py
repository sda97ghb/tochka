from datetime import date, timedelta, datetime

from django.http import HttpResponse, HttpRequest
from django.shortcuts import render

from .models import Ticker


def index(request):
    """
    /
    будет отдавать веб-страницу со ссылками на акции, доступные в базе данных.
    """
    return render(request, 'quotes_and_trades/index.html', context={
        'tickers': Ticker.objects.all()
    })


def quotes(request, ticker_id):
    """
    /%TICKER%
    будет отдавать веб-страницу с таблицей цен на акцию за 3 месяца
    """
    ticker = Ticker.objects.get(id=ticker_id)
    today = date.today()
    three_month_before = today + timedelta(days=-3*365/12)
    last_three_month_quotes = ticker.quote_set.filter(date__range=[three_month_before, today])
    return render(request, 'quotes_and_trades/quotes.html', context={
        'ticker': ticker,
        'quotes': last_three_month_quotes
    })


def insiders(request, ticker_id):
    """
    /%TICKER%/insider
    будет отдавать веб-страницу с данными торговли владельцев компании.
    На эту страницу попадать по ссыле со страницы /%TICKER%/
    """
    ticker = Ticker.objects.get(id=ticker_id)
    trades = ticker.trade_set.all()
    return render(request, 'quotes_and_trades/insiders.html', context={
        'ticker': ticker,
        'trades': trades
    })


def insider(request, ticker_id, insider):
    """
    /%TICKER%/insider/%NAME%
    будет отдавать веб-страницу с данными о торговле данного владельца компании.
    На эту страницу попадать по ссылке со страницы /%TICKER%/insider
    """
    ticker = Ticker.objects.get(id=ticker_id)
    trades = ticker.trade_set.filter(insider=insider)
    return render(request, 'quotes_and_trades/insider.html', context={
        'ticker': ticker,
        'insider': insider,
        'trades': trades
    })


def analytics(request: HttpRequest, ticker_id):
    """
    /%TICKER%/analytics?date_from=..&date_to=...
    будет отдавать веб-страницу с данными о разнице цен в текущих датах
    (нужна разница всех цен - открытия, закрытия, максимума, минимума)
    """
    date_from = get_date_or_today(request, 'date_from')
    date_to = get_date_or_today(request, 'date_to')
    ticker = Ticker.objects.get(id=ticker_id)
    quotes = ticker.quote_set.filter(date__range=[date_from, date_to])
    if quotes.count() > 0:
        first_quote = quotes[0]
        last_quote = first_quote
        open = first_quote.open
        close = open
        low = open
        high = open
        for quote in quotes:
            last_quote = quote
            close = quote.close
            low = min(low, quote.low)
            high = max(high, quote.high)
        return render(request, 'quotes_and_trades/analytics.html', context={
            'ticker': ticker,
            'date_from': date_from,
            'date_to': date_to,
            'today': date.today(),
            'date_from_iso': date_to_string(date_from),
            'date_to_iso': date_to_string(date_to),
            'today_iso': date_to_string(date.today()),
            'no_data_flag': False,
            'first_quote': first_quote,
            'last_quote': last_quote,
            'statistics': {
                'open': open,
                'close': close,
                'low': low,
                'high': high,
                'change': close - open
            }
        })
    else:
        return render(request, 'quotes_and_trades/analytics.html', context={
            'ticker': ticker,
            'date_from': date_from,
            'date_to': date_to,
            'today': date.today(),
            'date_from_iso': date_to_string(date_from),
            'date_to_iso': date_to_string(date_to),
            'today_iso': date_to_string(date.today()),
            'no_data_flag': True,
        })


def date_to_string(date):
    return "%d-%02d-%02d" % (date.year, date.month, date.day)


def get_date_or_today(request, argument_name):
    today = date_to_string(date.today())
    try:
        return datetime.strptime(request.GET.get(argument_name, today), '%Y-%m-%d')
    except ValueError:
        return datetime.strptime(today, '%Y-%m-%d')


def delta(request, ticker_id):
    """
    /%TICKER/delta?value=N&type=(open/high/low/close)
    будет отдавать веб-страницу с данными о минимальных периодах (дата начала-дата конца),
    когда указанная цена изменилась более чем на N
    """
    return None
