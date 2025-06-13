from http import HTTPStatus

from django.test import TestCase

from ..factories import user_factories

# Note: These tests are mainly an example on how to use factories
#       and the Django test client. Use them as a reference and write
#       exhaustive tests to ensure the application is working as expected.


class TestDjangoAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = user_factories.UserFactory()
        cls.superuser = user_factories.SuperUserFactory()

    def test_django_admin_as_user(self):
        """
        User gets redirected to OTP setup screen
        """
        self.client.force_login(self.user)
        response = self.client.get("/django-admin/")
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(
            response,
            "/manage/otp/setup/?next=/django-admin/",
            fetch_redirect_response=False,
        )

    def test_django_admin_as_superuser(self):
        """
        Superuser gets redirected to OTP setup screen
        """
        self.client.force_login(self.superuser)
        response = self.client.get("/django-admin/")
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(
            response,
            "/manage/otp/setup/?next=/django-admin/",
            fetch_redirect_response=False,
        )
