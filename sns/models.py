from django.db import models

class Person(models.Model):
    name = models.CharField(max_length=20)
    facebook_acct = models.CharField(max_length=50)
    instagram_acct = models.CharField(max_length=30)
    reddit_acct = models.CharField(max_length=20)
    spotify_acct = models.CharField(max_length=30)
    twitter_acct = models.CharField(max_length=20)
