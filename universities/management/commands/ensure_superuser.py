"""
Management command to create a default superuser if none exists.
This is useful for deployment on platforms like Render where you can't access the shell.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os


class Command(BaseCommand):
    help = 'Creates a superuser if none exists (for deployment)'

    def handle(self, *args, **options):
        User = get_user_model()
        
        # Check if any superuser exists
        if User.objects.filter(is_superuser=True).exists():
            self.stdout.write(
                self.style.SUCCESS('✓ Superuser already exists')
            )
            return
        
        # Get credentials from environment variables or use defaults
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@unihub.com')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin123')
        
        try:
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            self.stdout.write(
                self.style.SUCCESS(f'✓ Superuser created: {username}')
            )
            self.stdout.write(
                self.style.WARNING(f'  Username: {username}')
            )
            self.stdout.write(
                self.style.WARNING(f'  Password: {password}')
            )
            self.stdout.write(
                self.style.WARNING('  ⚠️  CHANGE THIS PASSWORD IMMEDIATELY!')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'✗ Failed to create superuser: {e}')
            )
