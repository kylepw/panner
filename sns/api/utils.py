"""Process data from API wrapper modules."""

from django.shortcuts import redirect
import logging

from .meetup import Meetup, OAuth2Code as MeetupOAuth
from .spotify import Spotify, OAuth2Client as SpotifyOAuth
from .twitter import Twitter
from .reddit import get_comments_submissions

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


class GetActivity:
    """Return activity data and add OAuth info to session."""

    @staticmethod
    def meetup(request, id):
        if request.session['meetup_token']:
            # Try to reuse stored token
            auth = MeetupOAuth(token=request.session['meetup_token'])
            if auth.is_token_expired():
                request.session['meetup_token'] = auth.refresh_token()
            try:
                meetup = Meetup(auth)
                return request, meetup.user_activity(id)
            except Exception:
                logger.exception('Failed to fetch data from Meetup API.')

        return request, None

    @staticmethod
    def spotify(request, id):
        """Return user's playlist information"""
        try:
            if request.session.get(
                'spotify_token'
            ) and not SpotifyOAuth().is_token_expired(request.session['spotify_token']):
                # Reuse stored token
                spotify = Spotify(
                    auth=SpotifyOAuth(token=request.session['spotify_token'])
                )
            else:
                spotify = Spotify()
                request.session['spotify_token'] = spotify.auth.token

            return request, spotify.get_playlists(id).get('items')

        except Exception:
            logger.exception('Failed to fetch data from Spotify API.')
            return request, None

    @staticmethod
    def reddit(request, username):
        """Return latest Reddit activity"""
        return request, get_comments_submissions(username)

    @staticmethod
    def twitter(request, id):
        """Return latest tweets"""
        api = Twitter()
        return request, api.get_tweets(id=id, num=5)
