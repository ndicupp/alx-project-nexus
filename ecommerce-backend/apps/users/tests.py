from django.test import TestCase
from django.contrib.auth import get_user_model

class UserTaskTests(TestCase):
    def test_create_user(self):
        """Test that a custom user is created correctly with email."""
        User = get_user_model()
        user = User.objects.create_user(email='test@example.com', password='password123')
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)

    def test_create_superuser(self):
        """Test creating a superuser for admin access."""
        User = get_user_model()
        admin_user = User.objects.create_superuser(email='admin@example.com', password='password123')
        self.assertTrue(admin_user.is_superuser)
        self.assertTrue(admin_user.is_staff)
