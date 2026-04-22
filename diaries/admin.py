from django.contrib import admin
from .models import DiaryEntry, Follow, Like, Comment, Profile

@admin.register(DiaryEntry)
class DiaryEntryAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'created_at', 'updated_at']
    list_filter = ['created_at', 'user']
    search_fields = ['title', 'content', 'user__username']
    ordering = ['-created_at']

@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ['follower', 'following', 'created_at']
    list_filter = ['created_at']
    search_fields = ['follower__username', 'following__username']


admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(Profile)
