from django.conf import settings
from django.contrib import messages
from django.core.cache import cache
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.cache import cache_page
from django.views.generic import DetailView, ListView

from .api.meetup import OAuth2Code as MeetupOAuth
from .api.utils import GetActivity
from .forms import ProfileForm
from .models import Profile

import json
import logging

logger = logging.getLogger(__name__)

API_CACHE_TTL = settings.API_CACHE_TTL


class ProfileList(ListView):
    model = Profile
    context_object_name = 'profiles'
    paginate_by = 20


class Activity(DetailView):
    model = Profile
    context_object_name = 'profile'
    template_name = 'sns/activity.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)

        # If Meetup account but no token, acquire one
        if self.object.meetup and not self.request.session.get('meetup_token'):
            return redirect('meetup_dance', pk=self.object.pk)

        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['data'] = {}
        profile_cache = cache.get_many(cache.keys(':'.join([str(context['profile'].pk), '*'])))
        for sns, acct in context['profile'].get_fields():
            if acct:
                key = ':'.join([str(context['profile'].pk), sns, acct])
                # Use cache if available
                if key in profile_cache:
                    context['data'][sns] = profile_cache[key]
                else:
                    self.request, context['data'][sns] = getattr(GetActivity, sns)(
                        self.request, acct
                    )
                    cache.set(key, context['data'][sns], API_CACHE_TTL)
        return context


def refresh_activity(request, pk):
    """Clear cache and reload activity view"""
    if request.method == 'GET':
        profile = get_object_or_404(Profile, pk=pk)
        cache.delete_many(cache.keys(':'.join([str(profile.pk), '*'])))
        return redirect('activity', pk=profile.pk)


def profile_new(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            post = form.save()
            messages.add_message(request, messages.SUCCESS, "Added '%s'." % post.name)
            return redirect('activity', pk=post.pk)
    else:
        form = ProfileForm()
    return render(request, 'sns/profile_edit.html', {'form': form})


def profile_edit(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            post = form.save()
            messages.add_message(
                request, messages.SUCCESS, "Changes to '%s' saved." % post.name
            )
            return redirect('activity', pk=post.pk)
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'sns/profile_edit.html', {'form': form})


def profile_delete(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    name = profile.name
    profile.delete()
    messages.add_message(request, messages.SUCCESS, "'%s' deleted." % name)
    return redirect('profile-list')


def profile_search(request):
    query = request.GET.get('profile_query')
    if query:
        try:
            # Match same name with different cased letters
            profile = Profile.objects.get(name__iexact=query)
            return redirect('activity', pk=profile.pk)
        except Profile.DoesNotExist:
            messages.error(request, "'%s' doesn't exist. Try again." % query)
            return redirect(request.META.get('HTTP_REFERER', 'profile_search'))
    profile_exists = Profile.objects.all().exists()
    return render(
        request, 'sns/profile_search.html', {'profile_exists': profile_exists}
    )

@cache_page(60 * 3)
def profile_autocomplete(request):
    """Return profiles matching autocomplete query"""
    if request.is_ajax():
        query = request.GET.get('term', '')
        profiles = Profile.objects.filter(name__istartswith=query)
        # Sort it so results show from shortest to longest
        data = json.dumps(sorted([p.name for p in profiles], key=len))
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def meetup_dance(request, pk):
    """Request oauth authentication code"""
    if request.method == 'GET':
        if not pk:
            raise Http404
        auth = MeetupOAuth()
        request.session['meetup_pk'] = pk
        return redirect(auth.authorization_url())


def meetup_callback(request):
    """Exchange oauth authentication code for access token"""
    if request.method == 'GET':
        pk = request.session.get('meetup_pk')
        if not pk:
            raise Http404
        del request.session['meetup_pk']
        auth = MeetupOAuth()
        request.session['meetup_token'] = auth.get_access(request.build_absolute_uri())
        return redirect('activity', pk=pk)
