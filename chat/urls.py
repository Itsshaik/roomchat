from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.room_list, name='room_list'),
    path('create/', views.create_room, name='create_room'),
    path('room/<int:room_id>/', views.chat_room, name='chat_room'),
    path('room/<int:room_id>/join/', views.join_room, name='join_room'),
    path('room/<int:room_id>/leave/', views.leave_room, name='leave_room'),
]
