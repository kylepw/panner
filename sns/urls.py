from django.urls import path

from . import views

urlpatterns = [
    path('', views.ProfileList.as_view(), name='profile-list'),
    path('profile/<int:pk>/', views.ProfileDetail.as_view(), name='profile-detail'),
    path('profile/<int:pk>/edit/', views.profile_edit, name='profile_edit'),
    path('profile/new/', views.profile_new, name='profile_new'),
    path('facebook/<int:pk>/', views.facebook_view, name='facebook'),
    path('instagram/<int:pk>/', views.instagram_view, name='instagram'),
    path('reddit/<int:pk>/', views.reddit_view, name='reddit'),
    path('spotify/<int:pk>/', views.spotify_view, name='spotify'),
    path('twitter/<int:pk>/', views.twitter_view, name='twitter'),
]