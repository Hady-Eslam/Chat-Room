from django.urls import path

from . import views


app_name = 'Profile.api'

urlpatterns = [
    
    path('password/', views.PasswordAPI.as_view(), name='Password'),

    path('avatar/', views.ProfileAvatartAPI.as_view(), name='Avatar'),

    path('', views.ProfileAPI.as_view(), name='Profile'),
]
