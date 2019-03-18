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
    path('api/', views.api_index, name='api_index'),
    path('api/<int:ticker_id>/', views.api_quotes, name='api_quotes'),
    path('api/<int:ticker_id>/insider/', views.api_insiders, name='api_insiders'),
    path('api/<int:ticker_id>/insider/<str:insider>/', views.api_insider, name='api_insider'),
    path('api/<int:ticker_id>/analytics', views.api_analytics, name='api_analytics'),
    path('api/<int:ticker_id>/delta', views.api_delta, name='api_delta'),
]
