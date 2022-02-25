from django.apps import AppConfig
from django.conf import settings
import os


class InfoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    path = os.path.join(settings.BASE_DIR, 'Apps', 'Info')
    verbose_name = 'App Info Feedback And Home Page'
    name = 'Apps.Info'
    label = 'Info'
