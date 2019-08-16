from ..api import datetime, logging, Meetup, pytz, requests

from unittest import TestCase
from unittest.mock import Mock, patch

logger = logging.getLogger('meetup.api')


class TestApi(TestCase):
    def setUp(self):
        self.meetup = Meetup(auth=Mock())

    @patch.object(requests, 'get')
    def test_get_activity_with_valid_data(self, mock_get):
        # Default value
        pages = 20
        data = {'results': ['result'], 'meta': {'next': 'https://nextpageeee.com'}}
        mock_get.return_value.json.return_value = data

        result = self.meetup.get_activity()

        self.assertEqual(len(result), pages)
        self.assertEqual(result, data.get('results') * pages)

    @patch.object(requests, 'get')
    def test_get_activity_with_valid_data_but_less_pages_than_default(self, mock_get):
        data = [
            {'results': ['result'], 'meta': {'next': 'url1'}},
            {'results': ['result'], 'meta': {'next': 'url2'}},
            {'results': ['result'], 'meta': {'next': ''}},
        ]
        mock_get.return_value.json.side_effect = data

        result = self.meetup.get_activity()
        self.assertEqual(len(result), len(data))
        self.assertEqual(result, [d.get('results')[0] for d in data])

    @patch.object(requests, 'get')
    def test_get_activity_with_error_data(self, mock_get):
        mock_get.return_value.json.return_value = {'error': '404'}
        self.assertEqual(self.meetup.get_activity(), [])

    @patch.object(requests, 'get')
    def test_get_member_with_valid_id(self, mock_get):
        response = {'id': '1234', 'last_event': 'party'}
        mock_get.return_value.json.return_value = response
        self.assertEqual(self.meetup.get_member('1234'), response)

    @patch.object(requests, 'get')
    @patch.object(logger, 'exception')
    def test_get_member_with_error_response(self, mock_exception, mock_get):
        response = {'errors': '401'}
        id = '666'
        mock_get.return_value.json.return_value = response

        self.assertIsNone(self.meetup.get_member(id))
        mock_exception.assert_called_once_with(
            'Failed to get member %s: %s', id, response.get('errors')
        )

    def test_get_member_photo_with_valid_data(self):
        data = {'photo': {'thumb_link': 'url'}}
        self.meetup.get_member = Mock(return_value=data)
        self.assertEqual(
            self.meetup.get_member_photo(), data.get('photo').get('thumb_link')
        )

    def test_get_member_photo_with_no_thumbnail(self):
        self.meetup.get_member = Mock(return_value={'photo': {'some_link': 'url'}})
        self.assertIsNone(self.meetup.get_member_photo())

    def test_is_member(self):
        self.meetup.get_member = Mock(return_value={'id': 'id'})
        self.assertTrue(self.meetup.is_member())

    def test_user_activity(self):
        id = '1234'
        data = [
            {'member_id': 'foo'},
            {'member_id': id, 'created': 1, 'published': 2},
            {'member_id': 'bar'},
            {'member_id': id, 'published': 2},
            {'member_id': 'jesus'},
        ]
        excepted_result = [
            {'member_id': id, 'created': 1, 'published': 2},
            {'member_id': id, 'created': 9, 'published': 2},
        ]
        self.meetup.get_activity = Mock(return_value=data)
        Meetup._us_to_utc = Mock(return_value=9)
        self.assertEqual(self.meetup.user_activity(id), excepted_result)

    def test_us_to_utc(self):
        self.assertIsNone(self.meetup._us_to_utc('1234'))
        self.assertIsNone(self.meetup._us_to_utc('Sun Jul 14 20:00:00 2019'))
        self.assertIsNone(self.meetup._us_to_utc('Sun Jul 17 08:00:00 JST 2019'))
        self.assertEqual(
            self.meetup._us_to_utc('Tue Jul 30 20:13:35 EDT 2019'),
            datetime(2019, 7, 31, 0, 13, 35, tzinfo=pytz.utc),
        )
        self.assertEqual(
            self.meetup._us_to_utc('Sun Jun 16 08:24:49 EDT 2019'),
            datetime(2019, 6, 16, 12, 24, 49, tzinfo=pytz.utc),
        )
