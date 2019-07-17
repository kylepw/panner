from datetime import datetime
import logging
import os
import tweepy

logger = logging.getLogger(__name__)


class Twitter:
    _CONSUMER_KEY = os.getenv('TWITTER_CONSUMER_KEY')
    _CONSUMER_SECRET_KEY = os.getenv('TWITTER_CONSUMER_SECRET_KEY')

    def __init__(self):
        auth = tweepy.AppAuthHandler(self._CONSUMER_KEY, self._CONSUMER_SECRET_KEY)
        self.api = tweepy.API(
            auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True
        )

    def get_tweets(self, id, num=10):
        try:
            tweets = []
            for t in tweepy.Cursor(self.api.user_timeline, id=id).items(num):
                tweets.append({'text': t.text, 'created': t.created_at})
            return tweets
        except tweepy.TweepError:
            logger.exception('Error! Failed to get tweets.')
