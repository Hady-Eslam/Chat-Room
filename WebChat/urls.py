"""WebChat URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import os
from django.apps import apps
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from Apps.Info import views


urlpatterns = [
    path('admin/', admin.site.urls),

    path('auth/', include('Apps.Auth.urls')),

    path('profile/', include('Apps.Profile.urls')),

    path('info/', include('Apps.Info.urls')),

    path('chats/', include('Apps.Chat.urls')),

    path('api/', include([

        path('auth/', include('Apps.Auth.api.urls')),

        path('profile/', include('Apps.Profile.api.urls')),

        path('info/', include('Apps.Info.api.urls')),

        path('chats/', include('Apps.Chat.api.urls')),

    ])),

    path('', views.HomeView.as_view(template_name='Info/Home.html'), name=''),
]

urlpatterns += static(
    settings.MEDIA_URL + 'user/',
    document_root=os.path.join(apps.get_app_config('Profile').path, 'media', 'user'),
)

urlpatterns += static(
    settings.MEDIA_URL + 'rooms/',
    document_root=os.path.join(apps.get_app_config('Chat').path, 'media', 'rooms'),
)
