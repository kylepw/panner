from api.reddit.reddit import logging, NotFound, Reddit
from requests import Response
from unittest import TestCase
from unittest.mock import call, Mock, MagicMock, patch

logger = logging.getLogger('api.reddit.reddit')


class RedditTests(TestCase):
    def test_praw_reddit_called_when_making_instance(self):
        client_id = 'id'
        client_secret = 'secret'
        user_agent = 'agent'

        with patch('api.reddit.reddit.PrawReddit') as MockPrawReddit:
            p = MockPrawReddit.return_value
            p.client_id = client_id
            p.client_secret = client_secret
            p.user_agent = user_agent

            Reddit(client_id, client_secret, user_agent)

        MockPrawReddit.assert_called_once_with(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent,
            read_only=True,
        )

    @patch.object(logger, 'exception')
    def test_profile_image_url_logs_on_notfound_exception(self, mock_logger):
        username = 'joe'

        r = Reddit('id', 'secret', 'agent')
        r.api = Mock()

        r.api.redditor.side_effect = NotFound(Response())
        r.profile_image_url(username)

        mock_logger.assert_called_once_with(
            'Failed to fetch Reddit profile image of %s', username
        )


class GetCommentsSubmissionsTest(TestCase):
    def setUp(self):
        self.mock_api = MagicMock()

        patch_datetime = patch('api.reddit.reddit.datetime')
        patch_pytz = patch('api.reddit.reddit.pytz')

        self.mock_datetime = patch_datetime.start()
        self.mock_pytz = patch_pytz.start()

        self.addCleanup(patch_datetime.stop)
        self.addCleanup(patch_pytz.stop)

    def mock_comments_submissions(self, num=5):
        """Return tuple of mock comments and submissions"""

        # Pretend API limit at 20 results per call
        num = num if num < 20 else 20

        mock_comment = Mock()
        mock_submission = Mock()

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
        mock_comments.new.return_value = iter([mock_comment] * num)
        mock_submissions.new.return_value = iter([mock_submission] * num)

        return mock_comments, mock_submissions

    def test_comments_submissions_calls(self):
        username = 'joe'

        r = Reddit('id', 'secret', 'agent')
        r.api = self.mock_api
        r.get_comments_submissions(username)

        chained_comments = call.redditor(username).comments.new(limit=5)
        chained_submissions = call.redditor(username).submissions.new(limit=5)

        call_list_comments = chained_comments.call_list()
        call_list_submissions = chained_submissions.call_list()

        r.api.assert_has_calls(call_list_comments)
        r.api.assert_has_calls(call_list_submissions)

    def test_num_of_results_0(self):
        num = 0

        mock_comments, mock_submissions = self.mock_comments_submissions(num)
        self.mock_api.redditor.return_value.comments = mock_comments
        self.mock_api.redditor.return_value.submissions = mock_submissions

        r = Reddit('id', 'secret', 'agent')
        r.api = self.mock_api

        self.assertEqual(len(r.get_comments_submissions('joe', num=num)), 0)

    def test_num_of_results_7(self):
        num = 7

        mock_comments, mock_submissions = self.mock_comments_submissions(num)
        self.mock_api.redditor.return_value.comments = mock_comments
        self.mock_api.redditor.return_value.submissions = mock_submissions

        r = Reddit('id', 'secret', 'agent')
        r.api = self.mock_api

        self.assertEqual(len(r.get_comments_submissions('joe', num=num)), 7)

    def test_num_of_results_100(self):
        num = 100

        mock_comments, mock_submissions = self.mock_comments_submissions(num)
        self.mock_api.redditor.return_value.comments = mock_comments
        self.mock_api.redditor.return_value.submissions = mock_submissions

        r = Reddit('id', 'secret', 'agent')
        r.api = self.mock_api

        # API results limited to 20 per call
        self.assertEqual(len(r.get_comments_submissions('joe', num=num)), 40)
