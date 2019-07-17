"""
    utils.py
    ~~~~~~~~

    Process data from API wrapper modules.

"""
from .twitter import Twitter

def twitter_activity(twitter_id):
    """Return latest Twitter tweets"""
    api = Twitter()
    return api.get_tweets(id=twitter_id, num=5)