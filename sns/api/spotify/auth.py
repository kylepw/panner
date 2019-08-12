import logging
import os
import requests
from requests_oauthlib import OAuth2Session
import time

logger = logging.getLogger(__name__)


class OAuth2Bearer(requests.auth.AuthBase):
    """Authenticates API requests"""

    def __init__(self, bearer_token):
        self.bearer_token = bearer_token

    def __call__(self, request):
        request.headers['Authorization'] = 'Bearer ' + self.bearer_token
        return request


class OAuthHandler:
    """OAuth handler base"""

    OAUTH_HOST = 'accounts.spotify.com'
    OAUTH_ROOT = '/'

    def __init__(self, client_id=None, client_secret=None, token=None):
        self.client_id = client_id or os.getenv('SPOTIFY_CLIENT_ID')
        self.client_secret = client_secret or os.getenv('SPOTIFY_CLIENT_SECRET')
        self.token = token or {}

    def apply_auth(self):
        """Apply bearer token to header of each request"""
        return OAuth2Bearer(self.token.get('access_token'))

    def is_token_expired(self, token=None):
        if token and token.get('expires_at'):
            return time.time() > int(token.get('expires_at'))
        return time.time() > int(self.token.get('expires_at'))

    def _url_for_endpoint(self, endpoint):
        """Return full url to OAuth endpoint."""
        return 'https://' + self.OAUTH_HOST + self.OAUTH_ROOT + endpoint


class OAuth2Code(OAuthHandler):
    """OAuth 2 (code authorization flow) authentication handler

        >>> auth = OAuth2Code()
        >>> auth.authorization_url()
        'https://accounts.spotify.com/authorize?...'
        >>> # Redirect to URL above and copy response URL
        >>> auth_resp_url = 'https://127...'
        >>> auth.get_access(auth_resp_url)
        {'access_token': 'xxx', 'refresh_token': 'xxx', ...}

    """
    def __init__(
        self,
        client_id=None,
        client_secret=None,
        redirect_uri=None,
        token=None,
        scope=None,
    ):
        super().__init__(client_id=None, client_secret=None, token=None)
        self.redirect_uri = redirect_uri or os.getenv('SPOTIFY_REDIRECT_URI')
        self.scope = scope

        if self.token:
            self.oauth = OAuth2Session(self.client_id, token=self.token)
        else:
            self.oauth = OAuth2Session(
                self.client_id, redirect_uri=self.redirect_uri, scope=scope
            )

    def authorization_url(self):
        """Return authorization url"""
        return self.oauth.authorization_url(self._url_for_endpoint('authorize'))[0]

    def get_access(self, authorization_response):
        """Return fetched access-related token information (dict)."""
        self.token = self.oauth.fetch_token(
            self._url_for_endpoint('api/token'),
            include_client_id=self.client_id,
            client_secret=self.client_secret,
            authorization_response=authorization_response,
        )
        return self.token

    def refresh_token(self, refresh_token=None):
        """Refresh access token"""
        refresh_token = refresh_token or self.token.get('refresh_token')
        extra = {'client_id': self.client_id, 'client_secret': self.client_secret}
        self.token = self.oauth.refresh_token(
            self._url_for_endpoint('api/token'), refresh_token, **extra
        )
        return self.token


class OAuth2Client(OAuthHandler):
    """OAuth 2 (client credential flow) authentication handler

        >>> auth = OAuth2Client()
        {'access_token': 'xxx',  ...}

    """

    def __init__(self, client_id=None, client_secret=None, token=None):
        super().__init__(client_id, client_secret, token)
        if not token:
            r = requests.post(
                self._url_for_endpoint('api/token'),
                auth=(self.client_id, self.client_secret),
                data={'grant_type': 'client_credentials'},
            )
            data = r.json()
            if data.get('error'):
                raise ValueError(
                    'Failed to acquire access token with `%s` error: %s'
                    % (data.get('error', '?'), data.get('error_description', '?'))
                )
            if data.get('token_type', '').lower() != 'bearer':
                raise ValueError(
                    'Expected token_type to equal "bearer" but instead got %s'
                    % data.get('token_type')
                )
            if not data.get('expires_at'):
                # Add 'expires_at' value not included in client credential response
                data.update({'expires_at': time.time() + data.get('expires_in', 3600)})
                logger.debug(
                    "Added {'expires_at': %s} to token data", data['expires_at']
                )
            self.token = data
