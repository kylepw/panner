from unittest import TestCase
from unittest.mock import patch

from .twitter import logging, os, tweepy, Twitter

logger = logging.getLogger('twitter')


class TwitterTests(TestCase):
    def setUp(self):
        patch_consumer_key = patch.object(Twitter, '_CONSUMER_KEY')
        patch_secret_key = patch.object(Twitter, '_CONSUMER_SECRET_KEY')
        patch_appauth = patch('tweepy.AppAuthHandler')
        patch_api = patch('tweepy.API')

        self.mock_consumer_key = patch_consumer_key.start()
        self.mock_secret_key = patch_secret_key.start()
        self.mock_appauth = patch_appauth.start()
        self.mock_api = patch_api.start()

        self.addCleanup(patch_consumer_key.stop)
        self.addCleanup(patch_secret_key.stop)
        self.addCleanup(patch_appauth.stop)
        self.addCleanup(patch_api.stop)

    def test_tweepy_objects_called_when_making_api_instance(self):
        Twitter()

        self.mock_appauth.assert_called_once_with(
            self.mock_consumer_key, self.mock_secret_key
        )
        self.mock_api.assert_called_once()

    def test_cursor_called_when_get_tweets_called(self):
        id = '123'
        api = Twitter()

        with patch('tweepy.Cursor') as mock_cursor:
            api.get_tweets(id)

        mock_cursor.assert_called_once_with(api.api.user_timeline, id=id)

    @patch.object(logger, 'exception')
    def test_nothing_returned_when_exception_called(self, mock_exception):
        api = Twitter()

        with patch('tweepy.Cursor', side_effect=mock_exception) as mock_cursor:
            api.get_tweets('123')

        mock_cursor.assert_called_once()
        mock_exception.assert_called_once()
