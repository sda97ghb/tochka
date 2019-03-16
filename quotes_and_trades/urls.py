from django.urls import path

from . import views

app_name = 'quotes_and_trades'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:ticker_id>/', views.quotes, name='quotes'),
    path('<int:ticker_id>/insider', views.insiders, name='insiders'),
    path('<int:ticker_id>/insider/<str:insider>', views.insider, name='insider'),
]

# /%TICKER%/analytics?date_from=..&date_to=... будет отдавать веб-страницу с данными о разнице цен в текущих датах(нужна разница всех цен - открытия, закрытия, максимума, минимума)
# /%TICKER/delta?value=N&type=(open/high/low/close) будет отдавать веб-страницу с данными о минимальных периодах (дата начала-дата конца), когда указанная цена изменилась более чем на N
