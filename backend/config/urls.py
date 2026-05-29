from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/health/', include('apps.health.urls')),
    path('api/exchanges/', include('apps.exchanges.urls')),
    path('api/market/', include('apps.market_data.urls')),
    path('api/opportunities/', include('apps.arbitrage.urls')),
    path('api/trades/', include('apps.trading.urls')),
    path('api/wallets/', include('apps.wallets.urls')),
    path('api/logs/', include('apps.system_logs.urls')),
]
