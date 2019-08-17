from collections import namedtuple
import logging
from unittest import TestCase
from unittest.mock import patch
from api.utils import GetActivity

logger = logging.getLogger('api.utils')

# mocked request obj
Request = namedtuple('Request', 'headers, session')

class TestGetActivity(TestCase):
    """Test exception handling"""

    def setUp(self):
        self.mock_request = Request(headers={}, session={})
        self.id = 'jimmy'

        patch_exception = patch.object(logger, 'exception')
        self.mock_exception = patch_exception.start()
        self.addCleanup(patch_exception.stop)

    @patch('api.utils.Meetup', side_effect=Exception('Boom!'), autospec=True)
    @patch('api.utils.MeetupOAuth', autospec=True)
    def test_meetup(self, mock_meetupoauth, mock_meetup):
        # Required to reach `try` block
        self.mock_request.session['meetup_token'] = 'xxx'

        self.assertEqual(
            GetActivity().meetup(self.mock_request, self.id), (self.mock_request, None)
        )
        self.mock_exception.assert_called_once_with(
            'Failed to fetch data from Meetup API.'
        )

    @patch('api.utils.Spotify', side_effect=Exception('Boom!'), autospec=True)
    def test_spotify(self, mock_spotify):
        self.assertEqual(
            GetActivity().spotify(self.mock_request, self.id), (self.mock_request, None)
        )
        self.mock_exception.assert_called_once_with(
            'Failed to fetch data from Spotify API.'
        )

    @patch('api.utils.Reddit', side_effect=Exception('Boom!'), autospec=True)
    def test_reddit(self, mock_spotify):
        self.assertEqual(
            GetActivity().reddit(self.mock_request, self.id), (self.mock_request, None)
        )
        self.mock_exception.assert_called_once_with(
            'Failed to fetch data from Reddit API.'
        )

    @patch('api.utils.Twitter', side_effect=Exception('Boom!'), autospec=True)
    def test_twitter(self, mock_twitter):
        self.assertEqual(
            GetActivity().twitter(self.mock_request, self.id), (self.mock_request, None)
        )
        self.mock_exception.assert_called_once_with(
            'Failed to fetch data from Twitter API.'
        )
