from django.urls import re_path
from apps.core.consumers import DashboardConsumer

websocket_urlpatterns = [
    re_path(r'ws/dashboard/$', DashboardConsumer.as_asgi()),
    re_path(r'ws/market/$', DashboardConsumer.as_asgi()),
    re_path(r'ws/logs/$', DashboardConsumer.as_asgi()),
]
