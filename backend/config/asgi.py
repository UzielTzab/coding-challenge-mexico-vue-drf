"""
ASGI config for config project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django_asgi_app = get_asgi_application()

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from config.routing import websocket_urlpatterns

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)
    ),
})

import asyncio
from apps.market_data.streams.stream_manager import StreamManager

class StartupMiddleware:
    def __init__(self, inner):
        self.inner = inner
        self.started = False

    async def __call__(self, scope, receive, send):
        if not self.started:
            self.started = True
            print("[MARKET ENGINE] Iniciando Motor de Mercado en el proceso ASGI (InMemoryLayer)...")
            asyncio.create_task(StreamManager().start())
        return await self.inner(scope, receive, send)

application = StartupMiddleware(application)
