import json
from django.core.management.base import BaseCommand
from wagtail.models import Page, Site
from pages.models import (
    ContentPage, ServicePage, BlogIndexPage, BlogPostPage,
    ServiceAreaIndexPage, ServiceAreaPage, ContactPage,
    SiteSettings, ThemeSettings, Menu, MenuItem, FormField
)

class Command(BaseCommand):
    help = 'Seeds a Corporate demo website'

    def handle(self, *args, **options):
        self.stdout.write('[Corporate Site] Seeding...')

        site = Site.objects.filter(is_default_site=True).first()
        if not site:
            self.stdout.write(self.style.ERROR('No default site found.'))
            return
            
        config, _ = ThemeSettings.objects.update_or_create(
            site=site,
            defaults={
                'base_theme': 'corporate',
                'primary_color': '#1e40af',  # Strong Blue
                'secondary_color': '#f59e0b', # Amber
                'background_color': '#ffffff',
                'text_color': '#111827',
                'heading_font': 'Inter',
                'body_font': 'Inter',
            }
        )

        Page.objects.filter(depth__gt=1).delete()
        Page.fix_tree()
        root_page = Page.objects.filter(depth=1).first()

        home = ContentPage(
            title="Professional Solutions for Your Business",
            slug="home",
            body=json.dumps([
                {
                    "type": "hero",
                    "value": {
                        "title": "Empowering Corporate Excellence",
                        "subtitle": "We provide strategic consulting and innovative solutions to help your business thrive in a competitive market.",
                        "badge_text": "Industry Leader",
                        "cta_text": "Our Services",
                        "cta_link": "#services",
                        "overlay": True,
                        "variant": "v1"
                    }
                },
                {
                    "type": "about",
                    "value": {
                        "section_tag": "Who We Are",
                        "title": "Decades of Strategic Success",
                        "content": "<p>Our mission is to bridge the gap between business challenges and scalable solutions. We work with Fortune 500 companies to streamline operations and drive growth.</p>",
                        "variant": "v1"
                    }
                },
                {
                    "type": "services",
                    "value": {
                        "title": "Our Core Expertise",
                        "subtitle": "Tailored strategies designed for modern enterprises.",
                        "services": [
                            {"icon": "fa-chart-pie", "name": "Market Analysis", "description": "In-depth research and data-driven insights into your industry.", "cta_text": "Learn More", "link": "#"},
                            {"icon": "fa-handshake", "name": "Strategic Planning", "description": "Long-term roadmaps for sustainable business development.", "cta_text": "Learn More", "link": "#"},
                            {"icon": "fa-gears", "name": "Operational Audit", "description": "Identifying inefficiencies and optimizing your internal processes.", "cta_text": "Learn More", "link": "#"}
                        ],
                        "variant": "v1"
                    }
                }
            ])
        )
        root_page.add_child(instance=home)
        site.root_page = home
        site.save()

        # Navigation
        menu, _ = Menu.objects.get_or_create(slug="main", defaults={"title": "Main Navigation"})
        menu.menu_items.all().delete()
        MenuItem.objects.create(menu=menu, link_title="Home", link_url="/", sort_order=0)

        self.stdout.write(self.style.SUCCESS('Done!'))
