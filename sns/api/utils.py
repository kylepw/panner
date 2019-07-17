"""Process data from API wrapper modules."""
from .spotify import Spotify
from .twitter import Twitter
from .reddit import get_comments_submissions

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
    """Return user's playlist information"""
    spotify = Spotify()

    # user_info = spotify.get_profile(profile.spotify)
    return spotify.get_playlists(id)

def _get_reddit(username):
    """Return latest Reddit activity"""
    return get_comments_submissions(username)

def _get_twitter(id):
    """Return latest tweets"""
    api = Twitter()
    return api.get_tweets(id=id, num=5)
