from django.urls import path
from channels.routing import URLRouter
from Apps.Chat.channels import routing



websocket_urlpatterns = [
    path('ws/', URLRouter(
        routing.websocket_urlpatterns
    )),
]
