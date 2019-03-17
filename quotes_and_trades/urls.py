from django.urls import path

from . import views

app_name = 'quotes_and_trades'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:ticker_id>/', views.quotes, name='quotes'),
    path('<int:ticker_id>/insider/', views.insiders, name='insiders'),
    path('<int:ticker_id>/insider/<str:insider>/', views.insider, name='insider'),
    path('<int:ticker_id>/analytics', views.analytics, name='analytics'),
    path('<int:ticker_id>/delta', views.delta, name='delta'),
]
