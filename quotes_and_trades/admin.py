from django.contrib import admin

from .models import Ticker, Quote, Trade

admin.site.register(Ticker)
admin.site.register(Quote)
admin.site.register(Trade)
