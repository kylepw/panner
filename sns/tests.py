from django.db.utils import DataError, IntegrityError
from django.test import TestCase
from django.urls import reverse

from .forms import ProfileForm
from .models import Profile


class ProfileListViewTests(TestCase):
    def setUp(self):
        self.a = Profile.objects.create(name='Jerry', twitter='jerryyy318')
        self.response = self.client.get(reverse('profile-list'))

    def test_added_profile_name_appears_on_page(self):
        b_name = 'Kylie'

        self.assertContains(self.response, self.a.name)
        self.assertNotContains(self.response, b_name)

        Profile.objects.create(name=b_name)
        self.response = self.client.get(reverse('profile-list'))

        self.assertContains(self.response, self.a.name)
        self.assertContains(self.response, b_name)

    def test_displays_new_profile_name_after_name_change(self):
        old_name = self.a.name
        new_name = 'Harry'

        self.assertContains(self.response, old_name)

        self.a.name = new_name
        self.a.save()

        self.response = self.client.get(reverse('profile-list'))
        self.assertContains(self.response, new_name)
        self.assertNotContains(self.response, old_name)

    def test_name_of_removed_profile_disappears_from_page(self):
        a_name = self.a.name

        self.assertContains(self.response, a_name)
        self.a.delete()
        self.response = self.client.get(reverse('profile-list'))
        self.assertNotContains(self.response, a_name)


class ProfileModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.FIELDS = {
            'facebook': 'jerry@gmail.com',
            'reddit': 'jjjjerry',
            'twitter': 'jerryinthewild318',
        }

        cls.a = Profile.objects.create(
            name='Jerry',
            facebook=cls.FIELDS['facebook'],
            reddit=cls.FIELDS['reddit'],
            twitter=cls.FIELDS['twitter'],
        )

    def test_name_label(self):
        name_label = self.a._meta.get_field('name').verbose_name
        self.assertEqual(name_label, 'name')

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

    def test_facebook_max_length(self):
        max_length = self.a._meta.get_field('facebook').max_length

        self.assertEqual(max_length, 50)

    def test_name_that_is_too_long(self):
        with self.assertRaisesMessage(DataError, 'value too long'):
            Profile.objects.create(name='Jjjjjjjjjjjjjjjjjjjjjerry')


class ProfileFormTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass

    def test_form_with_no_name(self):
        form = ProfileForm(data={'name': ''})

        self.assertFalse(form.is_valid())

    def test_form_with_only_name(self):
        form = ProfileForm(data={'name': 'Jerry'})

        self.assertTrue(form.is_valid())

    def test_form_with_name_and_sns_field(self):
        data = {'name': 'Jerry', 'facebook': 'fb@fb.com'}
        form = ProfileForm(data=data)

        self.assertTrue(form.is_valid())

    def test_name_that_is_too_long(self):
        form = ProfileForm(data={'name': 'Jjjjjjjjjjjjjjjjjjjjjerry'})

        self.assertFalse(form.is_valid())
