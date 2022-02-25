from django.apps import AppConfig
from django.conf import settings
import os




class ProfileConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    path = os.path.join(settings.BASE_DIR, 'Apps', 'Profile')
    verbose_name = 'App For Profile Info'
    name = 'Apps.Profile'
    label = 'Profile'
