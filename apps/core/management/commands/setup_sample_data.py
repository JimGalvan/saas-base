"""
Management command to create sample data for development.

This command creates sample users, subscriptions, and other data
to help developers get started quickly with a populated database.

Usage:
    python manage.py setup_sample_data
    python manage.py setup_sample_data --clear  # Clear existing sample data first
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.subscription.models import Customer, Subscription
from apps.subscription.enums import PlanType, SubscriptionStatus
from apps.maintenance.models import MaintenanceMode
from apps.webhooks.models import WebhookEvent

User = get_user_model()


class Command(BaseCommand):
    help = 'Create sample data for development and testing'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing sample data before creating new data',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.clear_sample_data()

        self.stdout.write(self.style.NOTICE('Creating sample data...'))

        # Create sample users
        users = self.create_sample_users()

        # Create sample subscriptions
        self.create_sample_subscriptions(users)

        # Initialize maintenance mode
        self.initialize_maintenance_mode()

        # Create sample webhook events
        self.create_sample_webhooks()

        self.stdout.write(self.style.SUCCESS('Sample data created successfully!'))
        self.print_summary()

    def clear_sample_data(self):
        """Remove previously created sample data."""
        self.stdout.write(self.style.WARNING('Clearing existing sample data...'))

        # Delete sample users (cascades to subscriptions)
        sample_emails = [
            'demo@example.com',
            'free@example.com',
            'premium@example.com',
            'admin@example.com',
        ]
        User.objects.filter(email__in=sample_emails).delete()

        # Clear sample webhooks
        WebhookEvent.objects.filter(event_id__startswith='evt_sample_').delete()

        self.stdout.write(self.style.SUCCESS('Sample data cleared.'))

    def create_sample_users(self):
        """Create sample user accounts."""
        self.stdout.write('  Creating sample users...')

        users = {}

        # Admin user
        admin, created = User.objects.get_or_create(
            email='admin@example.com',
            defaults={
                'username': 'admin',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if created:
            admin.set_password('admin123')
            admin.save()
            self.stdout.write(f'    Created admin user: admin@example.com')
        users['admin'] = admin

        # Demo user (with subscription)
        demo, created = User.objects.get_or_create(
            email='demo@example.com',
            defaults={
                'username': 'demo',
                'first_name': 'Demo',
                'last_name': 'User',
            }
        )
        if created:
            demo.set_password('demo123')
            demo.save()
            self.stdout.write(f'    Created demo user: demo@example.com')
        users['demo'] = demo

        # Free tier user
        free, created = User.objects.get_or_create(
            email='free@example.com',
            defaults={
                'username': 'freeuser',
                'first_name': 'Free',
                'last_name': 'User',
            }
        )
        if created:
            free.set_password('free123')
            free.save()
            self.stdout.write(f'    Created free user: free@example.com')
        users['free'] = free

        # Premium user
        premium, created = User.objects.get_or_create(
            email='premium@example.com',
            defaults={
                'username': 'premiumuser',
                'first_name': 'Premium',
                'last_name': 'User',
            }
        )
        if created:
            premium.set_password('premium123')
            premium.save()
            self.stdout.write(f'    Created premium user: premium@example.com')
        users['premium'] = premium

        return users

    def create_sample_subscriptions(self, users):
        """Create sample subscriptions for users."""
        self.stdout.write('  Creating sample subscriptions...')

        # Demo user - active subscription
        demo_customer, _ = Customer.objects.get_or_create(
            user=users['demo'],
            defaults={'stripe_customer_id': 'cus_sample_demo'}
        )
        Subscription.objects.get_or_create(
            customer=demo_customer,
            defaults={
                'stripe_subscription_id': 'sub_sample_demo',
                'plan': PlanType.PLUS,
                'status': SubscriptionStatus.ACTIVE,
            }
        )
        self.stdout.write(f'    Created PLUS subscription for demo user')

        # Free user - free tier
        free_customer, _ = Customer.objects.get_or_create(
            user=users['free'],
            defaults={'stripe_customer_id': 'cus_sample_free'}
        )
        Subscription.objects.get_or_create(
            customer=free_customer,
            defaults={
                'stripe_subscription_id': 'sub_sample_free',
                'plan': PlanType.FREE,
                'status': SubscriptionStatus.ACTIVE,
            }
        )
        self.stdout.write(f'    Created FREE subscription for free user')

        # Premium user - active subscription
        premium_customer, _ = Customer.objects.get_or_create(
            user=users['premium'],
            defaults={'stripe_customer_id': 'cus_sample_premium'}
        )
        Subscription.objects.get_or_create(
            customer=premium_customer,
            defaults={
                'stripe_subscription_id': 'sub_sample_premium',
                'plan': PlanType.PLUS,
                'status': SubscriptionStatus.ACTIVE,
            }
        )
        self.stdout.write(f'    Created PLUS subscription for premium user')

    def initialize_maintenance_mode(self):
        """Ensure maintenance mode is initialized."""
        self.stdout.write('  Initializing maintenance mode...')
        try:
            instance = MaintenanceMode.get_instance()
            self.stdout.write(f'    Maintenance mode: {"ACTIVE" if instance.is_active else "INACTIVE"}')
        except Exception as e:
            # Handle case where Redis is not available
            self.stdout.write(self.style.WARNING(f'    Skipped (cache unavailable): {str(e)[:50]}'))

    def create_sample_webhooks(self):
        """Create sample webhook events for testing."""
        self.stdout.write('  Creating sample webhook events...')

        sample_events = [
            {
                'event_id': 'evt_sample_subscription_created',
                'provider': 'stripe',
                'payload': {
                    'type': 'customer.subscription.created',
                    'data': {'object': {'id': 'sub_sample'}}
                },
            },
            {
                'event_id': 'evt_sample_payment_succeeded',
                'provider': 'stripe',
                'payload': {
                    'type': 'invoice.payment_succeeded',
                    'data': {'object': {'id': 'in_sample'}}
                },
            },
        ]

        for event_data in sample_events:
            WebhookEvent.objects.get_or_create(
                event_id=event_data['event_id'],
                provider=event_data['provider'],
                defaults={'payload': event_data['payload']}
            )

        self.stdout.write(f'    Created {len(sample_events)} sample webhook events')

    def print_summary(self):
        """Print a summary of the created data."""
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('=' * 50))
        self.stdout.write(self.style.SUCCESS('Sample Data Summary'))
        self.stdout.write(self.style.SUCCESS('=' * 50))
        self.stdout.write('')
        self.stdout.write('Sample User Accounts:')
        self.stdout.write('  Admin:   admin@example.com / admin123')
        self.stdout.write('  Demo:    demo@example.com / demo123 (PLUS subscription)')
        self.stdout.write('  Free:    free@example.com / free123 (FREE subscription)')
        self.stdout.write('  Premium: premium@example.com / premium123 (PLUS subscription)')
        self.stdout.write('')
        self.stdout.write('To access the admin panel:')
        self.stdout.write('  1. Run: python manage.py runserver')
        self.stdout.write('  2. Visit: http://localhost:8000/admin/')
        self.stdout.write('  3. Login with admin@example.com / admin123')
        self.stdout.write('')
