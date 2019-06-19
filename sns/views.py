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