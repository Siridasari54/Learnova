from django.urls import path
from . import views

urlpatterns = [
    path('', views.room_list_view, name='room_list'),
    path('<int:pk>/', views.room_detail_view, name='room_detail'),
    path('create/', views.create_room_view, name='create_room'),
    path('<int:pk>/edit/', views.edit_room_view, name='edit_room'),
    path('<int:pk>/delete/', views.delete_room_view, name='delete_room'),
    path('<int:pk>/join/', views.join_room_view, name='join_room'),
    path('<int:pk>/leave/', views.leave_room_view, name='leave_room'),
    path('message/<int:pk>/delete/', views.delete_message_view, name='delete_message'),
]
