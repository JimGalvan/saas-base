"""
Django management command for controlling maintenance mode.

This command allows administrators to enable/disable maintenance mode
and customize the maintenance message from the command line.

Usage:
    python manage.py maintenance_mode --status
    python manage.py maintenance_mode --enable
    python manage.py maintenance_mode --disable
    python manage.py maintenance_mode --message "Custom message"
    python manage.py maintenance_mode --enable --message "Under maintenance"
"""
from django.core.management.base import BaseCommand, CommandError
from apps.maintenance.models import MaintenanceMode


class Command(BaseCommand):
    """
    Management command to control maintenance mode.

    This command provides a CLI interface to enable/disable maintenance mode,
    check its status, and customize the maintenance message.
    """
    help = 'Enable, disable or check the status of maintenance mode'

    def add_arguments(self, parser):
        """
        Define command line arguments.

        Args:
            parser: The argument parser
        """
        # Named (optional) arguments
        parser.add_argument(
            '--enable',
            action='store_true',
            help='Enable maintenance mode',
        )

        parser.add_argument(
            '--disable',
            action='store_true',
            help='Disable maintenance mode',
        )

        parser.add_argument(
            '--message',
            type=str,
            help='Customize the maintenance mode message',
        )

        parser.add_argument(
            '--status',
            action='store_true',
            help='Check the current status of maintenance mode',
        )

    def handle(self, *args, **options):
        """
        Execute the command.

        Args:
            *args: Positional arguments
            **options: Named arguments from parser
        """
        maintenance_instance = MaintenanceMode.get_instance()

        # Status check (default if no options provided)
        if options['status'] or (not options['enable'] and not options['disable'] and not options['message']):
            status = "ENABLED" if maintenance_instance.is_active else "DISABLED"
            self.stdout.write(f"Maintenance mode is currently {status}")
            self.stdout.write(f"Message: {maintenance_instance.message}")
            return

        # Update message if provided
        if options['message']:
            maintenance_instance.message = options['message']
            self.stdout.write(self.style.SUCCESS(f"Maintenance message updated to: {options['message']}"))

        # Handle enable/disable
        if options['enable'] and options['disable']:
            raise CommandError("You can't both enable and disable maintenance mode at the same time")

        if options['enable']:
            maintenance_instance.is_active = True
            self.stdout.write(self.style.SUCCESS('Maintenance mode ENABLED'))

        if options['disable']:
            maintenance_instance.is_active = False
            self.stdout.write(self.style.SUCCESS('Maintenance mode DISABLED'))

        # Save changes
        maintenance_instance.save()
