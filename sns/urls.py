from django.urls import path

from . import views

urlpatterns = [
    path('', views.profile_search, name='profile_search'),
    path('profiles/', views.ProfileList.as_view(), name='profile-list'),
    path('profile/<int:pk>/', views.Activity.as_view(), name='activity'),
    path('profile/<int:pk>/edit/', views.profile_edit, name='profile_edit'),
    path('profile/<int:pk>/del/', views.profile_delete, name='profile_delete'),
    path('profile/new/', views.profile_new, name='profile_new'),
    path('meetup/<int:pk>/dance/', views.meetup_dance, name='meetup_dance'),
    path('meetup/callback/', views.meetup_callback, name='meetup_callback'),
]
