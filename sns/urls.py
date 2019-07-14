from django.urls import path

from . import views

urlpatterns = [
    path('', views.profile_search, name='profile_search'),
    path('profiles/', views.ProfileList.as_view(), name='profile-list'),
    path('profile/<int:pk>/', views.ProfileDetail.as_view(), name='profile-detail'),
    path('profile/<int:pk>/edit/', views.profile_edit, name='profile_edit'),
    path('profile/new/', views.profile_new, name='profile_new'),
    path('activity/<int:pk>/', views.activity, name='activity'),
]
