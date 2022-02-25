from django.urls import path
from . import views


app_name = 'Info'

urlpatterns = [

    path('feedback/', views.FeedbackView.as_view(template_name='Info/Feedback.html'), name='Feedback'),

    path('who-i-am/', views.WhoIAmView.as_view(template_name='Info/WhoIAm.html'), name='WhoIAm'),

    path('download-cv/', views.DownloadCV.as_view(), name='Download-CV'),
]
