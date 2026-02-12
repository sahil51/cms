from django.core.management.base import BaseCommand
from tenants.models import Tenant, Domain

class Command(BaseCommand):
    help = 'Initialize the SaaS Website Builder with public and first sample tenant'

    def handle(self, *args, **options):
        # Create Public Tenant (Shared data, login, signup, etc.)
        tenant, created = Tenant.objects.get_or_create(
            schema_name='public',
            defaults={'name': 'Public Host'}
        )
        Domain.objects.get_or_create(
            domain='localhost', 
            tenant=tenant,
            defaults={'is_primary': True}
        )
        Domain.objects.get_or_create(
            domain='127.0.0.1', 
            tenant=tenant,
            defaults={'is_primary': False}
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f"Created public tenant 'public'"))

        # Create Sample Tenant (Isolated customer data)
        sample_tenant, created = Tenant.objects.get_or_create(
            schema_name='sample',
            defaults={'name': 'Sample Customer'}
        )
        Domain.objects.get_or_create(
            domain='sample.localhost',
            tenant=sample_tenant,
            defaults={'is_primary': True}
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f"Created sample tenant 'sample' at sample.localhost"))
        
        self.stdout.write(self.style.SUCCESS("SaaS system initialization complete."))
