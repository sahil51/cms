"""
Management command to seed a complete Security Services website.
Creates: Home, About, Services (7), Blog (3 posts), Service Areas (3), Contact page.
Uses all 18 block types with realistic content.
"""
import json
from django.core.management.base import BaseCommand
from wagtail.models import Page, Site
from pages.models import (
    ContentPage, ServicePage, BlogIndexPage, BlogPostPage,
    ServiceAreaIndexPage, ServiceAreaPage, ContactPage,
    SiteSettings, ThemeSettings, Menu, MenuItem, FormField
)


class Command(BaseCommand):
    help = 'Seeds a complete Security Services demo website'

    def handle(self, *args, **options):
        self.stdout.write('🔐 Seeding Security Services website...\n')

        # ============================================
        # 1. THEME CONFIG
        # ============================================
        site = Site.objects.filter(is_default_site=True).first()
        config, _ = ThemeSettings.objects.update_or_create(
            site=site,
            defaults={
                'base_theme': 'modern',
                'primary_color': '#00D4FF',
                'secondary_color': '#FF6B35',
                'background_color': '#0A0E17',
                'text_color': '#FFFFFF',
                'heading_font': 'Inter',
                'body_font': 'Inter',
            }
        )
        self.stdout.write(self.style.SUCCESS('  ✓ Theme configured'))

        # ============================================
        # 2. GET ROOT PAGE — clean existing pages
        # ============================================
        # Delete all non-root pages safely for treebeard
        Page.objects.filter(depth__gt=1).delete()
        # Fix the treebeard MP tree after bulk deletion
        Page.fix_tree()
        # Reload root page with fresh tree state
        root_page = Page.objects.filter(depth=1).first()

        # ============================================
        # 3. HOME PAGE
        # ============================================
        home = ContentPage(
            title="Home",
            slug="home",
            body=json.dumps([
                # --- Carousel Hero ---
                {
                    "type": "carousel_hero",
                    "value": {
                        "variant": "v1", "animation": "fade-up", "section_id": "hero", "visible": True,
                        "autoplay": True, "autoplay_speed": 5000, "pause_on_hover": True,
                        "show_arrows": True, "show_dots": True,
                        "animation_type": "fade", "animation_speed": 800,
                        "slides": [
                            {
                                "title": "Protect What Matters Most",
                                "subtitle": "Industry-leading CCTV, alarm systems, and 24/7 monitoring for homes and businesses across the region.",
                                "image": None, "background_video_url": "", "overlay": True,
                                "badge_text": "24/7 Live Monitoring",
                                "cta_text": "Get Free Security Audit",
                                "cta_link": "#contact",
                                "secondary_cta_text": "Call Now",
                                "secondary_cta_link": "tel:+1800555SAFE",
                                "enabled": True
                            },
                            {
                                "title": "Smart CCTV Solutions",
                                "subtitle": "AI-powered surveillance with real-time alerts, night vision, and cloud storage. See everything, anywhere.",
                                "image": None, "background_video_url": "", "overlay": True,
                                "badge_text": "AI-Powered",
                                "cta_text": "Explore CCTV Systems",
                                "cta_link": "#services",
                                "secondary_cta_text": "Free Quote",
                                "secondary_cta_link": "#contact",
                                "enabled": True
                            },
                            {
                                "title": "Commercial Security Systems",
                                "subtitle": "Enterprise-grade access control, intrusion detection, and fire safety systems for businesses of all sizes.",
                                "image": None, "background_video_url": "", "overlay": True,
                                "badge_text": "Enterprise Grade",
                                "cta_text": "Business Solutions",
                                "cta_link": "#services",
                                "secondary_cta_text": "Schedule Consultation",
                                "secondary_cta_link": "#contact",
                                "enabled": True
                            }
                        ]
                    }
                },
                # --- Trust Bar ---
                {
                    "type": "trust_bar",
                    "value": {
                        "variant": "v1", "animation": "fade-up", "section_id": "trusted", "visible": True,
                        "title": "Trusted by 500+ Businesses & Homeowners",
                        "logos": []
                    }
                },
                # --- Services Grid ---
                {
                    "type": "services",
                    "value": {
                        "variant": "v1", "animation": "fade-up", "section_id": "services", "visible": True,
                        "title": "Our Security Services",
                        "subtitle": "Complete security solutions tailored to your needs. From installation to 24/7 monitoring.",
                        "services": [
                            {"icon": "fa-video", "image": None, "name": "CCTV Systems", "description": "HD & 4K surveillance cameras with night vision, motion detection, and remote viewing from your smartphone.", "cta_text": "Learn More", "link": ""},
                            {"icon": "fa-bell", "image": None, "name": "Alarm Systems", "description": "Smart intrusion detection with instant alerts, professional monitoring, and police/fire dispatch integration.", "cta_text": "Learn More", "link": ""},
                            {"icon": "fa-walkie-talkie", "image": None, "name": "Intercom Systems", "description": "Video intercom with remote access, visitor screening, and seamless integration with access control.", "cta_text": "Learn More", "link": ""},
                            {"icon": "fa-key", "image": None, "name": "Access Control", "description": "Keycard, biometric, and mobile-based access systems for offices, warehouses, and residential complexes.", "cta_text": "Learn More", "link": ""},
                            {"icon": "fa-fire", "image": None, "name": "Smoke Detectors", "description": "Intelligent fire detection systems with automated suppression, emergency alerts, and compliance certification.", "cta_text": "Learn More", "link": ""},
                            {"icon": "fa-shield-halved", "image": None, "name": "Site Security", "description": "Physical security assessments, guard patrols, and integrated electronic monitoring for construction sites and events.", "cta_text": "Learn More", "link": ""}
                        ]
                    }
                },
                # --- Why Choose Us ---
                {
                    "type": "why_choose_us",
                    "value": {
                        "variant": "v1", "animation": "fade-up", "section_id": "why-us", "visible": True,
                        "title": "Why Choose SecureGuard Pro?",
                        "subtitle": "With 15+ years of experience, we deliver security solutions that actually work.",
                        "image": None,
                        "cta_text": "Get Started Today",
                        "cta_link": "#contact",
                        "reasons": [
                            {"icon": "fa-clock", "title": "24/7 Live Monitoring", "description": "Our monitoring center never sleeps. Real operators respond to every alarm within 30 seconds."},
                            {"icon": "fa-certificate", "title": "Licensed & Insured", "description": "Fully licensed, bonded, and insured. All technicians are background-checked and certified."},
                            {"icon": "fa-bolt", "title": "Fast Response Time", "description": "Average response time under 8 minutes. We partner with local law enforcement for rapid dispatch."},
                            {"icon": "fa-handshake", "title": "No Lock-In Contracts", "description": "Month-to-month monitoring available. We earn your business every month, not through contracts."},
                            {"icon": "fa-tools", "title": "Free Installation", "description": "Professional installation included with all monitoring plans. No hidden costs or surprise fees."},
                            {"icon": "fa-headset", "title": "Lifetime Support", "description": "Free technical support and system health checks for as long as you're our customer."}
                        ]
                    }
                },
                # --- Industries ---
                {
                    "type": "industries",
                    "value": {
                        "variant": "v1", "animation": "fade-up", "section_id": "industries", "visible": True,
                        "title": "Industries We Protect",
                        "subtitle": "Tailored security solutions for every sector",
                        "industries": [
                            {"icon": "fa-store", "name": "Retail & Shopping", "image": None},
                            {"icon": "fa-building", "name": "Corporate Offices", "image": None},
                            {"icon": "fa-warehouse", "name": "Warehouses", "image": None},
                            {"icon": "fa-school", "name": "Schools & Education", "image": None},
                            {"icon": "fa-hospital", "name": "Healthcare", "image": None},
                            {"icon": "fa-hotel", "name": "Hotels & Hospitality", "image": None}
                        ]
                    }
                },
                # --- Process Steps ---
                {
                    "type": "process_steps",
                    "value": {
                        "variant": "v1", "animation": "fade-up", "section_id": "process", "visible": True,
                        "title": "How It Works",
                        "subtitle": "Getting started is simple — we handle everything from assessment to installation",
                        "steps": [
                            {"icon": "fa-magnifying-glass", "title": "Free Security Audit", "description": "Our experts visit your property to assess vulnerabilities and recommend the ideal security setup."},
                            {"icon": "fa-pencil-ruler", "title": "Custom Design", "description": "We design a tailored security system based on your property layout, risk profile, and budget."},
                            {"icon": "fa-screwdriver-wrench", "title": "Professional Install", "description": "Certified technicians install your system with minimal disruption. Usually completed in one day."},
                            {"icon": "fa-satellite-dish", "title": "24/7 Monitoring", "description": "Your system goes live with round-the-clock monitoring from our state-of-the-art operations center."}
                        ]
                    }
                },
                # --- Testimonials ---
                {
                    "type": "testimonials",
                    "value": {
                        "variant": "v1", "animation": "fade-up", "section_id": "testimonials", "visible": True,
                        "title": "What Our Clients Say",
                        "testimonials": [
                            {"quote": "SecureGuard Pro installed our entire office CCTV system in a single day. The image quality is incredible, and the mobile app lets me check cameras from anywhere. Best investment we've made.", "author": "James Morrison", "role": "CEO, Morrison & Partners", "location": "Downtown", "rating": 5, "image": None},
                            {"quote": "After a break-in attempt, we called SecureGuard and they had a full alarm system installed within 48 hours. The monitoring team caught a second attempt and police arrived in 6 minutes. Incredible.", "author": "Sarah Chen", "role": "Homeowner", "location": "Westside", "rating": 5, "image": None},
                            {"quote": "We manage 12 apartment buildings and SecureGuard handles all our access control and intercom systems. Their support is outstanding — any issue gets resolved same day.", "author": "Michael Torres", "role": "Property Manager, Urban Living", "location": "Metro Area", "rating": 5, "image": None}
                        ]
                    }
                },
                # --- FAQ ---
                {
                    "type": "faq",
                    "value": {
                        "variant": "v1", "animation": "fade-up", "section_id": "faq", "visible": True,
                        "enable_schema": True,
                        "title": "Frequently Asked Questions",
                        "items": [
                            {"question": "How much does a security system cost?", "answer": "<p>Our systems start at $29/month with free installation. The total cost depends on your property size and requirements. We offer free security audits to provide accurate quotes with no obligation.</p>"},
                            {"question": "Do you offer 24/7 monitoring?", "answer": "<p>Yes! Our monitoring center operates 24/7/365 with trained operators who respond to every alarm within 30 seconds. We partner with local law enforcement for rapid dispatch when needed.</p>"},
                            {"question": "Can I view my cameras remotely?", "answer": "<p>Absolutely. All our CCTV systems come with a free mobile app that lets you view live feeds, playback recordings, and receive motion alerts from anywhere in the world.</p>"},
                            {"question": "How long does installation take?", "answer": "<p>Most residential installations are completed in 4-6 hours. Commercial projects typically take 1-3 days depending on the scope. We schedule at your convenience and minimize disruption.</p>"},
                            {"question": "Do you offer warranties?", "answer": "<p>Yes, all equipment comes with a 3-year manufacturer warranty. Our workmanship is guaranteed for 5 years. We also offer extended warranty plans for complete peace of mind.</p>"},
                            {"question": "Are your technicians background-checked?", "answer": "<p>Every SecureGuard technician undergoes thorough background checks, drug screening, and is fully bonded and insured. Your safety and trust are our top priorities.</p>"}
                        ]
                    }
                },
                # --- Lead Form ---
                {
                    "type": "lead_form",
                    "value": {
                        "variant": "v1", "animation": "fade-up", "section_id": "contact", "visible": True,
                        "title": "Get Your Free Security Assessment",
                        "subtitle": "Fill out the form below and our security experts will contact you within 1 business hour.",
                        "form_action": "",
                        "success_message": "Thank you! A security specialist will contact you shortly.",
                        "fields": [
                            {"label": "Full Name", "field_type": "text", "required": True, "placeholder": "John Doe"},
                            {"label": "Email", "field_type": "email", "required": True, "placeholder": "john@example.com"},
                            {"label": "Phone", "field_type": "tel", "required": True, "placeholder": "+1 (555) 000-0000"},
                            {"label": "Property Type", "field_type": "select", "required": True, "placeholder": "Select property type"},
                            {"label": "Tell us about your security needs", "field_type": "textarea", "required": False, "placeholder": "Describe your requirements..."}
                        ]
                    }
                },
                # --- Final CTA ---
                {
                    "type": "final_cta",
                    "value": {
                        "variant": "v1", "animation": "fade-up", "section_id": "final-cta", "visible": True,
                        "title": "Don't Wait Until It's Too Late",
                        "subtitle": "Protect your family, property, and business with a security system you can trust. Free installation on all monitoring plans.",
                        "background_image": None,
                        "primary_cta_text": "Get Free Quote",
                        "primary_cta_link": "#contact",
                        "secondary_cta_text": "Call 1-800-555-SAFE",
                        "secondary_cta_link": "tel:+18005557233"
                    }
                }
            ])
        )
        root_page.add_child(instance=home)
        home.save_revision().publish()
        self.stdout.write(self.style.SUCCESS('  ✓ Home page created (11 blocks)'))

        # Update default site to point to home
        site = Site.objects.filter(is_default_site=True).first()
        if site:
            site.root_page = home
            site.save()

        # ============================================
        # 4. ABOUT PAGE
        # ============================================
        about = ContentPage(
            title="About Us",
            slug="about",
            body=json.dumps([
                {
                    "type": "hero",
                    "value": {
                        "variant": "v1", "animation": "fade-up", "section_id": "", "visible": True,
                        "title": "Securing Lives Since 2008",
                        "subtitle": "15+ years of protecting homes, businesses, and communities with cutting-edge security technology.",
                        "image": None, "background_video_url": "", "overlay": True,
                        "badge_text": "Est. 2008",
                        "cta_text": "Our Services", "cta_link": "/home/#services",
                        "secondary_cta_text": "Contact Us", "secondary_cta_link": "/contact/"
                    }
                },
                {
                    "type": "about",
                    "value": {
                        "variant": "v1", "animation": "fade-up", "section_id": "", "visible": True,
                        "title": "Our Story",
                        "content": "<p>SecureGuard Pro was founded with a simple mission: make professional-grade security accessible to everyone. What started as a two-person operation installing residential alarm systems has grown into the region's most trusted security provider.</p><p>Today, we protect over 500 homes and businesses with state-of-the-art CCTV, smart alarm systems, access control, and 24/7 monitoring. Our team of 40+ certified technicians delivers the same personal attention that built our reputation from day one.</p><p>We believe security shouldn't be complicated or expensive. That's why we offer free security audits, transparent pricing, and no lock-in contracts. Our customers stay because they want to, not because they have to.</p>",
                        "image": None
                    }
                },
                {
                    "type": "why_choose_us",
                    "value": {
                        "variant": "v1", "animation": "fade-up", "section_id": "", "visible": True,
                        "title": "Our Core Values",
                        "subtitle": "", "image": None, "cta_text": "", "cta_link": "",
                        "reasons": [
                            {"icon": "fa-shield-halved", "title": "Integrity First", "description": "We never recommend services you don't need. Honest assessments, transparent pricing, always."},
                            {"icon": "fa-people-group", "title": "Community Focused", "description": "We live where we work. Our neighborhoods' safety is personal to every team member."},
                            {"icon": "fa-rocket", "title": "Innovation Driven", "description": "We stay ahead of threats with the latest AI-powered cameras, smart sensors, and cloud technology."},
                            {"icon": "fa-award", "title": "Excellence in Service", "description": "97% customer satisfaction rate. We measure success by how safe our clients feel, not by sales numbers."}
                        ]
                    }
                },
                {
                    "type": "final_cta",
                    "value": {
                        "variant": "v1", "animation": "fade-up", "section_id": "", "visible": True,
                        "title": "Ready to Secure Your Property?",
                        "subtitle": "Book a free consultation with our security experts today.",
                        "background_image": None,
                        "primary_cta_text": "Book Free Consultation",
                        "primary_cta_link": "/contact/",
                        "secondary_cta_text": "Call Now",
                        "secondary_cta_link": "tel:+18005557233"
                    }
                }
            ])
        )
        home.add_child(instance=about)
        about.save_revision().publish()
        self.stdout.write(self.style.SUCCESS('  ✓ About page created'))

        # ============================================
        # 5. SERVICE PAGES (7)
        # ============================================
        services_data = [
            {"title": "CCTV Systems", "slug": "cctv-systems", "icon": "fa-video",
             "intro": "HD and 4K surveillance solutions with AI-powered analytics, night vision, and cloud storage.",
             "problem": "Property crime costs businesses billions annually. Without proper surveillance, break-ins go undetected and evidence is lost.",
             "solution": "Our CCTV systems provide 24/7 crystal-clear surveillance with AI motion detection, instant mobile alerts, and 30-day cloud recording."},
            {"title": "Alarm Systems", "slug": "alarm-systems", "icon": "fa-bell",
             "intro": "Smart intrusion detection with instant alerts and professional 24/7 monitoring.",
             "problem": "Traditional alarm systems have high false alarm rates and slow response times, leaving you vulnerable when it matters most.",
             "solution": "Our smart alarm systems use AI to distinguish real threats from false alarms, ensuring rapid dispatch only when you need it."},
            {"title": "Intercom Systems", "slug": "intercom-systems", "icon": "fa-walkie-talkie",
             "intro": "Video intercom with remote access and seamless building integration.",
             "problem": "Uncontrolled building access creates security vulnerabilities. Traditional buzzer systems offer no verification or recording.",
             "solution": "Our video intercom systems let you see, hear, and speak to visitors from anywhere. Integrated with access control for complete building security."},
            {"title": "Access Control", "slug": "access-control", "icon": "fa-key",
             "intro": "Keycard, biometric, and mobile-based access for secure facilities.",
             "problem": "Lost keys, copied badges, and untracked entry points create critical security gaps in commercial and residential properties.",
             "solution": "Our access control systems use biometric, keycard, and smartphone authentication with full audit trails and real-time access management."},
            {"title": "Smoke Detectors", "slug": "smoke-detectors", "icon": "fa-fire",
             "intro": "Intelligent fire detection with automated alerts and compliance certification.",
             "problem": "Fire causes devastating property damage and life-threatening situations. Early detection is critical for survival and damage control.",
             "solution": "Our intelligent smoke and heat detection systems provide multi-sensor protection with automated fire service notification."},
            {"title": "Site Security", "slug": "site-security", "icon": "fa-shield-halved",
             "intro": "Physical and electronic security for construction sites, events, and temporary locations.",
             "problem": "Construction sites and event venues face theft, vandalism, and liability risks that standard security can't address.",
             "solution": "Our site security combines mobile CCTV towers, perimeter detection, and remote monitoring for complete temporary security coverage."},
            {"title": "Security Lighting", "slug": "security-lighting", "icon": "fa-lightbulb",
             "intro": "Motion-activated and smart security lighting systems for deterrence and visibility.",
             "problem": "Dark areas around properties create hiding spots for intruders and increase the risk of accidents and criminal activity.",
             "solution": "Our security lighting systems use motion sensors, timers, and smart controls to illuminate threats and deter criminal activity."},
        ]

        for svc in services_data:
            service_page = ServicePage(
                title=svc["title"],
                slug=svc["slug"],
                icon=svc["icon"],
                intro=svc["intro"],
                body=json.dumps([
                    {
                        "type": "hero",
                        "value": {
                            "variant": "v1", "animation": "fade-up", "section_id": "", "visible": True,
                            "title": svc["title"],
                            "subtitle": svc["intro"],
                            "image": None, "background_video_url": "", "overlay": True,
                            "badge_text": "Professional Service",
                            "cta_text": "Get Free Quote", "cta_link": "/contact/",
                            "secondary_cta_text": "Call Now", "secondary_cta_link": "tel:+18005557233"
                        }
                    },
                    {
                        "type": "about",
                        "value": {
                            "variant": "v1", "animation": "fade-up", "section_id": "", "visible": True,
                            "title": "The Problem",
                            "content": f"<p>{svc['problem']}</p>",
                            "image": None
                        }
                    },
                    {
                        "type": "about",
                        "value": {
                            "variant": "v1", "animation": "fade-up", "section_id": "", "visible": True,
                            "title": "Our Solution",
                            "content": f"<p>{svc['solution']}</p>",
                            "image": None
                        }
                    },
                    {
                        "type": "cta",
                        "value": {
                            "variant": "v1", "animation": "fade-up", "section_id": "", "visible": True,
                            "title": f"Ready for Professional {svc['title']}?",
                            "subtitle": "Contact us today for a free security assessment and custom quote.",
                            "background_image": None, "icon": svc["icon"],
                            "button_text": "Get Free Quote",
                            "button_link": "/contact/"
                        }
                    },
                    {
                        "type": "faq",
                        "value": {
                            "variant": "v1", "animation": "fade-up", "section_id": "", "visible": True,
                            "enable_schema": True,
                            "title": f"Common Questions About {svc['title']}",
                            "items": [
                                {"question": f"How much do {svc['title'].lower()} cost?", "answer": f"<p>Pricing depends on your property size and requirements. We offer free assessments to provide accurate, no-obligation quotes for {svc['title'].lower()}.</p>"},
                                {"question": f"How long does {svc['title'].lower()} installation take?", "answer": f"<p>Most {svc['title'].lower()} installations are completed in 1-2 days. Our certified technicians work efficiently with minimal disruption to your routine.</p>"},
                                {"question": "Do you offer maintenance plans?", "answer": "<p>Yes! All our installations come with a standard warranty and we offer extended maintenance plans to keep your system running optimally.</p>"}
                            ]
                        }
                    },
                    {
                        "type": "final_cta",
                        "value": {
                            "variant": "v1", "animation": "fade-up", "section_id": "", "visible": True,
                            "title": "Protect Your Property Today",
                            "subtitle": f"Professional {svc['title'].lower()} with free installation and no lock-in contracts.",
                            "background_image": None,
                            "primary_cta_text": "Schedule Free Audit",
                            "primary_cta_link": "/contact/",
                            "secondary_cta_text": "1-800-555-SAFE",
                            "secondary_cta_link": "tel:+18005557233"
                        }
                    }
                ])
            )
            home.add_child(instance=service_page)
            service_page.save_revision().publish()

        self.stdout.write(self.style.SUCCESS(f'  ✓ {len(services_data)} service pages created'))

        # ============================================
        # 6. BLOG SYSTEM
        # ============================================
        blog_index = BlogIndexPage(
            title="Security Blog",
            slug="blog",
            intro="Expert tips, industry insights, and security guides to keep you informed and protected."
        )
        home.add_child(instance=blog_index)
        blog_index.save_revision().publish()

        blog_posts = [
            {
                "title": "5 Signs Your Home Security System Needs an Upgrade",
                "slug": "5-signs-security-upgrade",
                "date": "2026-02-01",
                "category": "Home Security",
                "intro": "Is your security system keeping up with modern threats? Here are five warning signs it's time for an upgrade."
            },
            {
                "title": "CCTV vs. Smart Cameras: Which Is Right for Your Business?",
                "slug": "cctv-vs-smart-cameras",
                "date": "2026-01-25",
                "category": "CCTV",
                "intro": "Understanding the difference between traditional CCTV and modern smart camera systems can save you thousands."
            },
            {
                "title": "The Complete Guide to Access Control for Commercial Buildings",
                "slug": "access-control-guide",
                "date": "2026-01-15",
                "category": "Access Control",
                "intro": "Everything you need to know about implementing modern access control in your commercial property."
            }
        ]

        for bp in blog_posts:
            post = BlogPostPage(
                title=bp["title"],
                slug=bp["slug"],
                date=bp["date"],
                category=bp["category"],
                intro=bp["intro"],
                body=json.dumps([
                    {"type": "paragraph", "value": f"<p>{bp['intro']}</p><p>Security technology evolves rapidly. What was cutting-edge five years ago may now leave your property vulnerable to sophisticated modern threats. Regular security audits and system updates are essential to maintaining protection.</p><p>At SecureGuard Pro, we recommend reviewing your security setup annually. Our free security assessments identify gaps and recommend cost-effective upgrades that make a real difference.</p>"},
                    {
                        "type": "cta",
                        "value": {
                            "variant": "v1", "animation": "fade-up", "section_id": "", "visible": True,
                            "title": "Need Expert Security Advice?",
                            "subtitle": "Book a free consultation with our security specialists.",
                            "background_image": None, "icon": "fa-shield-halved",
                            "button_text": "Book Free Consultation",
                            "button_link": "/contact/"
                        }
                    },
                    {"type": "paragraph", "value": "<p>Don't wait until something goes wrong. Proactive security upgrades cost a fraction of what you'd spend recovering from a security breach. Contact us today for a no-obligation assessment of your current system.</p>"}
                ])
            )
            blog_index.add_child(instance=post)
            post.save_revision().publish()

        self.stdout.write(self.style.SUCCESS(f'  ✓ Blog with {len(blog_posts)} posts created'))

        # ============================================
        # 7. SERVICE AREAS
        # ============================================
        sa_index = ServiceAreaIndexPage(
            title="Service Areas",
            slug="service-areas",
            intro="We provide professional security services across the metro area and surrounding regions."
        )
        home.add_child(instance=sa_index)
        sa_index.save_revision().publish()

        areas = [
            {"title": "Downtown Security Services", "slug": "downtown", "location": "Downtown"},
            {"title": "Westside Security Services", "slug": "westside", "location": "Westside"},
            {"title": "North County Security Services", "slug": "north-county", "location": "North County"},
        ]

        for area in areas:
            sa = ServiceAreaPage(
                title=area["title"],
                slug=area["slug"],
                location_name=area["location"],
                body=json.dumps([
                    {
                        "type": "hero",
                        "value": {
                            "variant": "v1", "animation": "fade-up", "section_id": "", "visible": True,
                            "title": f"Security Services in {area['location']}",
                            "subtitle": f"Trusted local security provider serving {area['location']} homes and businesses.",
                            "image": None, "background_video_url": "", "overlay": True,
                            "badge_text": f"Serving {area['location']}",
                            "cta_text": "Get Local Quote", "cta_link": "/contact/",
                            "secondary_cta_text": "Call Now", "secondary_cta_link": "tel:+18005557233"
                        }
                    },
                    {
                        "type": "services",
                        "value": {
                            "variant": "v1", "animation": "fade-up", "section_id": "", "visible": True,
                            "title": f"Services Available in {area['location']}",
                            "subtitle": "",
                            "services": [
                                {"icon": "fa-video", "image": None, "name": "CCTV Installation", "description": f"Professional CCTV installation and monitoring in {area['location']}.", "cta_text": "Learn More", "link": ""},
                                {"icon": "fa-bell", "image": None, "name": "Alarm Systems", "description": f"Smart alarm systems with 24/7 monitoring for {area['location']} properties.", "cta_text": "Learn More", "link": ""},
                                {"icon": "fa-key", "image": None, "name": "Access Control", "description": f"Commercial and residential access control solutions in {area['location']}.", "cta_text": "Learn More", "link": ""}
                            ]
                        }
                    },
                    {
                        "type": "final_cta",
                        "value": {
                            "variant": "v1", "animation": "fade-up", "section_id": "", "visible": True,
                            "title": f"Protect Your {area['location']} Property",
                            "subtitle": "Free security assessment for all local residents and businesses.",
                            "background_image": None,
                            "primary_cta_text": "Get Free Quote",
                            "primary_cta_link": "/contact/",
                            "secondary_cta_text": "Call 1-800-555-SAFE",
                            "secondary_cta_link": "tel:+18005557233"
                        }
                    }
                ])
            )
            sa_index.add_child(instance=sa)
            sa.save_revision().publish()

        self.stdout.write(self.style.SUCCESS(f'  ✓ {len(areas)} service areas created'))

        # ============================================
        # 8. CONTACT PAGE
        # ============================================
        contact = ContactPage(
            title="Contact Us",
            slug="contact",
            thank_you_text="Thank you for contacting SecureGuard Pro! A security specialist will reach out within 1 business hour.",
            address="123 Security Boulevard, Suite 400\nMetro City, MC 10001",
            phone_cta="+1-800-555-SAFE",
            emergency_text="🚨 Emergency? Call our 24/7 hotline now!",
            intro=json.dumps([
                {
                    "type": "hero",
                    "value": {
                        "variant": "v1", "animation": "fade-up", "section_id": "", "visible": True,
                        "title": "Contact SecureGuard Pro",
                        "subtitle": "Get in touch for a free security assessment or emergency assistance.",
                        "image": None, "background_video_url": "", "overlay": True,
                        "badge_text": "24/7 Support",
                        "cta_text": "", "cta_link": "",
                        "secondary_cta_text": "", "secondary_cta_link": ""
                    }
                }
            ])
        )
        home.add_child(instance=contact)
        contact.save_revision().publish()

        # Add form fields
        FormField.objects.create(page=contact, sort_order=1, label="Full Name", field_type="singleline", required=True)
        FormField.objects.create(page=contact, sort_order=2, label="Email", field_type="email", required=True)
        FormField.objects.create(page=contact, sort_order=3, label="Phone", field_type="singleline", required=True)
        FormField.objects.create(page=contact, sort_order=4, label="Message", field_type="multiline", required=False)

        self.stdout.write(self.style.SUCCESS('  ✓ Contact page created with form fields'))

        # ============================================
        # 9. NAVIGATION MENU
        # ============================================
        menu, _ = Menu.objects.get_or_create(slug="main", defaults={"title": "Main Navigation"})
        menu.menu_items.all().delete()  # Clean slate

        menu_items = [
            ("Home", "/"),
            ("About", "/about/"),
            ("Services", "/#services"),
            ("Blog", "/blog/"),
            ("Areas", "/service-areas/"),
            ("Contact", "/contact/"),
        ]
        for i, (title, url) in enumerate(menu_items):
            MenuItem.objects.create(menu=menu, link_title=title, link_url=url, sort_order=i)

        self.stdout.write(self.style.SUCCESS('  ✓ Navigation menu created'))

        # ============================================
        # 10. SITE SETTINGS
        # ============================================
        site = Site.objects.filter(is_default_site=True).first()
        if site:
            settings, _ = SiteSettings.objects.get_or_create(site=site)
            settings.site_name = "SecureGuard Pro"
            settings.phone_number = "1-800-555-SAFE"
            settings.email_address = "info@secureguardpro.com"
            settings.header_cta_text = "Get Free Quote"
            settings.header_cta_link = "/contact/"
            settings.announcement_text = "🔒 Free Security Audit for New Customers — Limited Time Offer!"
            settings.announcement_link = "/contact/"
            settings.emergency_badge_text = "24/7 Emergency"
            settings.emergency_phone = "1-800-911-SAFE"
            settings.address = "123 Security Boulevard, Suite 400\nMetro City, MC 10001"
            
            # New dynamic labels
            settings.gallery_tag = "Featured Projects"
            settings.process_tag = "Our Security Process"
            settings.industries_tag = "Sectors We Protect"
            settings.partners_tag = "Trusted Partners"
            settings.success_stories_tag = "Client Success Stories"
            settings.submit_button_label = "Request Free Quote"
            settings.no_results_message = "No articles found in this category. Please check back soon!"
            settings.form_success_message = "Great! Your security request has been sent. A specialist will call you shortly."
            settings.emergency_contact_label = "24/7 Security Hotline"
            settings.contact_form_title = "Tailored Security Consultation"
            
            # Icons
            settings.announcement_icon = "fa-bell"
            settings.emergency_icon = "fa-shield-halved"
            settings.phone_icon = "fa-phone"
            settings.email_icon = "fa-envelope"
            settings.location_icon = "fa-location-dot"
            settings.menu_icon = "fa-bars"
            
            settings.save()
            self.stdout.write(self.style.SUCCESS('  ✓ Site settings configured'))

        self.stdout.write(self.style.SUCCESS('\n🎉 DONE! Full Security Services website seeded.'))
        self.stdout.write('  📄 Pages: Home, About, 7 Services, Blog (3 posts), 3 Service Areas, Contact')
        self.stdout.write('  🧱 Blocks used: CarouselHero, TrustBar, Services, WhyChooseUs, Industries,')
        self.stdout.write('                 ProcessSteps, Testimonials, FAQ, LeadForm, FinalCTA, CTA, About')
        self.stdout.write(f'\n  🌐 Visit: http://localhost:8000/')
