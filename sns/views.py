from django.contrib import messages
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView, ListView

from sns.api.meetup import OAuth2Code as MeetupOAuth
from sns.api.utils import GetActivity
from sns.forms import ProfileForm
from sns.models import Profile


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
        for sns, acct in context['profile'].get_fields():
            if sns and acct:
                self.request, context['data'][sns] = getattr(GetActivity, sns)(
                    self.request, acct
                )
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
            profile = Profile.objects.get(name=query)
            return redirect('activity', pk=profile.pk)
        except Profile.DoesNotExist:
            messages.error(request, "'%s' doesn't exist. Try again." % query)
            return redirect(request.META.get('HTTP_REFERER', 'profile_search'))
    profile_exists = Profile.objects.all().exists()
    return render(
        request, 'sns/profile_search.html', {'profile_exists': profile_exists}
    )


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
