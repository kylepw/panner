from django.urls import path

from . import views

urlpatterns = [
    path('<int:pk>/', views.content_view, name='reddit'),
]