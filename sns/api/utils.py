"""
    utils.py
    ~~~~~~~~

    Process data from API wrapper modules.

"""
from .twitter import TwitterAPI

def get_tweets(twitter_id):
    """Return latest tweets"""
    api = TwitterAPI()
    return api.get_tweets(id=twitter_id)