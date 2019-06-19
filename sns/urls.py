from django.urls import path

from . import views

urlpatterns = [
    path('', views.PersonList.as_view(), name='person-list'),
    path('profile/<int:pk>/', views.PersonDetail.as_view(), name='person-detail'),
    path('facebook/<int:pk>/', views.facebook_view, name='facebook'),
    path('instagram/<int:pk>/', views.instagram_view, name='instagram'),
    path('reddit/<int:pk>/', views.reddit_view, name='reddit'),
    path('spotify/<int:pk>/', views.spotify_view, name='spotify'),
    path('twitter/<int:pk>/', views.twitter_view, name='twitter'),
]