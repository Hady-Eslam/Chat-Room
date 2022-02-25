from django.apps import AppConfig
from django.conf import settings
import os


class ChatConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    path = os.path.join(settings.BASE_DIR, 'Apps', 'Chat')
    verbose_name = 'App For Chating'
    label = 'Chat'
    name = 'Apps.Chat'
