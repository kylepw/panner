from ..api import requests, Spotify

from unittest import TestCase
from unittest.mock import patch, Mock


class TestApi(TestCase):
    def setUp(self):
        self.spotify = Spotify(auth=Mock())

        patch_get = patch.object(requests, 'get')
        self.mock_get = patch_get.start()
        self.addCleanup(patch_get.stop)

    def test_get_playlists_with_valid_id(self):
        response = {'items': ['foobar']}
        self.mock_get.return_value.json.return_value = response
        self.assertIn('items', self.spotify.get_playlists('valid_id'))

    def test_get_playlists_with_invalid_id(self):
        response = {'error': '401'}
        self.mock_get.return_value.json.return_value = response
        self.assertIn('error', self.spotify.get_playlists('invalid_id'))

    def test_get_playlists_with_no_id(self):
        # Should error in read-only mode
        response = {'error': '404'}
        self.mock_get.return_value.json.return_value = response
        self.assertIn('error', self.spotify.get_playlists())

    def test_get_profile_with_valid_id(self):
        response = {'display_name': 'valid_id'}
        self.mock_get.return_value.json.return_value = response
        self.assertIn('display_name', self.spotify.get_profile('valid_id'))

    def test_get_profile_with_invalid_id(self):
        response = {'error': '401'}
        self.mock_get.return_value.json.return_value = response
        self.assertIn('error', self.spotify.get_profile('invalid_id'))

    def test_get_profile_with_no_id(self):
        # Should error in read-only mode
        response = {'error': '404'}
        self.mock_get.return_value.json.return_value = response
        self.assertIn('error', self.spotify.get_profile())

    @patch.object(
        Spotify,
        'get_profile',
        return_value={'images': [{'url': 'http://foo.com/image.jpg'}]},
    )
    def test_profile_image_url_with_valid_get_profile_return_value(
        self, mock_profile_image_url
    ):
        self.assertEqual(
            self.spotify.profile_image_url('badid'), 'http://foo.com/image.jpg'
        )

    @patch.object(Spotify, 'get_profile', return_value={'error': '404'})
    def test_profile_image_url_with_get_profile_fail(self, mock_profile_image_url):
        self.assertEqual(self.spotify.profile_image_url('badid'), None)


class TestAuth(TestCase):
    def test_something(self):
        pass
