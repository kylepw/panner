from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView, ListView

from .api.utils import twitter_activity
from .forms import ProfileForm
from .models import Profile


class ProfileList(ListView):
    model = Profile
    context_object_name = 'profiles'
    paginate_by = 20


class Activity(DetailView):
    model = Profile
    context_object_name = 'profile'
    template_name = "sns/activity.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if context['profile'].twitter:
            context['twitter'] = twitter_activity(context['profile'].twitter)
        return context


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
            messages.add_message(request, messages.SUCCESS, "Changes to '%s' saved." % post.name)
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
            profile = Profile.objects.get(name=query)
            return redirect('activity', pk=profile.pk)
        except Profile.DoesNotExist:
            messages.error(request, "'%s' doesn't exist. Try again." % query)
            return redirect(request.META.get('HTTP_REFERER', 'profile_search'))
    profile_exists = Profile.objects.all().exists()
    return render(request, 'sns/profile_search.html', {'profile_exists': profile_exists})