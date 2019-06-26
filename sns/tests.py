from django.db.utils import DataError, IntegrityError
from django.test import TestCase
from django.urls import reverse

from .forms import ProfileForm
from .models import Profile


class ProfileListViewTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create 25 profiles for pagination tests
        number_of_profiles = 25

        for profile_id in range(number_of_profiles):
            Profile.objects.create(name=f'Profile {profile_id}')

        cls.first_page = reverse('profile-list')
        cls.second_page = reverse('profile-list') + '?page=2'

    def test_view_urls_exists_at_desired_location(self):
        self.assertEqual(self.first_page, '/')
        self.assertEqual(self.second_page, '/?page=2')

    def test_view_url_accessible_by_name(self):
        response = self.client.get(self.first_page)
        self.assertEqual(response.status_code, 200)

    def test_uses_correct_template(self):
        response = self.client.get(self.first_page)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sns/profile_list.html')

    def test_pagination_is_twenty(self):
        response = self.client.get(self.first_page)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'])
        self.assertTrue(len(response.context['profiles']) == 20)

    def test_lists_all_profiles(self):
        # Second page should show last five profiles
        response = self.client.get(self.second_page)
        self.assertEqual(response.status_code, 200)

        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'])
        self.assertTrue(len(response.context['profiles']) == 5)

    def test_added_profile_name_appears_on_second_page(self):
        name = 'Harry'

        response = self.client.get(self.second_page)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, name)

        Profile.objects.create(name=name)

        response = self.client.get(self.second_page)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, name)

    def test_displays_new_profile_name_after_name_change(self):
        old_name = 'Harry'
        new_name = 'Harris'

        profile = Profile.objects.create(name=old_name)

        response = self.client.get(self.second_page)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, old_name)
        self.assertNotContains(response, new_name)

        profile.name = new_name
        profile.save()

        response = self.client.get(self.second_page)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, old_name)
        self.assertContains(response, new_name)

    def test_name_of_removed_profile_disappears_from_page(self):
        name = 'Harry'
        Profile.objects.create(name=name)

        response = self.client.get(self.second_page)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, name)

        Profile.objects.filter(name=name).delete()

        response = self.client.get(self.second_page)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, name)


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

    def test_facebook_label(self):
        name_label = self.a._meta.get_field('facebook').verbose_name
        self.assertEqual(name_label, 'facebook')

    def test_instagram_label(self):
        name_label = self.a._meta.get_field('instagram').verbose_name
        self.assertEqual(name_label, 'instagram')

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

    def test_facebook_max_length(self):
        max_length = self.a._meta.get_field('facebook').max_length

        self.assertEqual(max_length, 50)

    def test_instagram_max_length(self):
        max_length = self.a._meta.get_field('instagram').max_length

        self.assertEqual(max_length, 30)

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


class ProfileFormTests(TestCase):

    def test_form_labels(self):
        form = ProfileForm()

        self.assertEqual(form.fields['name'].label, 'Name')
        self.assertEqual(form.fields['facebook'].label, 'Facebook')
        self.assertEqual(form.fields['instagram'].label, 'Instagram')
        self.assertEqual(form.fields['reddit'].label, 'Reddit')
        self.assertEqual(form.fields['spotify'].label, 'Spotify')
        self.assertEqual(form.fields['twitter'].label, 'Twitter')

    def test_form_with_name_and_sns_field(self):
        form = ProfileForm(data={'name': 'Jerry', 'facebook': 'fb@fb.com'})

        self.assertTrue(form.is_valid())

    def test_form_with_no_name(self):
        form = ProfileForm(data={'name': ''})

        self.assertFalse(form.is_valid())

    def test_form_with_only_name(self):
        form = ProfileForm(data={'name': 'Jerry'})

        self.assertTrue(form.is_valid())

    def test_name_that_is_too_long(self):
        form = ProfileForm(data={'name': 'Jjjjjjjjjjjjjjjjjjjjjerry'})

        self.assertFalse(form.is_valid())
