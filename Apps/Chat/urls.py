from django.urls import path, include
from . import views



app_name = 'Chat'

urlpatterns = [

    path('create/', views.CreateRoomView.as_view(template_name='Chat/Create.html'), name='Create'),

    path('room/', views.JoinRoomView.as_view(), name='Join-Room'),

    path('<slug:Room_Code>/', include([

        path('settings/', views.SettingsView.as_view(template_name='Chat/Settings.html'), name='Settings'),

        path('members/', include([

            path('<int:Member_id>/', views.MemberView.as_view(), name='Member'),

            path('', views.MembersView.as_view(template_name='Chat/Members.html'), name='Members'),
        ])),

        path('', views.RoomView.as_view(template_name='Chat/Room.html'), name='Room'),
    ])),
    
    path('', views.HomeView.as_view(template_name='Chat/Home.html'), name='Home')
]
