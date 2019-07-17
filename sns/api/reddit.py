from datetime import datetime
from praw import Reddit
import os


def get_comments_submissions(username):
    reddit = Reddit(
        client_id=os.getenv('REDDIT_CLIENT_ID'),
        client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
        user_agent=os.getenv('REDDIT_USER_AGENT'),
        read_only=True,
    )
    comments = [
        dict(
            title=comment.link_title,
            text=comment.body_html,
            subreddit=comment.subreddit_name_prefixed,
            url=comment.link_url,
            created=datetime.utcfromtimestamp(int(comment.created)).strftime(
                '%Y-%m-%d %H:%M:%S'
            ),
        )
        for comment in reddit.redditor(username).comments.new(limit=5)
    ]
    submissions = [
        dict(
            title=submission.title,
            text=submission.selftext_html,
            subreddit=submission.subreddit_name_prefixed,
            url=submission.url,
            created=datetime.utcfromtimestamp(int(submission.created)).strftime(
                '%Y-%m-%d %H:%M:%S'
            ),
        )
        for submission in reddit.redditor(username).submissions.new(limit=5)
    ]
    data = comments + submissions
    return data