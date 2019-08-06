import pdb
from unittest import TestCase
from unittest.mock import call, Mock, MagicMock, patch

from reddit import datetime, logging, os, prawcore, PrawReddit, pytz, Reddit
from praw.models import Comment, Submission

logger = logging.getLogger('reddit')


class RedditTests(TestCase):

    def setUp(self):
        patch_datetime = patch('reddit.datetime')
        patch_pytz = patch('reddit.pytz')

        self.mock_datetime = patch_datetime.start()
        self.mock_pytz = patch_pytz.start()

        self.addCleanup(patch_datetime.stop)
        self.addCleanup(patch_pytz.stop)

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

    def test_get_comments_submissions_num_of_results(self):
        username = 'joe'
        num = 10

        mock_comment = MagicMock()
        mock_submission = MagicMock()
        comment_attrs = {
            'link_title': 'foo',
            'body_html': 'foo',
            'subreddit_name_prefixed': 'foo',
            'link_url': 'foo',
            'created_utc': 'foo',
        }
        submission_attrs = {
            'title': 'bar',
            'selftext_html': 'bar',
            'subreddit_name_prefixed': 'bar',
            'url': 'bar',
            'created_utc': 'bar',
        }
        mock_comment.configure_mock(**comment_attrs)
        mock_submission.configure_mock(**submission_attrs)

        mock_comments = MagicMock()
        mock_submissions = MagicMock()

        mock_comments.new.return_value = iter([mock_comment]*num)
        mock_submissions.new.return_value = iter([mock_submission]*num)

        mock_api = MagicMock()
        mock_api.redditor.return_value.comments = mock_comments
        mock_api.redditor.return_value.submissions = mock_submissions

        r = Reddit('id', 'secret', 'agent')
        r.api = mock_api
        print(len(r.get_comments_submissions(username, num=num)))

        chained_comments = call.redditor(username).comments.new(limit=num)
        chained_submissions = call.redditor(username).submissions.new(limit=num)

        call_list_comments = chained_comments.call_list()
        call_list_submissions = chained_submissions.call_list()

        mock_api.assert_has_calls(call_list_comments)
        mock_api.assert_has_calls(call_list_submissions)

        mock_comments.new.assert_called_with(limit=num)


