from django.urls import path, include
from . import views


app_name = 'Chat.api'

urlpatterns = [

    path('<slug:Room_Code>/', include([

        path('join/', views.JoinRoomAPI.as_view(), name='Join-Room'),

        path('settings/', include([

            path('cover/', views.RoomCoverSettingsAPI.as_view(), name='Cover-Settings'),

            path('', views.RoomSettingsAPI.as_view(), name='Settings'),
        ])),

        path('members/', include([

            path('<int:Member_id>/', views.MemberAPI.as_view(), name='Member'),

            path('', views.MembersAPI.as_view(), name='Members'),
        ])),

        path('messages/', views.MessagesAPI.as_view(), name='Messages'),

        path('', views.RoomAPI.as_view(), name='Room'),
    ])),

    path('', views.RoomsAPI.as_view(), name='Rooms'),
]
