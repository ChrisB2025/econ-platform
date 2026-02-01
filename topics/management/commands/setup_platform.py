"""
Management command to set up the platform with all initial data.

This command is idempotent - safe to run multiple times.
It handles:
- Database migrations
- Loading schools of thought (via migration)
- Loading inflation topic content
- Creating a superuser if credentials are provided via environment

Usage:
    python manage.py setup_platform
"""
import os
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = 'Set up the platform with initial data (idempotent)'

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING('Setting up Pluralist Economics Platform...'))
        self.stdout.write('')

        # Step 1: Run migrations
        self.stdout.write(self.style.MIGRATE_HEADING('Step 1: Running database migrations...'))
        call_command('migrate', '--noinput', verbosity=1)
        self.stdout.write(self.style.SUCCESS('Migrations complete.'))
        self.stdout.write('')

        # Step 2: Load inflation content
        self.stdout.write(self.style.MIGRATE_HEADING('Step 2: Loading inflation topic content...'))
        call_command('load_inflation_content', verbosity=1)
        self.stdout.write(self.style.SUCCESS('Content loaded.'))
        self.stdout.write('')

        # Step 3: Collect static files
        self.stdout.write(self.style.MIGRATE_HEADING('Step 3: Collecting static files...'))
        call_command('collectstatic', '--noinput', verbosity=1)
        self.stdout.write(self.style.SUCCESS('Static files collected.'))
        self.stdout.write('')

        # Step 4: Create superuser if environment variables are set
        self.create_superuser_if_configured()

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('Platform setup complete!'))

    def create_superuser_if_configured(self):
        """Create superuser from environment variables if not exists."""
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

        if not all([username, email, password]):
            self.stdout.write(
                'Skipping superuser creation (DJANGO_SUPERUSER_* env vars not set)'
            )
            return

        User = get_user_model()

        if User.objects.filter(username=username).exists():
            self.stdout.write(f'Superuser "{username}" already exists.')
            return

        self.stdout.write(self.style.MIGRATE_HEADING('Step 4: Creating superuser...'))
        User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )
        self.stdout.write(self.style.SUCCESS(f'Superuser "{username}" created.'))
