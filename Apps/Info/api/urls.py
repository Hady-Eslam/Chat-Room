from django.urls import path
from . import views


app_name = 'Info.api'

urlpatterns = [

    path('feedback/', views.FeedbackAPI.as_view(), name='Feedback'),
]
