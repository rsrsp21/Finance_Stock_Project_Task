from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.homepage, name='homepage'),  # Existing homepage URL
    path('fetch/', views.fetch_and_store, name='fetch_and_store'),  # Existing fetch URL
    path('stock_data/', views.stock_data_list, name='stock_data_list'),  # New URL for stock data
    path('backtest/', views.backtest, name='backtest'), #New Backtest page
    path('predict/', views.predict_prices, name='predict_prices'),
    path('report/', views.performance_report, name='performance_report'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)