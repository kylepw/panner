"""Process data from API wrapper modules."""
from .twitter import Twitter


def get_activity(sns, acct):
    """Return activity data."""
    DATA = {
        'meetup': _get_meetup,
        'reddit': _get_reddit,
        'spotify': _get_spotify,
        'twitter': _get_twitter,
    }

    if sns in DATA:
        return DATA[sns](acct)
    return

def _get_meetup(id):
    return

def _get_spotify(id):
    return

def _get_reddit(username):
    return

def _get_twitter(id):
    """Return latest Twitter tweets"""
    api = Twitter()
    return api.get_tweets(id=id, num=5)
