from django.urls import path
from . import views



app_name = 'Profile'

urlpatterns = [

    path('password/', views.PasswordView.as_view(template_name='Profile/Password.html'), name='Password'),

    path('settings/', views.SettingsView.as_view(template_name='Profile/Settings.html'), name='Settings'),

    path('', views.ProfileView.as_view(template_name='Profile/Profile.html'), name='Profile'),
]
