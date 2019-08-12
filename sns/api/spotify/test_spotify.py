from api import Spotify
from auth import OAuth2Client

from unittest import TestCase
from unittest.mock import Mock


class TestApi(TestCase):

    def setUp(self):
        self.id = 'deerhunter_official'
        self.spotify = Spotify()

    def test_get_playlists(self):
        self.assertEqual(self.spotify.get_playlists(self.id), {'playlists': 'data'})