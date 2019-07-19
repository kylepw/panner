from django.test import TestCase
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch

from sns.forms import ProfileForm
from sns.models import Profile


class ProfileListViewWithDataTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create 25 profiles for pagination tests
        number_of_profiles = 25

        for profile_id in range(number_of_profiles):
            Profile.objects.create(name=f'Profile {profile_id}')

        cls.first_page = reverse('profile-list')
        cls.second_page = reverse('profile-list') + '?page=2'

    def test_view_urls_exists_at_desired_location(self):
        self.assertEqual(self.first_page, '/profiles/')
        self.assertEqual(self.second_page, '/profiles/?page=2')

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

    def test_no_profiles_msg_not_displayed(self):
        response = self.client.get(self.first_page)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'No profiles to display')

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


class ProfileListViewWithoutDataTests(TestCase):
    def setUp(self):
        self.response = self.client.get(reverse('profile-list'))

    def test_message_displayed_when_no_profile_data(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertContains(self.response, 'No profiles to display.')

    def test_uses_correct_template(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'sns/profile_list.html')

    def test_no_profiles_passed_in_context(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTrue('profiles' in self.response.context)
        self.assertEqual(len(self.response.context['profiles']), 0)


class ActivityView(TestCase):
    def setUp(self):

        self.profile = Profile.objects.create(
            name='Harry', reddit='Gallowboob', twitter='katyperry'
        )
        # Prevent Meetup OAuth redirect.
        session = self.client.session
        session['meetup_token'] = 'TOKEN'
        session.save()

    def test_view_url_exists_at_desired_location(self):
        pk = self.profile.pk
        self.assertEqual(reverse('activity', kwargs={'pk': pk}), f'/profile/{pk}/')

    def test_does_not_render_page_without_pk_value_passed(self):
        with self.assertRaises(NoReverseMatch):
            self.client.get(reverse('activity'))

    def test_view_renders_an_existing_profile(self):
        pk = self.profile.pk
        response = self.client.get(reverse('activity', kwargs={'pk': pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('profile' in response.context)
        self.assertEqual(response.context['profile'], self.profile)

    def test_view_uses_correct_template(self):
        pk = self.profile.pk
        response = self.client.get(reverse('activity', kwargs={'pk': pk}))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sns/activity.html')

    def test_does_not_render_nonexisting_profile(self):
        response = self.client.get(reverse('activity', kwargs={'pk': 100000}))
        self.assertEqual(response.status_code, 404)


class ProfileNewTests(TestCase):
    def setUp(self):
        # Prevent Meetup OAuth redirect.
        session = self.client.session
        session['meetup_token'] = 'TOKEN'
        session.save()

    def post_profile(self, data=None):
        if data is None:
            return self.client.post(reverse('profile_new'))

        return self.client.post(reverse('profile_new'), data)

    def test_view_url_exists_at_desired_location(self):
        self.assertEqual(reverse('profile_new'), '/profile/new/')

    def test_uses_correct_template(self):
        response = self.client.get(reverse('profile_new'))

        self.assertTrue(response.status_code, 200)
        self.assertTemplateUsed(response, 'sns/profile_edit.html')

    def test_post_form_with_name_and_sns_handle(self):
        data = {'name': 'Harry', 'twitter': 'katyperry'}
        response = self.post_profile(data)

        self.assertEqual(response.status_code, 302)
        pk = Profile.objects.get(name=data['name']).pk
        self.assertRedirects(response, reverse('activity', kwargs={'pk': pk}))

    def test_post_form_with_only_name(self):
        name = 'Harry'
        response = self.post_profile({'name': name})

        self.assertEqual(response.status_code, 302)
        pk = Profile.objects.get(name=name).pk
        self.assertRedirects(response, reverse('activity', kwargs={'pk': pk}))

    def test_post_form_with_only_twitter_handle(self):
        response = self.post_profile({'twitter': 'katyperry'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sns/profile_edit.html')
        self.assertContains(response, 'This field is required.')

    def test_post_form_without_values(self):
        response = self.post_profile()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sns/profile_edit.html')
        self.assertContains(response, 'This field is required.')


class ProfileEditTests(TestCase):
    def setUp(self):

        self.profile = Profile.objects.create(
            name='Harry', reddit='Gallowboob', twitter='katyperry'
        )
        # Prevent Meetup OAuth redirect.
        session = self.client.session
        session['meetup_token'] = 'TOKEN'
        session.save()

    def get_profile(self, pk=None):
        if pk is None:
            return self.client.get(reverse('profile_edit'))
        return self.client.get(reverse('profile_edit', kwargs={'pk': pk}))

    def post_profile(self, pk, data=None):
        if data is None:
            return self.client.post(reverse('profile_edit', kwargs={'pk': pk}))
        return self.client.post(reverse('profile_edit', kwargs={'pk': pk}), data)

    def test_view_url_exists_at_desired_location(self):
        pk = self.profile.pk
        self.assertEqual(
            reverse('profile_edit', kwargs={'pk': pk}), f'/profile/{pk}/edit/'
        )

    def test_does_not_render_page_without_pk_value_passed(self):
        with self.assertRaises(NoReverseMatch):
            self.get_profile()

    def test_uses_correct_template(self):
        pk = self.profile.pk
        response = self.get_profile(pk)

        self.assertTrue(response.status_code, 200)
        self.assertTemplateUsed(response, 'sns/profile_edit.html')

    def test_get_profile_that_does_not_exist(self):
        response = self.get_profile(pk=1000)
        self.assertEqual(response.status_code, 404)

    def test_edit_profile_with_just_name(self):
        pk = self.profile.pk
        new_data = {'name': 'Harris'}
        response = self.post_profile(pk, new_data)

        self.assertTrue(response, 200)
        self.assertRedirects(response, reverse('activity', kwargs={'pk': pk}))
        self.assertEqual(Profile.objects.get(pk=pk).name, new_data['name'])

    def test_get_profile_without_name(self):
        pk = self.profile.pk
        response = self.post_profile(pk)

        self.assertTrue(response, 200)
        self.assertTemplateUsed(response, 'sns/profile_edit.html')
        self.assertContains(response, 'This field is required.')


class ProfileDeleteTests(TestCase):
    def setUp(self):

        self.profile = Profile.objects.create(
            name='Harry', reddit='Gallowboob', twitter='katyperry'
        )

    def del_profile(self, pk=None):
        if pk is None:
            return self.client.get(reverse('profile_delete'))
        return self.client.get(reverse('profile_delete', kwargs={'pk': pk}))

    def test_view_url_exists_at_desired_location(self):
        pk = self.profile.pk
        self.assertEqual(
            reverse('profile_delete', kwargs={'pk': pk}), f'/profile/{pk}/del/'
        )

    def test_does_not_render_page_without_pk_value_passed(self):
        with self.assertRaises(NoReverseMatch):
            self.del_profile()

    def test_redirects_to_correct_template(self):
        pk = self.profile.pk
        response = self.del_profile(pk)

        self.assertTrue(response.status_code, 200)
        self.assertRedirects(response, reverse('profile-list'))

    def test_get_profile_that_does_not_exist(self):
        response = self.del_profile(pk=1000)
        self.assertEqual(response.status_code, 404)

    def test_instance_is_properly_deleted(self):
        pk = self.profile.pk
        self.assertTrue(Profile.objects.filter(pk=pk).exists())
        response = self.del_profile(pk)
        self.assertTrue(response.status_code, 200)
        self.assertFalse(Profile.objects.filter(pk=pk).exists())
