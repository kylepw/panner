import logging
import requests
from auth import OAuth2Client

logger = logging.getLogger(__name__)


class Spotify:
    """Spotify API handler

        Client credential flow (read-only)
        >>> spotify = Spotify()
        >>> spotify.get_playlists('user_id')
        {"href":...}

        Authorization code flow (access to user data)
        >>> auth = OAuth2Code()
        >>> # OAuth2 dance... (see OAuth2Code docstring)
        >>> spotify = Spotify(auth)
        >>> spotify.get_playlists()
        {"href":...}

    """

    API_HOST = 'api.spotify.com'
    API_ROOT = '/v1/'

    def __init__(self, auth=None):
        if not auth:
            # Default to client credential flow
            auth = OAuth2Client()
        self.auth = auth

    def get_playlists(self, id=None):
        """Retrieve playlists that user created and follows."""
        if id:
            return requests.get(
                self._url_for_endpoint(f'users/{str(id)}/playlists'),
                auth=self.auth.apply_auth(),
            ).json()
        return requests.get(
            self._url_for_endpoint('me/playlists'), auth=self.auth.apply_auth()
        ).json()

    def get_profile(self, id=None):
        """Return profile information."""
        if id:
            return requests.get(
                self._url_for_endpoint(f'users/{str(id)}'), auth=self.auth.apply_auth()
            ).json()
        return requests.get(
            self._url_for_endpoint('me'), auth=self.auth.apply_auth()
        ).json()

    def profile_image_url(self, id=None):
        """Return profile image URL or None."""
        if id:
            profile = self.get_profile(id)
            images = profile.get('images') or []
            return images[0].get('url') if images else None

    def _url_for_endpoint(self, endpoint):
        return 'https://' + self.API_HOST + self.API_ROOT + endpoint
