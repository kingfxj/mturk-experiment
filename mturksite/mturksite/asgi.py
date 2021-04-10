"""
ASGI config for mturksite project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter,URLRouter
from channels.security.websocket import AllowedHostsOriginValidator 
from django.urls import path
from mturkapp.consumers import GameRoom

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mturksite.settings')

application = get_asgi_application()

ws_pattern = [
        path('ws/gamer/<hit_id>' , GameRoom.as_asgi())
]

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
            URLRouter(
                ws_pattern
            )
        )
    }) 