from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from . import views


app_name = 'Auth.api'

urlpatterns = [
    
    path('signup/', views.SignupAPI.as_view(), name='Signup'),
    path('confirm-signup/', views.ConfirmSignupAPI.as_view(), name='Confirm-Signup'),


    path('token/', jwt_views.TokenObtainPairView.as_view(), name='Token'),
    path('refresh/', jwt_views.TokenRefreshView.as_view(), name='Refresh'),


    path('forget-password/', views.ForgetPasswordAPI.as_view(), name='Forget-Password'),
    path('reset-password/', views.ResetPasswordAPI.as_view(), name='Reset-Password'),
]
