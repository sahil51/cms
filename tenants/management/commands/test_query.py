from django.core.management.base import BaseCommand
from pages.models import ThemeConfig
from django.db import connection

class Command(BaseCommand):
    def handle(self, *args, **options):
        # Check search path
        with connection.cursor() as cursor:
            cursor.execute("SHOW search_path")
            path = cursor.fetchone()
            self.stdout.write(f"Current search path: {path}")

        # Try to query ThemeConfig
        try:
            count = ThemeConfig.objects.count()
            self.stdout.write(f"ThemeConfig count: {count}")
        except Exception as e:
            self.stdout.write(f"ThemeConfig query failed: {str(e)}")
