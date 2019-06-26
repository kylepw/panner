from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView, ListView

from .forms import ProfileForm
from .models import Profile


class ProfileList(ListView):
    model = Profile
    context_object_name = 'profiles'
    paginate_by = 20


class ProfileDetail(DetailView):
    model = Profile
    context_object_name = 'profile'


def profile_new(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            post = form.save()
            return redirect('profile-detail', pk=post.pk)
    else:
        form = ProfileForm()
    return render(request, 'sns/profile_edit.html', {'form': form})


def profile_edit(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            post = form.save()
            return redirect('profile-detail', pk=post.pk)
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'sns/profile_edit.html', {'form': form})
