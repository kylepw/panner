from datetime import datetime
import logging
import os
from praw import Reddit as PrawReddit
from prawcore.exceptions import NotFound
import pytz

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


class Reddit:

    def __init__(self, client_id=None, client_secret=None, user_agent=None):
        self.client_id = client_id or os.getenv('REDDIT_CLIENT_ID')
        self.client_secret = client_secret or os.getenv('REDDIT_CLIENT_SECRET')
        self.user_agent = user_agent or os.getenv('REDDIT_USER_AGENT')

        self.api = PrawReddit(
            client_id=self.client_id,
            client_secret=self.client_secret,
            user_agent=self.user_agent,
            read_only=True,
        )

    def get_comments_submissions(self, username, num=5):
        """Return max `num` of comments and submissions by `username`."""
        coms = [
            dict(
                title=comment.link_title,
                text=comment.body_html,
                subreddit=comment.subreddit_name_prefixed,
                url=comment.link_url,
                created=datetime.fromtimestamp(comment.created_utc, pytz.utc),
            )
            for comment in self.api.redditor(username).comments.new(limit=num)
        ]
        subs = [
            dict(
                title=submission.title,
                text=submission.selftext_html,
                subreddit=submission.subreddit_name_prefixed,
                url=submission.url,
                created=datetime.fromtimestamp(submission.created_utc, pytz.utc),
            )
            for submission in self.api.redditor(username).submissions.new(limit=num)
        ]
        return coms + subs if len(coms + subs) < num else (coms + subs)[:num]

    def profile_image_url(self, username):
        """Return URL of user's avatar image."""
        try:
            return self.api.redditor(username).icon_img
        except NotFound:
            logger.exception('Failed to fetch Reddit profile image of %s', username)
            return None

    @staticmethod
    def profile_url(username):
        """Return URL of user's profile."""
        return 'https://www.reddit.com/user/%s' % username



