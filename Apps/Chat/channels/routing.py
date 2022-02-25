from django.urls import path
from . import consumers




websocket_urlpatterns = [
    path('chat/<slug:room_code>/', consumers.ChatConsumer.as_asgi()),
]
