from django.http import HttpResponse
from django.shortcuts import render

from .models import Ticker


def index(request):
    """
    / будет отдавать веб-страницу со ссылками на акции, доступные в базе данных.
    """
    return render(request, 'quotes_and_trades/index.html', context={
        'tickers': Ticker.objects.all()
    })


def quotes(request, ticker_id):
    """
    /%TICKER% будет отдавать веб-страницу с таблицей цен на акцию за 3 месяца
    """
    ticker = Ticker.objects.get(id=ticker_id)
    return HttpResponse("WIP: %s" % ticker.name)


def insiders(request, ticker_id):
    """
    /%TICKER%/insider будет отдавать веб-страницу с данными торговли владельцев компании. На эту страницу попадать по ссыле со страницы /%TICKER%/
    """
    ticker = Ticker.objects.get(id=ticker_id)
    return HttpResponse("WIP: %s" % ticker.name)


def insider(request, ticker_id, insider):
    """
    /%TICKER%/insider/%NAME% будет отдавать веб-страницу с данными о торговле данного владельца компании. На эту страницу попадать по ссылке со страницы /%TICKER%/insider
    """
    ticker = Ticker.objects.get(id=ticker_id)
    return HttpResponse("WIP: %s" % ticker.name)
