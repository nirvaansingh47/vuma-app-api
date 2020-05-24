from django.test import TestCase
from django.contrib.auth import get_user_model
from core.models import VumaRequest


def sample_user(email='test@gmail.com', password="testpassword"):
    """Create a sample user"""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        email = "test@gmail.com"
        password = "Test1234"
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalised(self):
        """Test the email for a new user is normalized"""
        email = "test@GREAT.COM"
        user = get_user_model().objects.create_user(
            email,
            password="test123"
        )

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, "Test123")

    def test_create_new_super_user(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            "superuser@test.com",
            "test123"
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_vuma_requests_str(self):
        """Test string representaiton of model"""
        request = VumaRequest.objects.create(
            name="Test request",
            method="GET",
            url="https://www.google.com",
            user=sample_user()
        )

        self.assertEqual(str(request), request.name)
