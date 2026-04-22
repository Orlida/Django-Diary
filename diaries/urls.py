from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Home feed
    path('', views.home_view, name='home'),

    # Diary entries
    path('entry/new/', views.entry_create_view, name='entry_create'),
    path('entry/<int:pk>/', views.entry_detail_view, name='entry_detail'),
    path('entry/<int:pk>/edit/', views.entry_edit_view, name='entry_edit'),
    path('entry/<int:pk>/delete/', views.entry_delete_view, name='entry_delete'),

    # Profile & follow
    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('follow/<str:username>/', views.follow_view, name='follow'),
    path('unfollow/<str:username>/', views.unfollow_view, name='unfollow'),

    # Search
    path('search/', views.search_view, name='search'),

    #Like & Comment
    path('entry/<int:pk>/like/', views.like_view, name='like'),
    path('entry/<int:pk>/comment/', views.comment_view, name='comment'),

    #Edit profile
    path('profile/<str:username>/edit/', views.edit_profile_view, name='edit_profile'),

    #Checking followers and followings
    path('profile/<str:username>/followers/', views.followers_view, name='followers'),
    path('profile/<str:username>/following/', views.following_view, name='following'),
]