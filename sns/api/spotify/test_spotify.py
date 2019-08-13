from .api import Spotify
from .auth import OAuth2Client

from unittest import TestCase
from unittest.mock import patch, Mock


class TestApi(TestCase):

    @classmethod
    def setUpClass(cls):
        #cls.maxDiff = None
        cls.spotify = Spotify()

    def setUp(self):
        self.valid_id = 'deerhunter_official'
        self.invalid_id = 'dflkj4k523j423'

    def test_get_playlists_with_valid_id(self):
        self.assertIn('items', self.spotify.get_playlists(self.valid_id))

    def test_get_playlists_with_invalid_id(self):
        self.assertIn('error', self.spotify.get_playlists(self.invalid_id))

    def test_get_playlists_with_no_id(self):
        # Should error in read-only mode
        self.assertIn('error', self.spotify.get_playlists())

    def test_get_profile_with_valid_id(self):
        self.assertIn('display_name', self.spotify.get_profile(self.valid_id))

    def test_get_profile_with_invalid_id(self):
        self.assertIn('error', self.spotify.get_profile(self.invalid_id))

    def test_get_profile_with_no_id(self):
        # Should error in read-only mode
        self.assertIn('error', self.spotify.get_profile())

    @patch.object(Spotify, 'get_profile', return_value={'images':[{'url': 'http://foo.com/image.jpg'}]})
    def test_profile_image_url_with_valid_get_profile_return_value(self, mock_profile_image_url):
        self.assertEqual(self.spotify.profile_image_url('badid'), 'http://foo.com/image.jpg')

    @patch.object(Spotify, 'get_profile', return_value={'error':'404'})
    def test_profile_image_url_with_get_profile_fail(self, mock_profile_image_url):
        self.assertEqual(self.spotify.profile_image_url('badid'), None)