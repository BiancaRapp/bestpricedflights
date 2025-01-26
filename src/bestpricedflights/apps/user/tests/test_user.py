import factory
from django.test import Client, TestCase

from bestpricedflights.apps.core.tests.factories import CityFactory
from bestpricedflights.apps.user.models import User
from bestpricedflights.apps.user.tests.factories import UserFactory


class UserTestCase(TestCase):
    def test_signup_user(self):
        c = Client()

        signup_url = "/signup/"
        response = c.get(signup_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/signup.html")

        origin = CityFactory(is_origin=True)

        username = "testuser"
        email = "test@example.com"
        password = factory.Faker("password", length=8)
        response = c.post(
            signup_url,
            {
                "username": username,
                "email": email,
                "preferred_origin_city": origin.pk,
                "password1": password,
                "password2": password,
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        user = User.objects.filter(username=username).first()
        self.assertTrue(user)
        self.assertEqual(user.preferred_origin_city, origin)
        self.assertEqual(user.email, email)

        c.login(username=username, password=password)
        self.assertTrue(user.is_authenticated)

    def test_edit_profile(self):
        user = UserFactory()
        c = Client()
        c.force_login(user)
        edit_profile_url = "/profile/"

        response = c.get(edit_profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "profile/update.html")
        self.assertContains(response, user.username)
        self.assertContains(response, user.email)
        self.assertContains(response, user.preferred_origin_city.__str__())

        origin = CityFactory(is_origin=True)
        response = c.post(
            edit_profile_url,
            {
                "username": user.username,
                "email": user.email,
                "preferred_origin_city": origin.pk,
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        updated_user = User.objects.filter(username=user.username).first()
        self.assertTrue(updated_user)
        self.assertEqual(updated_user.preferred_origin_city, origin)
        self.assertEqual(updated_user.email, user.email)
