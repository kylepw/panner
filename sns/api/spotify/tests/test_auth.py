from collections import namedtuple
from unittest import TestCase
from unittest.mock import Mock, patch

from ..auth import (
    logging,
    OAuth2Bearer,
    OAuth2Client,
    OAuth2Code,
    OAuthHandler,
    requests,
)

logger = logging.getLogger('spotify.auth')

# mocked request obj
Request = namedtuple('Request', 'headers, session')


class TestOAuth2Bearer(TestCase):
    def setUp(self):
        self.request = Request(headers={}, session={})

    def test_call_applies_header(self):
        token = '23l3kjlk'
        self.assertIsNone(self.request.headers.get('Authorization'))
        self.request = OAuth2Bearer(token)(self.request)
        self.assertEqual(self.request.headers.get('Authorization'), 'Bearer ' + token)


class TestOAuthHandler(TestCase):
    def setUp(self):
        token = {'access_token': 'lkj23'}
        self.oauth = OAuthHandler(client_id='id', client_secret='secret', token=token)

    def test_is_token_expired_with_expires_at_in_token(self):
        self.oauth.token['expires_at'] = 1565872294
        self.assertTrue(self.oauth.is_token_expired())

    def test_is_token_expired_without_expires_at_in_token(self):
        self.assertTrue(self.oauth.is_token_expired())

    def test_is_token_expired_with_expires_at_str(self):
        self.oauth.token['expires_at'] = '1565872294'
        self.assertTrue(self.oauth.is_token_expired())

    def test_is_token_expired_with_expires_token_argument(self):
        token = {'access_token': 'dfoasduf9', 'expires_at': 1565872294}
        self.assertTrue(self.oauth.is_token_expired(token))


class TestOAuth2Code(TestCase):
    def setUp(self):
        patch_oauth2session = patch('spotify.auth.OAuth2Session')
        self.mock_oauth2session = patch_oauth2session.start()

        self.addCleanup(patch_oauth2session.stop)

    def test_instance_without_token_passed(self):
        oauth = 'oauth object'
        self.mock_oauth2session.return_value = oauth

        self.assertEqual(
            OAuth2Code(
                client_id='id', client_secret='secret', redirect_uri='http://foobar'
            ).oauth,
            oauth,
        )
        self.mock_oauth2session.assert_called_once_with(
            'id', redirect_uri='http://foobar', scope=None
        )

    def test_instance_with_token_passed(self):
        oauth = 'oauth object'
        token = {'access_token': 'dfoasduf9', 'expires_at': 1565872294}
        self.mock_oauth2session.return_value = oauth

        auth = OAuth2Code(
            client_id='id',
            client_secret='secret',
            redirect_uri='http://foobar',
            token=token,
        )
        self.assertEqual(auth.oauth, oauth)
        self.assertEqual(auth.token, token)
        self.mock_oauth2session.assert_called_once_with('id', token=token)


class TestOAuth2Client(TestCase):
    def setUp(self):
        patch_post = patch.object(requests, 'post')
        self.mock_post = patch_post.start()

        self.token = {
            'access_token': 'BQDf7Lr1r',
            'token_type': 'Bearer',
            'expires_in': 3600,
            'scope': '',
            'expires_at': 1565878190.534921,
        }

        self.addCleanup(patch_post.stop)

    def test_valid_token_response(self):
        self.mock_post.return_value = Mock(json=Mock(return_value=self.token))
        self.assertEqual(
            OAuth2Client(client_id='id', client_secret='secret').token, self.token
        )

    def test_error_response(self):
        self.mock_post.return_value = Mock(
            json=Mock(
                return_value={'error': '401', 'error_description': 'You effed up'}
            )
        )
        with self.assertRaises(ValueError) as e:
            OAuth2Client(client_id='id', client_secret='secret')
        self.assertEqual(
            str(e.exception),
            'Failed to acquire access token with `401` error: You effed up',
        )

    def test_no_token_type_key(self):
        del self.token['token_type']
        self.mock_post.return_value = Mock(json=Mock(return_value=self.token))
        with self.assertRaises(ValueError) as e:
            OAuth2Client(client_id='id', client_secret='secret')
        self.assertEqual(
            str(e.exception),
            'Expected token_type to equal "bearer" but instead got None',
        )

    @patch.object(logger, 'debug')
    def test_token_without_expires_at_val_is_given_one(self, mock_debug):
        del self.token['expires_at']
        self.mock_post.return_value = Mock(json=Mock(return_value=self.token))
        self.assertTrue(OAuth2Client(client_id='id', client_secret='secret').token)
        mock_debug.assert_called_once()
