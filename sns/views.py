from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import DetailView, ListView

from .models import Profile


class ProfileList(ListView):
    model = Profile
    context_object_name = 'profiles'


class ProfileDetail(DetailView):
    model = Profile
    context_object_name = 'profile'


def profile_new(request):
    return HttpResponse('Create new profile.')

def profile_edit(request, pk):
    return HttpResponse('Edit profile %s' % str(pk))

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
