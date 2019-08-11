import logging
import os
import tweepy

logger = logging.getLogger(__name__)


class Twitter:

    def __init__(self, consumer_key=None, consumer_secret_key=None):
        self.consumer_key = consumer_key or os.getenv('TWITTER_CONSUMER_KEY')
        self.consumer_secret_key = consumer_secret_key or os.getenv('TWITTER_CONSUMER_SECRET_KEY')

        auth = tweepy.AppAuthHandler(self.consumer_key, self.consumer_secret_key)
        self.api = tweepy.API(
            auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True
        )

    @staticmethod
    def profile_url(id):
        return 'https://twitter.com/%s' % str(id)

    def get_tweets(self, id, num=10):
        try:
            tweets = []
            for t in tweepy.Cursor(self.api.user_timeline, id=id).items(num):
                tweets.append({'status_id': t.id_str, 'text': t.text, 'created': t.created_at, 'user': t.user})
            return tweets
        except tweepy.TweepError:
            logger.exception('Error! Failed to get tweets.')
