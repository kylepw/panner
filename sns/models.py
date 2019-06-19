from django.db import models

class Person(models.Model):
    name = models.CharField(max_length=20)
    facebook = models.CharField(max_length=50, blank=True)
    instagram = models.CharField(max_length=30, blank=True)
    reddit = models.CharField(max_length=20, blank=True)
    spotify = models.CharField(max_length=30, blank=True)
    twitter = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.name
