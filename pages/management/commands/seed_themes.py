import json
from django.core.management.base import BaseCommand
from wagtail.models import Page, Site
from pages.models import (
    ContentPage, SiteSettings, ThemeSettings, Menu, MenuItem
)

class Command(BaseCommand):
    help = 'Seeds all 4 new themes'

    def handle(self, *args, **options):
        site = Site.objects.filter(is_default_site=True).first()
        if not site:
            self.stdout.write('No site.')
            return

        # Clear existing
        Page.objects.filter(depth__gt=1).delete()
        Page.fix_tree()
        root = Page.objects.get(depth=1)

        themes = [
            ('corporate', 'Modern Enterprise Solutions', '#1e40af', 'Corporate Strategy for Growth'),
            ('creative', 'ARTISTIC DISRUPTION', '#d946ef', 'Breaking the Digital Mold'),
            ('saas', 'Automate Your Workflow', '#06b6d4', 'Scalable Productivity Solutions'),
            ('editorial', 'The Silent Observer', '#000000', 'Essays on Modern Life'),
        ]

        for theme_code, title, primary, hero_subtitle in themes:
            self.stdout.write(f'Seeding {theme_code}...')
            
            page = ContentPage(
                title=f"{theme_code.capitalize()} Home",
                slug=theme_code,
                body=json.dumps([
                    {
                        "type": "hero",
                        "value": {
                            "title": title,
                            "subtitle": hero_subtitle,
                            "cta_text": "Explore Now",
                            "cta_link": "#",
                            "badge_text": "FEATURED THEME" if theme_code == 'corporate' else "",
                            "variant": "v1"
                        }
                    }
                ])
            )
            root.add_child(instance=page)
            
            if theme_code == 'corporate':
                # Set default site to corporate theme
                site.root_page = page
                site.save()
                
                ThemeSettings.objects.update_or_create(
                    site=site,
                    defaults={
                        'base_theme': 'corporate',
                        'primary_color': '#1e40af',
                        'heading_font': 'Inter',
                        'body_font': 'Inter',
                    }
                )

        self.stdout.write(self.style.SUCCESS('All themes seeded! Default set to Corporate.'))
