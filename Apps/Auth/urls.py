from django.urls import path
from Apps.Auth import views



app_name = 'Auth'

urlpatterns = [

    path('signup/', views.Signup.as_view(template_name='Auth/signup.html'), name='Signup'),
    path('confirm-signup/', views.ConfirmSignup.as_view(template_name='Auth/confirm-signup.html'), name='Confirm-Signup'),

    path('login/', views.Login.as_view(template_name='Auth/login.html'), name='Login'),
    path('login-as-guest/', views.LoginAsGuest.as_view(), name='Guest-Login'),
    path('logout/', views.Logout.as_view(), name='Logout'),

    path('forget-password/', views.ForgetPassword.as_view(template_name='Auth/forget-password.html'), name='Forget-Password'),
    path('reset-password/', views.ResetPassword.as_view(template_name='Auth/reset-password.html'), name='Reset-Password'),
]
