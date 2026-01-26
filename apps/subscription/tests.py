"""
Tests for the subscription app.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.subscription.models import Customer, Subscription
from apps.subscription.enums import PlanType, SubscriptionStatus

User = get_user_model()


class PlanTypeEnumTests(TestCase):
    """Tests for the PlanType enum."""

    def test_plan_type_values(self):
        """Test PlanType enum has expected values."""
        self.assertEqual(PlanType.FREE, 'free')
        self.assertEqual(PlanType.PLUS, 'plus')

    def test_plan_type_choices(self):
        """Test PlanType provides choices for model fields."""
        choices = PlanType.choices
        self.assertIn(('free', 'Free'), choices)
        self.assertIn(('plus', 'Plus'), choices)


class SubscriptionStatusEnumTests(TestCase):
    """Tests for the SubscriptionStatus enum."""

    def test_subscription_status_values(self):
        """Test SubscriptionStatus enum has expected values."""
        self.assertEqual(SubscriptionStatus.ACTIVE, 'active')
        self.assertEqual(SubscriptionStatus.CANCELED, 'canceled')
        self.assertEqual(SubscriptionStatus.PAST_DUE, 'past_due')
        self.assertEqual(SubscriptionStatus.TRIALING, 'trialing')

    def test_subscription_status_choices(self):
        """Test SubscriptionStatus provides choices."""
        choices = SubscriptionStatus.choices
        self.assertIn(('active', 'Active'), choices)
        self.assertIn(('canceled', 'Canceled'), choices)


class CustomerModelTests(TestCase):
    """Tests for the Customer model."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='custtest',
            email='customer@example.com',
            password='testpass123'
        )

    def test_create_customer(self):
        """Test creating a customer."""
        customer = Customer.objects.create(
            user=self.user,
            stripe_customer_id='cus_test123'
        )
        self.assertEqual(customer.user, self.user)
        self.assertEqual(customer.stripe_customer_id, 'cus_test123')

    def test_customer_uuid_primary_key(self):
        """Test Customer uses UUID primary key."""
        import uuid
        customer = Customer.objects.create(
            user=self.user,
            stripe_customer_id='cus_uuid123'
        )
        self.assertIsInstance(customer.id, uuid.UUID)

    def test_customer_str(self):
        """Test Customer string representation."""
        customer = Customer.objects.create(
            user=self.user,
            stripe_customer_id='cus_str123'
        )
        str_repr = str(customer)
        self.assertIn('customer@example.com', str_repr)

    def test_customer_timestamps(self):
        """Test Customer has timestamps."""
        customer = Customer.objects.create(
            user=self.user,
            stripe_customer_id='cus_time123'
        )
        self.assertIsNotNone(customer.created_at)
        self.assertIsNotNone(customer.updated_at)


class SubscriptionModelTests(TestCase):
    """Tests for the Subscription model."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='subuser',
            email='subscription@example.com',
            password='testpass123'
        )
        self.customer = Customer.objects.create(
            user=self.user,
            stripe_customer_id='cus_sub123'
        )

    def test_create_subscription(self):
        """Test creating a subscription."""
        subscription = Subscription.objects.create(
            customer=self.customer,
            stripe_subscription_id='sub_test123',
            plan=PlanType.PLUS,
            status=SubscriptionStatus.ACTIVE
        )
        self.assertEqual(subscription.customer, self.customer)
        self.assertEqual(subscription.plan, PlanType.PLUS)
        self.assertEqual(subscription.status, SubscriptionStatus.ACTIVE)

    def test_subscription_is_active_property(self):
        """Test is_active property returns True for active subscriptions."""
        subscription = Subscription.objects.create(
            customer=self.customer,
            stripe_subscription_id='sub_active123',
            plan=PlanType.PLUS,
            status=SubscriptionStatus.ACTIVE
        )
        self.assertTrue(subscription.is_active)

    def test_subscription_is_active_false_for_canceled(self):
        """Test is_active returns False for canceled subscriptions."""
        subscription = Subscription.objects.create(
            customer=self.customer,
            stripe_subscription_id='sub_canceled123',
            plan=PlanType.PLUS,
            status=SubscriptionStatus.CANCELED
        )
        self.assertFalse(subscription.is_active)

    def test_subscription_uuid_primary_key(self):
        """Test Subscription uses UUID primary key."""
        import uuid
        subscription = Subscription.objects.create(
            customer=self.customer,
            stripe_subscription_id='sub_uuid123',
            plan=PlanType.FREE,
            status=SubscriptionStatus.ACTIVE
        )
        self.assertIsInstance(subscription.id, uuid.UUID)


class SubscriptionUtilsTests(TestCase):
    """Tests for subscription utility functions."""

    def test_utils_imports(self):
        """Test subscription utils can be imported."""
        from apps.subscription.utils import (
            sync_subscription_status_and_plan,
            get_plan_type,
            is_subscription_not_active
        )
        self.assertIsNotNone(sync_subscription_status_and_plan)
        self.assertIsNotNone(get_plan_type)
        self.assertIsNotNone(is_subscription_not_active)
