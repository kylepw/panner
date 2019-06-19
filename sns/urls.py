from django.urls import path

from . import views

urlpatterns = [
    path('', views.PersonList.as_view(), name='person-list'),
    path('<int:pk>/', views.PersonDetail.as_view(), name='person-detail'),
    # path('<int:pk>/twitter', views.twitter_view, name='twitter')
]