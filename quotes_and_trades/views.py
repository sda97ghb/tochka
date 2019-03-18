from datetime import date, timedelta, datetime

from django.http import HttpRequest, JsonResponse
from django.shortcuts import render

from .models import Ticker
from .models_serialization import serialize_ticker, serialize_quote, serialize_trade


def index(request):
    """
    /
    будет отдавать веб-страницу со ссылками на акции, доступные в базе данных.
    """
    return render(request, 'quotes_and_trades/index.html', context={
        'tickers': Ticker.objects.all()
    })


def api_index(request):
    return JsonResponse({
        'tickers': [serialize_ticker(ticker) for ticker in Ticker.objects.all()]
    })


def quotes(request, ticker_id):
    """
    /%TICKER%
    будет отдавать веб-страницу с таблицей цен на акцию за 3 месяца
    """
    ticker = Ticker.objects.get(id=ticker_id)
    last_three_month_quotes = get_last_three_month_quotes(ticker_id)
    return render(request, 'quotes_and_trades/quotes.html', context={
        'ticker': ticker,
        'quotes': last_three_month_quotes
    })


def api_quotes(request, ticker_id):
    ticker = Ticker.objects.get(id=ticker_id)
    last_three_month_quotes = get_last_three_month_quotes(ticker_id)
    return JsonResponse({
        'ticker': serialize_ticker(ticker),
        'quotes': [serialize_quote(quote) for quote in last_three_month_quotes]
    })


def get_last_three_month_quotes(ticker_id):
    ticker = Ticker.objects.get(id=ticker_id)
    today = date.today()
    three_month_before = today + timedelta(days=-3 * 365 / 12)
    return ticker.quote_set.filter(date__range=[three_month_before, today]).order_by('-date')


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


def api_insiders(request, ticker_id):
    ticker = Ticker.objects.get(id=ticker_id)
    trades = ticker.trade_set.all()
    return JsonResponse({
        'ticker': serialize_ticker(ticker),
        'trades': [serialize_trade(trade) for trade in trades]
    })


def insider(request, ticker_id, insider):
    """
    /%TICKER%/insider/%NAME%
    будет отдавать веб-страницу с данными о торговле данного владельца компании.
    На эту страницу попадать по ссылке со страницы /%TICKER%/insider
    """
    ticker = Ticker.objects.get(id=ticker_id)
    trades = get_insider_trades(ticker, insider)
    return render(request, 'quotes_and_trades/insider.html', context={
        'ticker': ticker,
        'insider': insider,
        'trades': trades
    })


def api_insider(request, ticker_id, insider):
    ticker = Ticker.objects.get(id=ticker_id)
    trades = get_insider_trades(ticker, insider)
    return JsonResponse({
        'ticker': serialize_ticker(ticker),
        'insider': insider,
        'trades': [serialize_trade(trade) for trade in trades]
    })


def get_insider_trades(ticker, insider):
    return ticker.trade_set.filter(insider=insider)


def analytics(request: HttpRequest, ticker_id):
    """
    /%TICKER%/analytics?date_from=..&date_to=...
    будет отдавать веб-страницу с данными о разнице цен в текущих датах
    (нужна разница всех цен - открытия, закрытия, максимума, минимума)
    """
    date_from = get_date_or_today(request, 'date_from')
    date_to = get_date_or_today(request, 'date_to')
    ticker = Ticker.objects.get(id=ticker_id)
    data = get_analytics_data(ticker, date_from, date_to)
    return render(request, 'quotes_and_trades/analytics.html', context={
        'ticker': ticker,
        'iso_date_from': date_to_iso_string(date_from),
        'iso_date_to': date_to_iso_string(date_to),
        'data': data
    })


def api_analytics(request: HttpRequest, ticker_id):
    date_from = get_date_or_today(request, 'date_from')
    date_to = get_date_or_today(request, 'date_to')
    ticker = Ticker.objects.get(id=ticker_id)
    data = get_analytics_data(ticker, date_from, date_to)
    return JsonResponse({
        'ticker': serialize_ticker(ticker),
        'date_from': date_from,
        'date_to': date_to,
        'first_quote': serialize_quote(data['first_quote']),
        'last_quote': serialize_quote(data['last_quote']),
        'statistics': data['statistics']
    })


def get_analytics_data(ticker, date_from, date_to):
    quotes = ticker.quote_set.filter(date__range=[date_from, date_to]).order_by('date')
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
        return {
                'first_quote': first_quote,
                'last_quote': last_quote,
                'statistics': {
                    'open': open,
                    'close': close,
                    'low': low,
                    'high': high,
                    'change': round(close - open, 4),
                    'change_percent': round((close - open) / open * 100, 2)
                }
            }
    else:
        return None


def get_date_or_today(request, argument_name):
    today = date_to_iso_string(date.today())
    try:
        return datetime.strptime(request.GET.get(argument_name, today), '%Y-%m-%d')
    except ValueError:
        return datetime.strptime(today, '%Y-%m-%d')


def date_to_iso_string(date):
    return "%d-%02d-%02d" % (date.year, date.month, date.day)


def delta(request, ticker_id):
    """
    /%TICKER/delta?value=N&type=(open/high/low/close)
    будет отдавать веб-страницу с данными о минимальных периодах (дата начала-дата конца),
    когда указанная цена изменилась более чем на N
    """
    change = float(request.GET.get('value', '1'))
    type = request.GET.get('type', 'open')
    ticker = Ticker.objects.get(id=ticker_id)
    periods = calculate_periods(ticker, change, type)
    return render(request, 'quotes_and_trades/delta.html', context={
        'request': {
            'change': change,
            'type': type
        },
        'ticker': ticker,
        'periods': periods
    })


def api_delta(request, ticker_id):
    change = float(request.GET.get('value', '1'))
    type = request.GET.get('type', 'open')
    ticker = Ticker.objects.get(id=ticker_id)
    periods = calculate_periods(ticker, change, type)
    return JsonResponse({
        'result': periods
    })


def get_quote_price(quote, type):
    if type == 'open':
        return quote.open
    elif type == 'close':
        return quote.close
    elif type == 'low':
        return quote.low
    elif type == 'high':
        return quote.high
    else:
        return 0


def calculate_periods(ticker, change, type):
    quotes = ticker.quote_set.all().order_by('date')
    if quotes.count() > 0:
        periods = []
        period_start_price = get_quote_price(quotes[0], type)
        period_start_date = quotes[0].date
        for quote in quotes:
            current_quote_price = get_quote_price(quote, type)
            current_quote_date = quote.date
            if abs(current_quote_price - period_start_price) >= change:
                periods.append({
                    'start_date': period_start_date,
                    'finish_date': current_quote_date,
                    'start_price': period_start_price,
                    'finish_price': current_quote_price
                })
                period_start_price = current_quote_price
                period_start_date = current_quote_date
        return periods
    else:
        return []
