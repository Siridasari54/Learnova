from django.contrib import admin
from .models import Topic, Room, RoomMembership, Message


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['name', 'host', 'topic', 'created_at']
    search_fields = ['name', 'host__username']
    list_filter = ['topic']


@admin.register(RoomMembership)
class RoomMembershipAdmin(admin.ModelAdmin):
    list_display = ['user', 'room', 'joined_at']


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['user', 'room', 'created_at']
    search_fields = ['body', 'user__username']
