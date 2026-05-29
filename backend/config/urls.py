from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/docs/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('api/health/', include('apps.health.urls')),
    path('api/exchanges/', include('apps.exchanges.urls')),
    path('api/market/', include('apps.market_data.urls')),
    path('api/opportunities/', include('apps.arbitrage.urls')),
    path('api/trades/', include('apps.trading.urls')),
    path('api/wallets/', include('apps.wallets.urls')),
    path('api/logs/', include('apps.system_logs.urls')),
]
