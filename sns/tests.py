from django.db.utils import IntegrityError
from django.test import TestCase

from .models import Profile


class ProfileModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.FIELDS = {
            'facebook': 'jerry@gmail.com',
            'reddit': 'jjjjerry',
            'twitter': 'jerryinthewild318',
        }

        # DON'T modify this in test methods!!
        cls.a = Profile.objects.create(
            name='Jerry',
            facebook=cls.FIELDS['facebook'],
            reddit=cls.FIELDS['reddit'],
            twitter=cls.FIELDS['twitter'],
        )

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