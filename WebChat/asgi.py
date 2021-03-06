"""
ASGI config for WebChat project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""

from django.core.asgi import get_asgi_application
import os, django


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WebChat.settings')

django.setup()

http_asgi_application = get_asgi_application()


from . import routing
from channels.security.websocket import AllowedHostsOriginValidator
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack



application = ProtocolTypeRouter({

    'http': http_asgi_application,
    
    'websocket': AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                routing.websocket_urlpatterns
            )
        )
    )
})
