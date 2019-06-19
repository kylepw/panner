from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import DetailView, ListView

from .models import Person


class PersonList(ListView):
    model = Person
    context_object_name = 'people'


class PersonDetail(DetailView):
    model = Person
    context_object_name = 'person'


def facebook_view(request, pk):
    return HttpResponse('Facebook feed for user %s' % str(pk))

def instagram_view(request, pk):
    return HttpResponse('Instagram feed for user %s' % str(pk))

def reddit_view(request, pk):
    return HttpResponse('Reddit feed for user %s' % str(pk))

def spotify_view(request, pk):
    return HttpResponse('Spotify feed for user %s' % str(pk))

def twitter_view(request, pk):
    return HttpResponse('Twitter feed for user %s' % str(pk))
