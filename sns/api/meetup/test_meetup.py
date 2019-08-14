from .api import Meetup, requests
from .auth import OAuth2Code

from unittest import TestCase
from unittest.mock import Mock, patch

class TestApi(TestCase):

    def setUp(self):
        self.meetup = Meetup(auth=Mock())

    @patch.object(requests, 'get')
    def test_get_activity_with_valid_data(self, mock_get):
        # Default value
        pages = 20
        data = {
            'results': ['result'],
            'meta': {'next': 'https://nextpageeee.com'},
        }
        mock_get.return_value.json.return_value = data

        result = self.meetup.get_activity()

        self.assertEqual(len(result), pages)
        self.assertEqual(result, data.get('results')*pages)

    @patch.object(requests, 'get')
    def test_get_activity_with_valid_data_but_less_pages_than_default(self, mock_get):
        data = [
            {'results': ['result'], 'meta': {'next': 'url1'}},
            {'results': ['result'], 'meta': {'next': 'url2'}},
            {'results': ['result'], 'meta': {'next': ''}},
        ]
        mock_get.return_value.json.side_effect = data

        result = self.meetup.get_activity()
        self.assertEqual(len(result), len(data))
        self.assertEqual(result, [d.get('results')[0] for d in data])

    @patch.object(requests, 'get')
    def test_get_activity_with_error_data(self, mock_get):
        mock_get.return_value.json.return_value  = {'error': '404'}
        self.assertEqual(self.meetup.get_activity(), [])

    @patch.object(requests, 'get')
    def test_get_member(self, mock_get):
        pass