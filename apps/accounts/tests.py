"""
Tests for the accounts app.
"""
from django.test import TestCase, override_settings
from django.contrib.auth import get_user_model
from apps.accounts.forms import CaptchaSignupForm, CustomLoginForm

User = get_user_model()


class UserModelTests(TestCase):
    """Tests for the custom User model."""

    def test_create_user(self):
        """Test creating a user with email and password."""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.username, 'testuser')
        self.assertTrue(user.check_password('testpass123'))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        """Test creating a superuser."""
        admin = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass123'
        )
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)

    def test_user_uuid_primary_key(self):
        """Test that User model uses UUID primary key."""
        import uuid
        user = User.objects.create_user(
            username='uuidtest',
            email='uuid@example.com',
            password='testpass123'
        )
        self.assertIsInstance(user.id, uuid.UUID)

    def test_user_str_returns_email(self):
        """Test User string representation."""
        user = User.objects.create_user(
            username='strtest',
            email='str@example.com',
            password='testpass123'
        )
        self.assertEqual(str(user), 'str@example.com')

    def test_user_timestamps(self):
        """Test that User has created_at and updated_at fields."""
        user = User.objects.create_user(
            username='timestamps',
            email='timestamps@example.com',
            password='testpass123'
        )
        self.assertIsNotNone(user.created_at)
        self.assertIsNotNone(user.updated_at)

    def test_has_active_subscription_returns_false_by_default(self):
        """Test has_active_subscription returns False for users without subscriptions."""
        user = User.objects.create_user(
            username='nosub',
            email='nosub@example.com',
            password='testpass123'
        )
        self.assertFalse(user.has_active_subscription())

    def test_has_ever_had_subscription_returns_false_by_default(self):
        """Test has_ever_had_subscription returns False for new users."""
        user = User.objects.create_user(
            username='neversub',
            email='neversub@example.com',
            password='testpass123'
        )
        self.assertFalse(user.has_ever_had_subscription())


class CustomLoginFormTests(TestCase):
    """Tests for the custom login form."""

    def test_login_form_fields(self):
        """Test that login form has expected fields."""
        form = CustomLoginForm()
        self.assertIn('login', form.fields)
        self.assertIn('password', form.fields)

    def test_login_form_has_custom_error_messages(self):
        """Test that login form has custom error messages defined."""
        form = CustomLoginForm()
        self.assertIn('email_password_mismatch', form.error_messages)
        self.assertIn('account_inactive', form.error_messages)


@override_settings(DISABLE_RECAPTCHA=True)
class CaptchaSignupFormTests(TestCase):
    """Tests for the signup form with captcha."""

    def test_signup_form_fields(self):
        """Test that signup form has expected fields."""
        form = CaptchaSignupForm()
        self.assertIn('email', form.fields)
        self.assertIn('password1', form.fields)
        self.assertIn('password2', form.fields)
