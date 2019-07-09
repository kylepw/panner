from django.db.utils import DataError, IntegrityError
from django.test import TestCase

from ..models import Profile


class ProfileModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.FIELDS = {
            'meetup': '356770692',
            'reddit': 'jjjjerry',
            'twitter': 'jerryinthewild318',
        }

        cls.a = Profile.objects.create(
            name='Jerry',
            meetup=cls.FIELDS['meetup'],
            reddit=cls.FIELDS['reddit'],
            twitter=cls.FIELDS['twitter'],
        )

    def test_name_label(self):
        name_label = self.a._meta.get_field('name').verbose_name
        self.assertEqual(name_label, 'name')

    def test_meetup_label(self):
        name_label = self.a._meta.get_field('meetup').verbose_name
        self.assertEqual(name_label, 'meetup')

    def test_reddit_label(self):
        name_label = self.a._meta.get_field('reddit').verbose_name
        self.assertEqual(name_label, 'reddit')

    def test_spotify_label(self):
        name_label = self.a._meta.get_field('spotify').verbose_name
        self.assertEqual(name_label, 'spotify')

    def test_name_twitter(self):
        name_label = self.a._meta.get_field('twitter').verbose_name
        self.assertEqual(name_label, 'twitter')

    def test_cannot_create_models_with_same_names(self):
        with self.assertRaisesMessage(
            IntegrityError, 'duplicate key value violates unique constraint'
        ):
            Profile.objects.create(name='Jerry')

    def test_str_representation(self):
        self.assertEqual(str(self.a), self.a.name)

    def test_get_fields_outputs_correct_fields_data(self):
        for name, val in self.FIELDS.items():
            self.assertIn((name, val), self.a.get_fields())

    def test_get_fields_excludes_id_and_name_fields(self):
        fields = [field for field, _ in self.a.get_fields()]

        self.assertNotIn('id', fields)
        self.assertNotIn('name', fields)

    def test_name_set_to_None(self):
        with self.assertRaises(IntegrityError):
            Profile.objects.create(name=None)

    def test_name_max_length(self):
        max_length = self.a._meta.get_field('name').max_length

        self.assertEqual(max_length, 20)

    def test_meetup_max_length(self):
        max_length = self.a._meta.get_field('meetup').max_length

        self.assertEqual(max_length, 20)

    def test_reddit_max_length(self):
        max_length = self.a._meta.get_field('reddit').max_length

        self.assertEqual(max_length, 20)

    def test_spotify_max_length(self):
        max_length = self.a._meta.get_field('spotify').max_length

        self.assertEqual(max_length, 30)

    def test_twitter_max_length(self):
        max_length = self.a._meta.get_field('twitter').max_length

        self.assertEqual(max_length, 20)

    def test_name_that_is_too_long(self):
        with self.assertRaisesMessage(DataError, 'value too long'):
            Profile.objects.create(name='Jjjjjjjjjjjjjjjjjjjjjerry')

    def test_get_absolute_url(self):
        pk = self.a.pk
        self.assertEqual(self.a.get_absolute_url(), f'/profile/{pk}/')
