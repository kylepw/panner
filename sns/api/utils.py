"""
    utils.py
    ~~~~~~~~

    Process data from API wrapper modules.

"""
from .twitter import TwitterAPI

def twitter_activity(twitter_id):
    """Return latest Twitter tweets"""
    api = TwitterAPI()
    return api.get_tweets(id=twitter_id, num=5)