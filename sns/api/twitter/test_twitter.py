from unittest import TestCase
from unittest.mock import patch

from api.twitter.twitter import logging, Twitter

logger = logging.getLogger('twitter')


class TwitterTests(TestCase):
    def setUp(self):
        patch_appauth = patch('api.twitter.twitter.tweepy.AppAuthHandler', autospec=True)
        patch_api = patch('api.twitter.twitter.tweepy.API', autospec=True)

        self.mock_appauth = patch_appauth.start()
        self.mock_api = patch_api.start()

        self.addCleanup(patch_appauth.stop)
        self.addCleanup(patch_api.stop)

    def test_tweepy_objects_called_when_making_api_instance(self):
        Twitter('id', 'secret')

        self.mock_appauth.assert_called_once_with('id', 'secret')
        self.mock_api.assert_called_once()

    def test_cursor_called_when_get_tweets_called(self):
        id = '123'
        api = Twitter('id', 'secret')

        with patch('tweepy.Cursor', autospec=True) as mock_cursor:
            api.get_tweets(id)

        mock_cursor.assert_called_once_with(api.api.user_timeline, id=id)

    @patch.object(logger, 'exception')
    def test_nothing_returned_when_exception_called(self, mock_exception):
        api = Twitter('id', 'secret')

        with patch('tweepy.Cursor', side_effect=mock_exception, autospec=True) as mock_cursor:
            api.get_tweets('123')

        mock_cursor.assert_called_once()
        mock_exception.assert_called_once()
