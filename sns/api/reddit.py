from datetime import datetime
from praw import Reddit
import pytz
import os

MAX = 5


def get_comments_submissions(username):
    reddit = Reddit(
        client_id=os.getenv('REDDIT_CLIENT_ID'),
        client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
        user_agent=os.getenv('REDDIT_USER_AGENT'),
        read_only=True,
    )
    coms = [
        dict(
            title=comment.link_title,
            text=comment.body_html,
            subreddit=comment.subreddit_name_prefixed,
            url=comment.link_url,
            created=datetime.fromtimestamp(comment.created_utc, pytz.utc),
        )
        for comment in reddit.redditor(username).comments.new(limit=5)
    ]
    subs = [
        dict(
            title=submission.title,
            text=submission.selftext_html,
            subreddit=submission.subreddit_name_prefixed,
            url=submission.url,
            created=datetime.fromtimestamp(submission.created_utc, pytz.utc),
        )
        for submission in reddit.redditor(username).submissions.new(limit=5)
    ]
    return coms + subs if len(coms + subs) < MAX else (coms + subs)[:MAX]

