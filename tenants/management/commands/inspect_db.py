from django.core.management.base import BaseCommand
from django.db import connection
from django_tenants.utils import schema_context

class Command(BaseCommand):
    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            # Check public schema
            cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' AND table_name LIKE 'pages_%'")
            public_tables = cursor.fetchall()
            self.stdout.write(f"Public tables: {public_tables}")

            # Check sample schema
            with schema_context('sample'):
                cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'sample' AND table_name LIKE 'pages_%'")
                sample_tables = cursor.fetchall()
                self.stdout.write(f"Sample tables: {sample_tables}")
