from django.db import models
from django.urls import reverse


class Profile(models.Model):
    # Postgres-specific case-insensitive
    name = models.CharField(max_length=20, unique=True)
    meetup = models.CharField(max_length=20, blank=True)
    reddit = models.CharField(max_length=20, blank=True)
    spotify = models.CharField(max_length=30, blank=True)
    twitter = models.CharField(max_length=20, blank=True)

    class Meta:
        ordering = ['pk']

    def get_absolute_url(self):
        return reverse('activity', args=[str(self.id)])

    def get_fields(self):
        return [
            (f.name, getattr(self, f.name))
            for f in Profile._meta.get_fields()
            if f.name not in ('id', 'name')
        ]

    def __str__(self):
        return self.name


