from datetime import datetime
import logging
import pytz
import re
import requests

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


class Meetup:
    """Meetup API handler

        >>> auth = OAuth2Handler()
        >>> auth.authorization_url()
        'https://secure.meetup.com/oauth2/authorize?...' # Access in web browser.
        >>> auth.get_access('https://.../callback?...')  # Pass in callback URI returned.
        >>> meetup = Meetup(auth)
        >>> meetup.get_member('member_id')
        {'country': ...}

    """

    API_HOST = 'api.meetup.com'
    API_ROOT = '/'

    def __init__(self, auth):
        self.auth = auth

    def get_activity(self, pages=20):
        """Retrieve activity feed for user's groups (GET /activity)"""
        results = []
        next_page = None
        for _ in range(pages):
            if next_page:
                data = requests.get(next_page, auth=self.auth.apply_auth()).json()
            else:
                data = requests.get(
                    self._url_for_endpoint('activity'), auth=self.auth.apply_auth()
                ).json()

            result = data.get('results')
            if result:
                result = result if isinstance(result, list) else [result]
                results.extend(result)

            next_page = data.get('meta').get('next') if data.get('meta') else None
            if not next_page:
                break

        return results

    def get_member(self, id='self'):
        """Retrieve a single member"""
        return requests.get(
            self._url_for_endpoint(f'2/member/{str(id)}'), auth=self.auth.apply_auth()
        ).json()

    def is_member(self, id='self'):
        """Return boolean if registered member or not."""
        return self.get_member(id).get('code') != 'not_found'

    def user_activity(self, id):
        """Retrieve recent activity of a user in one or more of your registered groups."""
        id = str(id)
        data = self.get_activity()
        activity = []
        for d in data:
            if d.get('member_id') == id:
                activity.append(d)

        # Add `created` values
        for a in activity:
            if not a.get('created') and a.get('published'):
                a['created'] = Meetup._us_to_utc(a.get('published'))

        return activity

    def _url_for_endpoint(self, endpoint):
        return 'https://' + self.API_HOST + self.API_ROOT + endpoint

    @staticmethod
    def _us_to_utc(date_str):
        """Convert local US date string to UTC datetime object."""
        if not isinstance(date_str, str):
            return
        US_TIMEZONES = {
            'CDT': 'US/Central',
            'CST': 'US/Central',
            'CT': 'US/Central',
            'EDT': 'US/Eastern',
            'EST': 'US/Eastern',
            'ET': 'US/Eastern',
            'MT': 'US/Mountain',
            'MDT': 'US/Mountain',
            'MST': 'US/Mountain',
            'PDT': 'US/Pacific',
            'PST': 'US/Pacific',
            'PT': 'US/Pacific',
        }
        tz_re = r'(\s*[A-Z]{2,3}\s*)'
        found_tz = re.search(tz_re, date_str)
        if not found_tz:
            return
        local_tz = pytz.timezone(US_TIMEZONES[found_tz.group().strip()])
        date_str = re.sub(tz_re, ' ', date_str)
        return pytz.utc.normalize(
            local_tz.localize(datetime.strptime(date_str, '%c')).astimezone(pytz.utc)
        )
