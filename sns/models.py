from django.db import models

class Profile(models.Model):
    name = models.CharField(max_length=20)
    facebook = models.CharField(max_length=50, blank=True)
    instagram = models.CharField(max_length=30, blank=True)
    reddit = models.CharField(max_length=20, blank=True)
    spotify = models.CharField(max_length=30, blank=True)
    twitter = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.name

    def get_fields(self):
        return [(f.name, getattr(self, f.name)) for f in Profile._meta.get_fields() if f.name not in ('id', 'name')]
