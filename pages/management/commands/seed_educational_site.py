"""
Management command to seed a complete Educational Institution website.
Creates: Home, About, Programs (6), Blog/News (3 posts), Admissions, Campus, Contact page.
Uses all 18 block types with realistic educational content.
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
    help = 'Seeds a complete Educational Institution demo website'

    def handle(self, *args, **options):
        self.stdout.write('[Educational Site] Seeding Educational Institution website...\n')

        # ============================================
        # 1. THEME CONFIG
        # ============================================
        site = Site.objects.filter(is_default_site=True).first()
        if not site:
            self.stdout.write(self.style.ERROR('No default site found. Please create a site first.'))
            return
            
        config, _ = ThemeSettings.objects.update_or_create(
            site=site,
            defaults={
                'base_theme': 'modern',
                'primary_color': '#2563EB',  # Blue for education
                'secondary_color': '#F59E0B',  # Amber for highlights
                'background_color': '#0F172A',  # Dark blue-gray
                'text_color': '#FFFFFF',
                'heading_font': 'Inter',
                'body_font': 'Inter',
            }
        )
        self.stdout.write(self.style.SUCCESS('  ✓ Theme configured'))

        # ============================================
        # 2. GET ROOT PAGE — clean existing pages
        # ============================================
        Page.objects.filter(depth__gt=1).delete()
        Page.fix_tree()
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
                        "autoplay": True, "autoplay_speed": 6000, "pause_on_hover": True,
                        "show_arrows": True, "show_dots": True,
                        "animation_type": "fade", "animation_speed": 800,
                        "slides": [
                            {
                                "title": "Shape Your Future at EduVerse Academy",
                                "subtitle": "World-class education with cutting-edge programs in technology, business, arts, and sciences. Join our community of innovative learners.",
                                "image": None, "background_video_url": "", "overlay": True,
                                "badge_text": "Top Ranked University",
                                "cta_text": "Apply Now",
                                "cta_link": "/admissions/",
                                "secondary_cta_text": "Explore Programs",
                                "secondary_cta_link": "#programs",
                                "enabled": True
                            },
                            {
                                "title": "Experience Campus Life",
                                "subtitle": "State-of-the-art facilities, vibrant student organizations, and a supportive community that helps you thrive both academically and personally.",
                                "image": None, "background_video_url": "", "overlay": True,
                                "badge_text": "Award-Winning Campus",
                                "cta_text": "Schedule Campus Tour",
                                "cta_link": "/campus-life/",
                                "secondary_cta_text": "Virtual Tour",
                                "secondary_cta_link": "#campus",
                                "enabled": True
                            },
                            {
                                "title": "Research & Innovation",
                                "subtitle": "Join faculty and students pushing the boundaries of knowledge in AI, biotechnology, sustainability, and social sciences.",
                                "image": None, "background_video_url": "", "overlay": True,
                                "badge_text": "Research Excellence",
                                "cta_text": "Explore Research",
                                "cta_link": "#programs",
                                "secondary_cta_text": "Apply for Grants",
                                "secondary_cta_link": "/contact/",
                                "enabled": True
                            }
                        ]
                    }
                },
                # --- Trust Bar (Accreditation) ---
                {
                    "type": "trust_bar",
                    "value": {
                        "title": "Accredited & Recognized",
                        "variant": "v1",
                        "animation": "fade-up",
                        "section_id": "accreditation",
                        "visible": True,
                        "partners": [
                            {"name": "Regional Accreditation Commission", "logo": None, "url": "#"},
                            {"name": "National Education Board", "logo": None, "url": "#"},
                            {"name": "Association of Universities", "logo": None, "url": "#"},
                            {"name": "Quality Assurance Agency", "logo": None, "url": "#"}
                        ]
                    }
                },
                # --- About Block ---
                {
                    "type": "about",
                    "value": {
                        "section_tag": "About EduVerse",
                        "title": "Empowering Learners Since 1985",
                        "description": "EduVerse Academy is a premier institution dedicated to fostering innovation, critical thinking, and global citizenship. With over 15,000 students from 80+ countries, we offer transformative educational experiences backed by world-class faculty and cutting-edge research facilities.",
                        "variant": "v1",
                        "animation": "fade-up",
                        "section_id": "about",
                        "visible": True,
                        "image": None,
                        "stats": [
                            {"number": "15,000+", "label": "Active Students"},
                            {"number": "500+", "label": "Expert Faculty"},
                            {"number": "80+", "label": "Countries Represented"},
                            {"number": "95%", "label": "Graduate Employment Rate"}
                        ],
                        "features": [
                            {"icon": "fa-graduation-cap", "title": "Accredited Programs", "text": "60+ undergraduate and graduate programs"},
                            {"icon": "fa-users", "title": "Small Class Sizes", "text": "15:1 student-faculty ratio"},
                            {"icon": "fa-building", "title": "Modern Facilities", "text": "$200M in recent campus upgrades"},
                            {"icon": "fa-globe", "title": "Global Network", "text": "200+ university partnerships worldwide"}
                        ]
                    }
                },
                # --- Services Block (Programs) ---
                {
                    "type": "services",
                    "value": {
                        "section_tag": "Our Programs",
                        "title": "Explore Your Path",
                        "description": "Choose from our diverse range of undergraduate and graduate programs designed to prepare you for success in a rapidly changing world.",
                        "variant": "v1",
                        "animation": "fade-up",
                        "section_id": "programs",
                        "visible": True,
                        "services": [
                            {
                                "icon": "fa-laptop-code",
                                "title": "Computer Science & Technology",
                                "description": "Master AI, cybersecurity, software engineering, and data science with hands-on projects.",
                                "link": "/computer-science/",
                                "cta_text": "Learn More",
                                "enabled": True
                            },
                            {
                                "icon": "fa-chart-line",
                                "title": "Business & Economics",
                                "description": "Develop leadership skills in finance, marketing, entrepreneurship, and international business.",
                                "link": "/business/",
                                "cta_text": "Learn More",
                                "enabled": True
                            },
                            {
                                "icon": "fa-flask",
                                "title": "Sciences & Engineering",
                                "description": "Advance in biology, chemistry, physics, mechanical, and electrical engineering.",
                                "link": "/sciences-engineering/",
                                "cta_text": "Learn More",
                                "enabled": True
                            },
                            {
                                "icon": "fa-palette",
                                "title": "Arts & Humanities",
                                "description": "Express creativity through visual arts, music, literature, philosophy, and history.",
                                "link": "/arts-humanities/",
                                "cta_text": "Learn More",
                                "enabled": True
                            },
                            {
                                "icon": "fa-heartbeat",
                                "title": "Health Sciences",
                                "description": "Train in nursing, public health, biomedical sciences, and healthcare management.",
                                "link": "/health-sciences/",
                                "cta_text": "Learn More",
                                "enabled": True
                            },
                            {
                                "icon": "fa-globe-americas",
                                "title": "Social Sciences",
                                "description": "Study psychology, sociology, political science, and international relations.",
                                "link": "/social-sciences/",
                                "cta_text": "Learn More",
                                "enabled": True
                            }
                        ]
                    }
                },
                # --- Why Choose Us ---
                {
                    "type": "why_choose_us",
                    "value": {
                        "section_tag": "Why Choose EduVerse",
                        "title": "Your Success is Our Mission",
                        "description": "We provide more than just education—we create opportunities for growth, discovery, and lifelong connections.",
                        "variant": "v1",
                        "animation": "fade-up",
                        "section_id": "why-choose",
                        "visible": True,
                        "image": None,
                        "reasons": [
                            {
                                "icon": "fa-award",
                                "title": "Top-Ranked Programs",
                                "description": "Nationally recognized excellence across multiple disciplines with industry-leading faculty."
                            },
                            {
                                "icon": "fa-hand-holding-usd",
                                "title": "Generous Financial Aid",
                                "description": "$50M+ in scholarships awarded annually. 80% of students receive financial assistance."
                            },
                            {
                                "icon": "fa-rocket",
                                "title": "Career Services",
                                "description": "Dedicated career center with 95% job placement rate within 6 months of graduation."
                            },
                            {
                                "icon": "fa-users-cog",
                                "title": "Research Opportunities",
                                "description": "Undergraduate research grants and partnerships with leading tech and healthcare companies."
                            }
                        ]
                    }
                },
                # --- Process Steps (Admissions) ---
                {
                    "type": "process_steps",
                    "value": {
                        "section_tag": "Admissions Process",
                        "title": "Your Journey Starts Here",
                        "description": "Applying to EduVerse Academy is straightforward. Follow these simple steps to begin your educational journey.",
                        "variant": "v1",
                        "animation": "fade-up",
                        "section_id": "admissions",
                        "visible": True,
                        "steps": [
                            {
                                "number": "01",
                                "title": "Submit Application",
                                "description": "Complete our online application with your academic transcripts and personal statement."
                            },
                            {
                                "number": "02",
                                "title": "Upload Documents",
                                "description": "Provide letters of recommendation, test scores (optional), and any additional materials."
                            },
                            {
                                "number": "03",
                                "title": "Interview (Optional)",
                                "description": "Selected applicants may be invited for a virtual or in-person interview with admissions."
                            },
                            {
                                "number": "04",
                                "title": "Receive Decision",
                                "description": "Get your admissions decision within 4-6 weeks. Financial aid packages sent with acceptance."
                            },
                            {
                                "number": "05",
                                "title": "Enroll & Register",
                                "description": "Accept your offer, pay your deposit, and register for orientation and courses."
                            }
                        ]
                    }
                },
                # --- Testimonials (Student Reviews) ---
                {
                    "type": "testimonials",
                    "value": {
                        "section_tag": "Student Voices",
                        "title": "Hear From Our Community",
                        "variant": "v1",
                        "animation": "fade-up",
                        "section_id": "testimonials",
                        "visible": True,
                        "testimonials": [
                            {
                                "quote": "EduVerse gave me the skills and confidence to launch my tech startup. The entrepreneurship program and faculty mentorship were invaluable.",
                                "author": "Sarah Chen",
                                "role": "Computer Science '23, Founder at TechFlow",
                                "image": None,
                                "rating": 5
                            },
                            {
                                "quote": "The research opportunities here are unmatched. I published two papers as an undergrad and got accepted to MIT for my PhD.",
                                "author": "Michael Rodriguez",
                                "role": "Engineering '24, PhD Candidate at MIT",
                                "image": None,
                                "rating": 5
                            },
                            {
                                "quote": "Amazing campus life and diversity. I've made lifelong friends from around the world and discovered passions I didn't know I had.",
                                "author": "Aisha Patel",
                                "role": "Business '25, Current Student",
                                "image": None,
                                "rating": 5
                            }
                        ]
                    }
                },
                # --- Lead Form (Inquiry Form) ---
                {
                    "type": "lead_form",
                    "value": {
                        "section_tag": "Request Information",
                        "title": "Take the Next Step",
                        "description": "Have questions? Want to schedule a campus tour? Fill out this form and an admissions counselor will contact you within 24 hours.",
                        "variant": "v1",
                        "animation": "fade-up",
                        "section_id": "inquiry",
                        "visible": True,
                        "name_label": "Full Name",
                        "email_label": "Email Address",
                        "phone_label": "Phone Number (Optional)",
                        "message_label": "Tell us about your interests",
                        "submit_text": "Submit Inquiry",
                        "success_message": "Thank you! An admissions counselor will reach out soon.",
                        "redirect_url": ""
                    }
                }
            ])
        )
        root_page.add_child(instance=home)
        site.root_page = home
        site.save()
        self.stdout.write(self.style.SUCCESS('  ✓ Home page created (9 blocks)'))

        # ============================================
        # 4. ABOUT PAGE
        # ============================================
        about = ContentPage(
            title="About",
            slug="about",
            body=json.dumps([
                {
                    "type": "about",
                    "value": {
                        "section_tag": "Our Story",
                        "title": "A Legacy of Excellence Since 1985",
                        "description": "Founded by Dr. Elizabeth Morgan, EduVerse Academy began with a vision to make quality education accessible to all. Today, we're recognized globally for our innovative programs, diverse community, and commitment to social responsibility.",
                        "variant": "v1",
                        "animation": "fade-up",
                        "section_id": "story",
                        "visible": True,
                        "image": None,
                        "stats": [
                            {"number": "40", "label": "Years of Excellence"},
                            {"number": "100,000+", "label": "Alumni Worldwide"},
                            {"number": "$2B", "label": "Research Funding"},
                            {"number": "150+", "label": "Academic Programs"}
                        ],
                        "features": []
                    }
                },
                {
                    "type": "why_choose_us",
                    "value": {
                        "section_tag": "Our Values",
                        "title": "What We Stand For",
                        "description": "Our core values guide everything we do, from curriculum design to community engagement.",
                        "variant": "v1",
                        "animation": "fade-up", 
                        "section_id": "values",
                        "visible": True,
                        "image": None,
                        "reasons": [
                            {"icon": "fa-lightbulb", "title": "Innovation", "description": "Fostering creativity and entrepreneurial thinking"},
                            {"icon": "fa-balance-scale", "title": "Integrity", "description": "Upholding the highest ethical standards"},
                            {"icon": "fa-hands-helping", "title": "Inclusivity", "description": "Celebrating diversity and promoting equity"},
                            {"icon": "fa-leaf", "title": "Sustainability", "description": "Commitment to environmental stewardship"}
                        ]
                    }
                }
            ])
        )
        home.add_child(instance=about)
        self.stdout.write(self.style.SUCCESS('  ✓ About page created'))

        # ============================================
        # 5. PROGRAM PAGES (6 programs)
        # ============================================
        programs = [
            {
                "title": "Computer Science & Technology",
                "slug": "computer-science",
                "intro": "Prepare for careers in software engineering, AI, cybersecurity, and data science with our comprehensive CS program.",
                "icon": "fa-laptop-code",
                "blocks": [
                    {"type": "about", "value": {
                        "section_tag": "Program Overview",
                        "title": "Lead the Digital Revolution",
                        "description": "Our Computer Science program combines theoretical foundations with hands-on experience in cutting-edge technologies. Work on real-world projects, contribute to open source, and intern at top tech companies.",
                        "variant": "v1", "animation": "fade-up", "section_id": "overview", "visible": True,
                        "image": None,
                        "stats": [
                            {"number": "92%", "label": "Job Placement Rate"},
                            {"number": "$85K", "label": "Average Starting Salary"},
                            {"number": "1:12", "label": "Faculty-Student Ratio"},
                            {"number": "25+", "label": "Industry Partners"}
                        ],
                        "features": []
                    }},
                    {"type": "why_choose_us", "value": {
                        "section_tag": "Specializations",
                        "title": "Choose Your Path",
                        "description": "Customize your degree with specialized tracks aligned to your career goals.",
                        "variant": "v1", "animation": "fade-up", "section_id": "tracks", "visible": True,
                        "image": None,
                        "reasons": [
                            {"icon": "fa-brain", "title": "Artificial Intelligence", "description": "Machine learning, neural networks, NLP"},
                            {"icon": "fa-shield-alt", "title": "Cybersecurity", "description": "Network security, ethical hacking, cryptography"},
                            {"icon": "fa-database", "title": "Data Science", "description": "Big data, analytics, visualization"},
                            {"icon": "fa-mobile-alt", "title": "Software Engineering", "description": "Full-stack, mobile, cloud development"}
                        ]
                    }}
                ]
            },
            {
                "title": "Business & Economics",
                "slug": "business",
                "intro": "Develop leadership skills and business acumen to excel in finance, marketing, entrepreneurship, and management.",
                "icon": "fa-chart-line",
                "blocks": [
                    {"type": "about", "value": {
                        "section_tag": "Program Overview",
                        "title": "Shape the Future of Business",
                        "description": "Our AACSB-accredited business program prepares you for leadership roles in a global economy. Learn from industry experts, participate in case competitions, and build your professional network.",
                        "variant": "v1", "animation": "fade-up", "section_id": "overview", "visible": True,
                        "image": None,
                        "stats": [
                            {"number": "Top 50", "label": "Business School Ranking"},
                            {"number": "89%", "label": "Job Placement Rate"},
                            {"number": "$72K", "label": "Average Starting Salary"},
                            {"number": "100+", "label": "Corporate Partners"}
                        ],
                        "features": []
                    }}
                ]
            },
            {
                "title": "Sciences & Engineering",
                "slug": "sciences-engineering",
                "intro": "Advance scientific knowledge and engineering solutions through research, innovation, and hands-on laboratory experience.",
                "icon": "fa-flask",
                "blocks": [
                    {"type": "about", "value": {
                        "section_tag": "Program Overview",
                        "title": "Innovate Through Science",
                        "description": "Engage in cutting-edge research across biology, chemistry, physics, and engineering disciplines. Access state-of-the-art labs and work on projects addressing global challenges.",
                        "variant": "v1", "animation": "fade-up", "section_id": "overview", "visible": True,
                        "image": None,
                        "stats": [
                            {"number": "$500M", "label": "Research Funding"},
                            {"number": "30+", "label": "Research Labs"},
                            {"number": "200+", "label": "Publications/Year"},
                            {"number": "85%", "label": "Graduate School Admission"}
                        ],
                        "features": []
                    }}
                ]
            },
            {
                "title": "Arts & Humanities",
                "slug": "arts-humanities",
                "intro": "Explore human creativity, culture, and expression through visual arts, music, literature, and philosophy.",
                "icon": "fa-palette",
                "blocks": [
                    {"type": "about", "value": {
                        "section_tag": "Program Overview",
                        "title": "Create, Think, Express",
                        "description": "Our Arts & Humanities programs foster critical thinking, creativity, and cultural awareness. From studio art to creative writing, develop your unique voice and perspective.",
                        "variant": "v1", "animation": "fade-up", "section_id": "overview", "visible": True,
                        "image": None,
                        "stats": [
                            {"number": "50+", "label": "Student Exhibitions/Year"},
                            {"number": "15", "label": "Performance Venues"},
                            {"number": "100%", "label": "Study Abroad Opportunities"},
                            {"number": "Award-Winning", "label": "Faculty Artists"}
                        ],
                        "features": []
                    }}
                ]
            },
            {
                "title": "Health Sciences",
                "slug": "health-sciences",
                "intro": "Train for careers in nursing, public health, biomedical research, and healthcare administration.",
                "icon": "fa-heartbeat",
                "blocks": [
                    {"type": "about", "value": {
                        "section_tag": "Program Overview",
                        "title": "Advance Health & Wellness",
                        "description": "Our health sciences programs prepare compassionate, skilled professionals to improve community health outcomes. Benefit from clinical partnerships with leading hospitals and health systems.",
                        "variant": "v1", "animation": "fade-up", "section_id": "overview", "visible": True,
                        "image": None,
                        "stats": [
                            {"number": "98%", "label": "NCLEX Pass Rate"},
                            {"number": "50+", "label": "Clinical Partners"},
                            {"number": "$68K", "label": "Average RN Salary"},
                            {"number": "100%", "label": "Job Placement Rate"}
                        ],
                        "features": []
                    }}
                ]
            },
            {
                "title": "Social Sciences",
                "slug": "social-sciences",
                "intro": "Understand human behavior, societies, and global challenges through psychology, sociology, and political science.",
                "icon": "fa-globe-americas",
                "blocks": [
                    {"type": "about", "value": {
                        "section_tag": "Program Overview",
                        "title": "Understand Society & Behavior",
                        "description": "Explore the complexities of human behavior and social structures. Conduct original research, engage in community-based learning, and develop analytical skills for careers in policy, counseling, and research.",
                        "variant": "v1", "animation": "fade-up", "section_id": "overview", "visible": True,
                        "image": None,
                        "stats": [
                            {"number": "40+", "label": "Faculty Researchers"},
                            {"number": "75%", "label": "Pursue Graduate Studies"},
                            {"number": "30+", "label": "Community Partnerships"},
                            {"number": "Top 100", "label": "Program Ranking"}
                        ],
                        "features": []
                    }}
                ]
            }
        ]

        for prog_data in programs:
            prog_page = ServicePage(
                title=prog_data["title"],
                slug=prog_data["slug"],
                intro=prog_data["intro"],
                icon=prog_data["icon"],
                body=json.dumps(prog_data["blocks"])
            )
            home.add_child(instance=prog_page)
        self.stdout.write(self.style.SUCCESS('  ✓ 6 program pages created'))

        # ============================================
        # 6. ADMISSIONS PAGE
        # ============================================
        admissions = ContentPage(
            title="Admissions",
            slug="admissions",
            body=json.dumps([
                {
                    "type": "process_steps",
                    "value": {
                        "section_tag": "Application Process",
                        "title": "How to Apply",
                        "description": "Start your journey to EduVerse Academy with our straightforward application process.",
                        "variant": "v1",
                        "animation": "fade-up",
                        "section_id": "process",
                        "visible": True,
                        "steps": [
                            {"number": "01", "title": "Create Account", "description": "Register on our admissions portal"},
                            {"number": "02", "title": "Complete Application", "description": "Fill out the online form with your information"},
                            {"number": "03", "title": "Submit Documents", "description": "Upload transcripts, test scores, and recommendations"},
                            {"number": "04", "title": "Await Decision", "description": "Receive notification within 4-6 weeks"},
                            {"number": "05", "title": "Accept Offer", "description": "Confirm enrollment and pay deposit"}
                        ]
                    }
                },
                {
                    "type": "faq",
                    "value": {
                        "section_tag": "Admissions FAQs",
                        "title": "Common Questions",
                        "variant": "v1",
                        "animation": "fade-up",
                        "section_id": "faq",
                        "visible": True,
                        "questions": [
                            {"question": "What are the admission requirements?", "answer": "High school diploma or equivalent, minimum 3.0 GPA, SAT/ACT scores (optional), personal statement, and two letters of recommendation."},
                            {"question": "What is the application deadline?", "answer": "Regular decision: March 1st. Early decision: November 15th. Rolling admissions for select programs."},
                            {"question": "How much is tuition?", "answer": "Tuition is $45,000/year for undergraduates. However, 80% of students receive financial aid averaging $25,000."},
                            {"question": "Can international students apply?", "answer": "Yes! We welcome international students. Additional requirements include TOEFL/IELTS scores and financial documentation."},
                            {"question": "Is campus housing guaranteed?", "answer": "Yes, all first-year students are guaranteed on-campus housing. Upperclassmen can apply for residence halls or off-campus options."}
                        ]
                    }
                }
            ])
        )
        home.add_child(instance=admissions)
        self.stdout.write(self.style.SUCCESS('  ✓ Admissions page created'))

        # ============================================
        # 7. CAMPUS LIFE PAGE
        # ============================================
        campus = ContentPage(
            title="Campus Life",
            slug="campus-life",
            body=json.dumps([
                {
                    "type": "about",
                    "value": {
                        "section_tag": "Campus Experience",
                        "title": "More Than Just Classes",
                        "description": "Life at EduVerse extends far beyond the classroom. With 200+ student organizations, Division II athletics, state-of-the-art recreation facilities, and a vibrant arts scene, there's something for everyone.",
                        "variant": "v1",
                        "animation": "fade-up",
                        "section_id": "experience",
                        "visible": True,
                        "image": None,
                        "stats": [
                            {"number": "200+", "label": "Student Organizations"},
                            {"number": "18", "label": "NCAA Sports Teams"},
                            {"number": "95%", "label": "Students Live on Campus"},
                            {"number": "500+", "label": "Events Per Year"}
                        ],
                        "features": []
                    }
                },
                {
                    "type": "services",
                    "value": {
                        "section_tag": "Campus Facilities",
                        "title": "World-Class Amenities",
                        "description": "Our campus features modern facilities designed to support your academic and personal growth.",
                        "variant": "v1",
                        "animation": "fade-up",
                        "section_id": "facilities",
                        "visible": True,
                        "services": [
                            {"icon": "fa-book", "title": "Main Library", "description": "3 million volumes, 24/7 study spaces, research support", "link": "#", "cta_text": "", "enabled": True},
                            {"icon": "fa-dumbbell", "title": "Recreation Center", "description": "200,000 sq ft fitness center, pool, climbing wall, courts", "link": "#", "cta_text": "", "enabled": True},
                            {"icon": "fa-utensils", "title": "Dining Halls", "description": "8 dining locations with diverse, healthy menu options", "link": "#", "cta_text": "", "enabled": True},
                            {"icon": "fa-home", "title": "Residence Halls", "description": "15 residence halls with suite and apartment-style living", "link": "#", "cta_text": "", "enabled": True},
                            {"icon": "fa-theater-masks", "title": "Performing Arts Center", "description": "1,200-seat theater, black box studio, music halls", "link": "#", "cta_text": "", "enabled": True},
                            {"icon": "fa-medkit", "title": "Health Center", "description": "On-campus medical care, counseling, wellness programs", "link": "#", "cta_text": "", "enabled": True}
                        ]
                    }
                }
            ])
        )
        home.add_child(instance=campus)
        self.stdout.write(self.style.SUCCESS('  ✓ Campus Life page created'))

        # ============================================
        # 8. BLOG (News & Events)
        # ============================================
        blog_index = BlogIndexPage(title="News & Events", slug="news")
        home.add_child(instance=blog_index)

        blog_posts = [
            {
                "title": "EduVerse Receives $50M Grant for AI Research Center",
                "slug": "ai-research-grant",
                "intro": "Major federal funding will establish new center for artificial intelligence and machine learning research.",
                "date": "2026-02-01",
                "category": "Research",
                "body": [
                    {"type": "heading", "value": "Transforming AI Education"},
                    {"type": "paragraph", "value": "<p>EduVerse Academy has been awarded a $50 million federal grant to establish the Center for Advanced AI Research. The center will focus on ethical AI development, machine learning applications in healthcare, and workforce training programs. This positions EduVerse as a national leader in AI education and research. Construction begins summer 2026.</p>"}
                ]
            },
            {
                "title": "Student Startup Wins $1M in National Competition",
                "slug": "student-startup-wins",
                "intro": "EduVerse entrepreneurship team takes top prize at National Collegiate Business Competition.",
                "date": "2026-02-05",
                "category": "Students",
                "body": [
                    {"type": "heading", "value": "Innovation in Action"},
                    {"type": "paragraph", "value": "<p>A team of business and engineering students from EduVerse won first place and $1 million in funding at the National Collegiate Business Competition. Their startup, 'GreenPack Solutions,' creates biodegradable packaging from agricultural waste. The team will use the prize money to scale production and bring their product to market. This win highlights EduVerse's strong entrepreneurship ecosystem.</p>"}
                ]
            },
            {
                "title": "Spring Open House: Explore Campus on April 12th",
                "slug": "spring-open-house",
                "intro": "Prospective students and families invited to experience EduVerse firsthand.",
                "date": "2026-02-10",
                "category": "Events",
                "body": [
                    {"type": "heading", "value": "Visit Us This Spring"},
                    {"type": "paragraph", "value": "<p>Join us for Spring Open House on Saturday, April 12th from 9am-4pm. Tour campus, meet faculty and current students, attend sample lectures, explore residence halls, and learn about financial aid. Registration is free but required. Lunch will be provided. This is the perfect opportunity to envision yourself as part of the EduVerse community. Register at admissions.eduverse.edu/openhouse</p>"}
                ]
            }
        ]

        for post_data in blog_posts:
            post = BlogPostPage(
                title=post_data["title"],
                slug=post_data["slug"],
                intro=post_data["intro"],
                date=post_data["date"],
                category=post_data["category"],
                body=json.dumps(post_data["body"])
            )
            blog_index.add_child(instance=post)
        self.stdout.write(self.style.SUCCESS('  ✓ Blog with 3 posts created'))

        # ============================================
        # 9. CONTACT PAGE
        # ============================================
        contact = ContactPage(
            title="Contact",
            slug="contact",
            intro="Have questions? Our admissions team is here to help. Contact us by phone, email, or schedule a campus visit.",
            emergency_text="For urgent student support: Call 24/7 Student Hotline"
        )
        home.add_child(instance=contact)

        # Add form fields
        FormField.objects.create(
            page=contact, sort_order=1, label="Full Name",
            field_type="singleline", required=True
        )
        FormField.objects.create(
            page=contact, sort_order=2, label="Email Address",
            field_type="email", required=True
        )
        FormField.objects.create(
            page=contact, sort_order=3, label="Phone Number",
            field_type="singleline", required=False
        )
        FormField.objects.create(
            page=contact, sort_order=4, label="Program of Interest",
            field_type="dropdown", required=False,
            choices="Computer Science,Business,Engineering,Arts,Health Sciences,Social Sciences,Undecided"
        )
        FormField.objects.create(
            page=contact, sort_order=5, label="How can we help you?",
            field_type="multiline", required=True
        )
        self.stdout.write(self.style.SUCCESS('  ✓ Contact page created with form fields'))

        # ============================================
        # 10. NAVIGATION MENU
        # ============================================
        menu, _ = Menu.objects.get_or_create(slug="main", defaults={"title": "Main Navigation"})
        menu.menu_items.all().delete()

        menu_items = [
            ("Home", "/"),
            ("About", "/about/"),
            ("Programs", "/computer-science/"),
            ("Admissions", "/admissions/"),
            ("Campus Life", "/campus-life/"),
            ("News", "/news/"),
            ("Contact", "/contact/"),
        ]
        for i, (title, url) in enumerate(menu_items):
            MenuItem.objects.create(menu=menu, link_title=title, link_url=url, sort_order=i)

        self.stdout.write(self.style.SUCCESS('  ✓ Navigation menu created'))

        # ============================================
        # 11. SITE SETTINGS
        # ============================================
        if site:
            settings, _ = SiteSettings.objects.get_or_create(site=site)
            settings.site_name = "EduVerse Academy"
            settings.phone_number = "1-800-EDU-VERSE"
            settings.email_address = "admissions@eduverse.edu"
            settings.header_cta_text = "Apply Now"
            settings.header_cta_link = "/admissions/"
            settings.announcement_text = "Spring Enrollment Now Open - Apply by March 31st for Fall 2026!"
            settings.announcement_link = "/admissions/"
            settings.announcement_link_text = "Apply Today"
            settings.emergency_badge_text = "24/7 Student Support"
            settings.emergency_phone = "1-800-HELP-NOW"
            settings.address = "1000 University Drive\nSpringfield, MA 01101"
            
            # Dynamic labels
            settings.services_tag = "Our Programs"
            settings.blog_tag = "News & Events"
            settings.testimonials_tag = "Student Voices"
            settings.faq_tag = "Admissions FAQs"
            settings.gallery_tag = "Campus Gallery"
            settings.process_tag = "Application Process"
            settings.partners_tag = "Accredited & Recognized"
            settings.read_more_label = "Learn More"
            settings.view_services_label = "Explore Program"
            settings.submit_button_label = "Submit Inquiry"
            settings.no_results_message = "No content found. Please check back soon!"
            settings.form_success_message = "Thank you! An admissions counselor will contact you within 24 hours."
            settings.emergency_contact_label = "24/7 Student Support Line"
            settings.contact_form_title = "Request Information"
            settings.call_us_label = "Call Admissions"
            settings.visit_us_label = "Visit Campus"
            
            # Footer
            settings.footer_description = "EduVerse Academy is a premier institution dedicated to fostering innovation, critical thinking, and global citizenship since 1985."
            settings.footer_copyright_text = "All rights reserved. | Excellence in Education"
            settings.footer_services_label = "Programs"
            settings.footer_company_label = "About"
            settings.footer_contact_label = "Contact"
            
            # Icons
            settings.announcement_icon = "fa-graduation-cap"
            settings.emergency_icon = "fa-phone-volume"
            settings.phone_icon = "fa-phone"
            settings.email_icon = "fa-envelope"
            settings.location_icon = "fa-location-dot"
            settings.menu_icon = "fa-bars"
            
            settings.save()
            self.stdout.write(self.style.SUCCESS('  ✓ Site settings configured'))

        self.stdout.write(self.style.SUCCESS('\n[SUCCESS] Educational Institution website seeded.'))
        self.stdout.write('  📄 Pages: Home, About, 6 Programs, Admissions, Campus, News (3 posts), Contact')
        self.stdout.write('  🧱 Blocks used: CarouselHero, TrustBar, About, Services, WhyChooseUs, ProcessSteps,')
        self.stdout.write('                 Testimonials, LeadForm, FAQ')
        self.stdout.write('  🌐 Visit: http://localhost:8000/')
