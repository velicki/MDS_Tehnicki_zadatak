from django.urls import path
from .views import *

urlpatterns = [
    path('company', company, name='company'),
    path('company/', company, name='company'),
    path('one_company/<str:ticker_symbol>', one_company, name='one_company'),
    path('stock/<str:ticker_symbol>', stock, name='stock'),
    path('one_stock/<str:ticker_symbol>/<str:date>', one_stock, name='one_stock'),
    path('triple_period_comparison/<str:ticker_symbol>/start-date/<str:mm1>/<str:dd1>/<int:yyyy1>/end-date/<str:mm2>/<str:dd2>/<int:yyyy2>', triple_period_comparison, name='triple_period_comparison'),
]