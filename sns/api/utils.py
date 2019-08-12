"""Process data from API wrapper modules."""

from django.shortcuts import redirect
import logging

from .meetup import Meetup, OAuth2Code as MeetupOAuth
from .spotify import Spotify, OAuth2Client as SpotifyOAuth
from .twitter import Twitter
from .reddit import Reddit

logger = logging.getLogger(__name__)


class GetActivity:
    """Return activity data and process OAuth tokens in session."""

    @staticmethod
    def meetup(request, id):
        if request.session.get('meetup_token'):
            # Try to reuse stored token
            logger.info('Trying to reuse stored Meetup token...')
            auth = MeetupOAuth(token=request.session['meetup_token'])
            if auth.is_token_expired():
                logger.info('Meetup token expired. Refreshing...')
                request.session['meetup_token'] = auth.refresh_token()
                logger.debug('New Meetup token: %s', request.session.get('meetup_token'))
            try:
                logger.info('Fetching Meetup data')
                meetup = Meetup(auth)
                data = {
                    'user': {
                        'url': meetup.profile_url(id),
                        'img': meetup.get_member_photo(id),
                    },
                    'statuses': meetup.user_activity(id),
                }
                logger.debug('Meetup data: %s', data)
                return request, data
            except Exception:
                logger.exception('Failed to fetch data from Meetup API.')

        logger.warning('No Meetup token in request. Skipping data fetch')
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

            playlists = spotify.get_playlists(id).get('items')
            user = playlists[0].get('owner') if playlists else {}
            images = user.get('images') if user else []
            urls = user.get('external_urls') if user else {}
            data = {
                'user': {
                    'url': urls.get('spotify') if urls else 'https://open.spotify.com/user/%s' % str(id),
                    # Make another fetch for photo data as last resort
                    'img': images[0].get('url') if images else (spotify.profile_image_url(id) or ''),
                },
                'statuses': playlists,
            }
            return request, data

        except Exception:
            logger.exception('Failed to fetch data from Spotify API.')
            return request, None

    @staticmethod
    def reddit(request, username):
        """Return latest Reddit activity"""
        try:
            logger.info('Fetching Reddit data')
            reddit = Reddit()
            data = {
                'user': {
                    'url': reddit.profile_url(username),
                    'img': reddit.profile_image_url(username) or '',
                },
                'statuses': reddit.get_comments_submissions(username),
            }
            logger.debug('Reddit data: %s', data)
            return request, data
        except Exception:
            logger.exception('Failed to fetch data from Reddit API.')
            return request, None


    @staticmethod
    def twitter(request, id):
        """Return latest tweets"""
        try:
            logger.info('Fetching Twitter data')
            twitter = Twitter()
            statuses = twitter.get_tweets(id=id, num=5)
            user = statuses[0].get('user') if statuses else None
            data = {
                'user': {
                    'url': twitter.profile_url(id),
                    'img': user.profile_image_url if user else '',
                },
                'statuses': statuses,
            }
            logger.debug('Twitter data: %s', data)
            return request, data
        except Exception:
            logger.exception('Failed to fetch data from Twitter API.')
            return request, None
