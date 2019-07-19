from django.test import TestCase

from sns.forms import ProfileForm
from sns.models import Profile


class ProfileFormTests(TestCase):
    def test_form_labels(self):
        form = ProfileForm()

        self.assertEqual(form.fields['name'].label, 'Name')
        self.assertEqual(form.fields['meetup'].label, 'Meetup')
        self.assertEqual(form.fields['reddit'].label, 'Reddit')
        self.assertEqual(form.fields['spotify'].label, 'Spotify')
        self.assertEqual(form.fields['twitter'].label, 'Twitter')

    def test_form_with_name_and_sns_field(self):
        form = ProfileForm(data={'name': 'Jerry', 'twitter': 'jerrryy12'})

        self.assertTrue(form.is_valid())

    def test_form_with_no_name(self):
        form = ProfileForm(data={'name': ''})

        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors.keys())
        self.assertEqual(form.errors['name'], ["This field is required."])

    def test_form_with_only_name(self):
        form = ProfileForm(data={'name': 'Jerry'})

        self.assertTrue(form.is_valid())

    def test_name_that_is_too_long(self):
        form = ProfileForm(data={'name': 'Jjjjjjjjjjjjjjjjjjjjjerry'})

        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors.keys())
        self.assertIn('Ensure this value has at most', form.errors['name'][0])

    def test_add_profile_with_duplicate_name(self):
        name = 'Harry'
        profile = Profile.objects.create(name=name)
        form = ProfileForm(data={'name': name})

        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors.keys())
        self.assertEqual(
            form.errors['name'], ['Profile with this Name already exists.']
        )

    def test_forms_fields_match_model_fields(self):
        model_fields = [field for field, _ in Profile().get_fields()]
        for field in model_fields:
            self.assertIn(field, ProfileForm().fields)
