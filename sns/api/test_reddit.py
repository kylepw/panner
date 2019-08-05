from unittest import TestCase
from unittest.mock import patch

from reddit import datetime, logging, os, prawcore, PrawReddit, pytz, Reddit

logger = logging.getLogger('reddit')


class RedditTests(TestCase):

    def test_praw_reddit_called_when_making_instance(self):
        with patch('reddit.PrawReddit') as MockPrawReddit:
            p = MockPrawReddit.return_value
            p.client_id = 'id'
            p.client_secret = 'secret'
            p.user_agent = 'agent'

            Reddit('id', 'secret', 'agent')

        MockPrawReddit.assert_called_once_with(
            client_id='id', client_secret='secret', user_agent='agent', read_only=True
        )
