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
    """OAuth 2.0 handler base"""

    OAUTH_HOST = 'secure.meetup.com'
    OAUTH_ROOT = '/oauth2/'

    def __init__(self, client_id=None, client_secret=None, token=None):
        self.client_id = client_id or os.getenv('MEETUP_CONSUMER_KEY')
        self.client_secret = client_secret or os.getenv('MEETUP_CONSUMER_SECRET_KEY')
        self.token = token or {}

    def apply_auth(self):
        """Apply bearer token to header of each request"""
        return OAuth2Bearer(self.token.get('access_token'))

    def is_token_expired(self, token=None):
        if token and token.get('expires_at'):
            return time.time() > float(token.get('expires_at') or 0)
        return time.time() > float(self.token.get('expires_at') or 0)

    def _url_for_endpoint(self, endpoint):
        """Return full url to OAuth endpoint."""
        return 'https://' + self.OAUTH_HOST + self.OAUTH_ROOT + endpoint


class OAuth2Code(OAuthHandler):
    """OAuth 2.0 authentication handler (authorization code flow)

        >>> auth = OAuth2Code()
        >>> auth.authorization_url()
        'https://secure.meetup.com/oauth2/authorize?...'
        >>> # Visit URL above in browser and copy response URL
        >>> auth_resp_url = 'https://127...'
        >>> auth.get_access(auth_resp_url)
        {'access_token': 'xxx', 'refresh_token': 'xxx', ...}

    """

    def __init__(
        self,
        client_id=None,
        client_secret=None,
        token=None,
        redirect_uri=None,
        scope=None,
    ):
        super().__init__(client_id, client_secret, token)
        self.redirect_uri = redirect_uri or os.getenv('MEETUP_REDIRECT_URI')
        self.scope = scope or []

        if token:
            self.oauth = OAuth2Session(self.client_id, token=self.token)
        else:
            self.oauth = OAuth2Session(
                self.client_id, redirect_uri=self.redirect_uri, scope=scope
            )

    def authorization_url(self):
        """Return authorization url"""
        return self.oauth.authorization_url(self._url_for_endpoint('authorize'))[0]

    def get_access(self, authorization_response):
        """Return fetched access-related token information (dict)"""
        self.token = self.oauth.fetch_token(
            self._url_for_endpoint('access'),
            include_client_id=self.client_id,
            client_secret=self.client_secret,
            authorization_response=authorization_response,
        )
        if not self.token.get('expires_at'):
            # Add convenient 'expires_at' value
            self.token.update(
                {'expires_at': time.time() + self.token.get('expires_in', 3600)}
            )
        return self.token

    def refresh_token(self, refresh_token=None):
        """Refresh access token"""
        refresh_token = refresh_token or self.token.get('refresh_token')
        extra = {'client_id': self.client_id, 'client_secret': self.client_secret}
        self.token = self.oauth.refresh_token(
            self._url_for_endpoint('access'), refresh_token, **extra
        )
        return self.token
