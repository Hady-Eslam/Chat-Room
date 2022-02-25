from django.apps import AppConfig
from django.conf import settings
import os


class AuthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    path = os.path.join(settings.BASE_DIR, 'Apps', 'Auth')
    verbose_name = 'App For Authentication'
    name = 'Apps.Auth'
    label = 'Auth'
