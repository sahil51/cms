from django.db import models
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail import blocks
from wagtail.models import Page, Orderable
from wagtail.fields import StreamField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.snippets.models import register_snippet
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.search import index

from wagtail.images.blocks import ImageChooserBlock
from wagtail.documents.blocks import DocumentChooserBlock

from .blocks import (
    HeroBlock, AboutBlock, ServicesBlock, FAQBlock, 
    TestimonialsBlock, CTABlock, GalleryBlock, DocumentBlock,
    LeadMagnetBlock, SuccessStoryBlock, PartnerBlock,
    CarouselHeroBlock, WhyChooseUsBlock, IndustriesBlock,
    ProcessStepsBlock, TrustBarBlock, LeadFormBlock, FinalCTABlock
)

# ==============================================
# THEME CONFIGURATION
# ==============================================

@register_setting
class ThemeSettings(BaseSiteSetting):
    THEME_CHOICES = [
        ('corporate', 'Corporate'),
        ('creative', 'Creative'),
        ('saas', 'SaaS'),
        ('editorial', 'Editorial'),
    ]
    
    base_theme = models.CharField(max_length=20, choices=THEME_CHOICES, default='corporate')
    
    # Block Variants
    hero_variant = models.CharField(max_length=10, default='v1')
    about_variant = models.CharField(max_length=10, default='v1')
    services_variant = models.CharField(max_length=10, default='v1')
    faq_variant = models.CharField(max_length=10, default='v1')
    
    primary_color = models.CharField(max_length=7, default='#00D4FF')
    secondary_color = models.CharField(max_length=7, default='#FF6B35')
    background_color = models.CharField(max_length=7, default='#0A0E17')
    text_color = models.CharField(max_length=7, default='#FFFFFF')
    
    heading_font = models.CharField(max_length=100, default='Inter')
    body_font = models.CharField(max_length=100, default='Inter')
    
    animation_preset = models.CharField(max_length=50, default='smooth-fade')
    
    logo = models.ForeignKey(
        'wagtailimages.Image',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name="Site Logo"
    )
    site_name = models.CharField(max_length=100, blank=True, default="SecureGuard Pro")
    
    hero_bg_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name="Hero Background Image"
    )
    hero_video_url = models.URLField(
        blank=True, 
        null=True, 
        help_text="Direct link to MP4 or YouTube/Vimeo URL",
        verbose_name="Hero Background Video"
    )
    
    last_ai_prompt = models.TextField(blank=True, null=True)
    
    panels = [
        MultiFieldPanel([
            FieldPanel('logo'),
            FieldPanel('site_name'),
        ], heading="Branding"),
        MultiFieldPanel([
            FieldPanel('base_theme'),
            FieldPanel('animation_preset'),
        ], heading="Theme Layout"),
        MultiFieldPanel([
            FieldPanel('hero_bg_image'),
            FieldPanel('hero_video_url'),
        ], heading="Hero Media"),
        MultiFieldPanel([
            FieldPanel('primary_color'),
            FieldPanel('secondary_color'),
            FieldPanel('background_color'),
            FieldPanel('text_color'),
        ], heading="Colors"),
        MultiFieldPanel([
            FieldPanel('heading_font'),
            FieldPanel('body_font'),
        ], heading="Typography"),
    ]

    def __str__(self):
        return f"Theme Settings for {self.site}"

# ==============================================
# SITE SETTINGS (Global Header/Footer/SEO)
# ==============================================

@register_setting
class SiteSettings(BaseSiteSetting):
    logo = models.ForeignKey(
        'wagtailimages.Image',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    # Logo & Branding
    site_name = models.CharField(max_length=100, blank=True, default="SecureGuard Pro")
    logo_split_index = models.PositiveIntegerField(
        default=6, 
        help_text="Number of characters to style with the primary color (e.g. 6 for 'Secure' in 'SecureGuard')"
    )
    
    # Global Section Tags
    services_tag = models.CharField(max_length=50, blank=True, default="Our Services")
    blog_tag = models.CharField(max_length=50, blank=True, default="Latest News")
    areas_tag = models.CharField(max_length=50, blank=True, default="Service Areas")
    testimonials_tag = models.CharField(max_length=50, blank=True, default="Testimonials")
    faq_tag = models.CharField(max_length=50, blank=True, default="FAQ")
    gallery_tag = models.CharField(max_length=50, blank=True, default="Project Gallery")
    process_tag = models.CharField(max_length=50, blank=True, default="Our Process")
    industries_tag = models.CharField(max_length=50, blank=True, default="Industries We Serve")
    partners_tag = models.CharField(max_length=50, blank=True, default="Our Partners")
    success_stories_tag = models.CharField(max_length=50, blank=True, default="Success Stories")
    
    # Global Link & Action Labels
    read_more_label = models.CharField(max_length=50, blank=True, default="Read Article")
    view_services_label = models.CharField(max_length=50, blank=True, default="View Services")
    share_label = models.CharField(max_length=50, blank=True, default="Share this article:")
    submit_button_label = models.CharField(max_length=50, blank=True, default="Submit Now")
    no_results_message = models.CharField(max_length=255, blank=True, default="No items found. Please check back later.")
    form_success_message = models.CharField(max_length=255, blank=True, default="Thank you! Your message has been sent successfully.")
    
    # Global Contact Labels
    emergency_contact_label = models.CharField(max_length=50, blank=True, default="Emergency Contact")
    contact_form_title = models.CharField(max_length=100, blank=True, default="Send Us a Message")
    call_us_label = models.CharField(max_length=50, blank=True, default="Call Us")
    visit_us_label = models.CharField(max_length=50, blank=True, default="Visit Us")

    phone_number = models.CharField(max_length=20, blank=True)
    email_address = models.EmailField(blank=True)
    
    # Header CTA
    header_cta_text = models.CharField(max_length=50, blank=True, default="Get Free Quote")
    header_cta_link = models.URLField(blank=True, default="/contact/")
    
    # Announcement Bar
    announcement_text = models.CharField(
        max_length=200, blank=True,
        help_text="Top announcement bar text. Leave empty to hide.")
    announcement_link = models.URLField(blank=True)
    announcement_link_text = models.CharField(max_length=50, blank=True, default="Learn More")
    
    # Emergency Badge
    emergency_badge_text = models.CharField(
        max_length=50, blank=True, default="24/7 Emergency",
        help_text="Emergency badge in header. Leave empty to hide.")
    emergency_phone = models.CharField(max_length=20, blank=True)
    
    # Address
    address = models.TextField(blank=True)
    
    # Footer Content
    footer_description = models.TextField(
        blank=True, 
        default="Professional security solutions for homes and businesses. CCTV, alarm systems, access control, and 24/7 monitoring services you can trust.",
        help_text="Description shown in the footer"
    )
    footer_copyright_text = models.CharField(
        max_length=255, 
        blank=True, 
        default="All rights reserved. | Professional Security Solutions",
        help_text="Copyright suffix text"
    )
    
    # Footer Labels
    footer_services_label = models.CharField(max_length=50, default="Services", blank=True)
    footer_company_label = models.CharField(max_length=50, default="Company", blank=True)
    footer_contact_label = models.CharField(max_length=50, default="Contact Info", blank=True)

    # Social Media
    facebook_url = models.URLField(blank=True)
    # Branding & Icons
    favicon = models.ForeignKey(
        'wagtailimages.Image',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text="Site favicon (PNG or ICO)"
    )
    announcement_icon = models.CharField(max_length=50, blank=True, default="fa-bell")
    emergency_icon = models.CharField(max_length=50, blank=True, default="fa-shield-halved")
    phone_icon = models.CharField(max_length=50, blank=True, default="fa-phone")
    email_icon = models.CharField(max_length=50, blank=True, default="fa-envelope")
    location_icon = models.CharField(max_length=50, blank=True, default="fa-location-dot")
    menu_icon = models.CharField(max_length=50, blank=True, default="fa-bars")

    twitter_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)

    # SEO Defaults
    default_og_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text="Default Open Graph image when pages don't have one"
    )

    panels = [
        MultiFieldPanel([
            FieldPanel('favicon'),
            FieldPanel('announcement_icon'),
            FieldPanel('emergency_icon'),
            FieldPanel('phone_icon'),
            FieldPanel('email_icon'),
            FieldPanel('location_icon'),
            FieldPanel('menu_icon'),
        ], heading="Global Icons & Favicon"),
        MultiFieldPanel([
            FieldPanel('logo'),
            FieldPanel('site_name'),
            FieldPanel('logo_split_index'),
            FieldPanel('phone_number'),
            FieldPanel('email_address'),
            FieldPanel('address'),
        ], heading="Business Information"),
        MultiFieldPanel([
            FieldPanel('services_tag'),
            FieldPanel('blog_tag'),
            FieldPanel('areas_tag'),
            FieldPanel('testimonials_tag'),
            FieldPanel('faq_tag'),
            FieldPanel('gallery_tag'),
            FieldPanel('process_tag'),
            FieldPanel('industries_tag'),
            FieldPanel('partners_tag'),
            FieldPanel('success_stories_tag'),
        ], heading="Global Section Tags"),
        MultiFieldPanel([
            FieldPanel('read_more_label'),
            FieldPanel('view_services_label'),
            FieldPanel('share_label'),
            FieldPanel('submit_button_label'),
            FieldPanel('no_results_message'),
            FieldPanel('form_success_message'),
        ], heading="Global Link & Action Labels"),
        MultiFieldPanel([
            FieldPanel('emergency_contact_label'),
            FieldPanel('contact_form_title'),
            FieldPanel('call_us_label'),
            FieldPanel('visit_us_label'),
        ], heading="Contact Labels"),
        MultiFieldPanel([
            FieldPanel('header_cta_text'),
            FieldPanel('header_cta_link'),
        ], heading="Header CTA Button"),
        MultiFieldPanel([
            FieldPanel('announcement_text'),
            FieldPanel('announcement_link'),
            FieldPanel('announcement_link_text'),
        ], heading="Announcement Bar"),
        MultiFieldPanel([
            FieldPanel('emergency_badge_text'),
            FieldPanel('emergency_phone'),
        ], heading="Emergency Badge"),
        MultiFieldPanel([
            FieldPanel('footer_description'),
            FieldPanel('footer_copyright_text'),
            FieldPanel('footer_services_label'),
            FieldPanel('footer_company_label'),
            FieldPanel('footer_contact_label'),
        ], heading="Footer Content"),
        MultiFieldPanel([
            FieldPanel('facebook_url'),
            FieldPanel('twitter_url'),
            FieldPanel('instagram_url'),
            FieldPanel('linkedin_url'),
            FieldPanel('youtube_url'),
        ], heading="Social Media Links"),
        MultiFieldPanel([
            FieldPanel('default_og_image'),
        ], heading="SEO Defaults"),
    ]

# ==============================================
# CONTENT PAGE (Main StreamField Page)
# ==============================================

ALL_BLOCKS = [
    ('hero', HeroBlock()),
    ('carousel_hero', CarouselHeroBlock()),
    ('about', AboutBlock()),
    ('services', ServicesBlock()),
    ('why_choose_us', WhyChooseUsBlock()),
    ('industries', IndustriesBlock()),
    ('process_steps', ProcessStepsBlock()),
    ('trust_bar', TrustBarBlock()),
    ('testimonials', TestimonialsBlock()),
    ('success_story', SuccessStoryBlock()),
    ('partners', PartnerBlock()),
    ('faq', FAQBlock()),
    ('cta', CTABlock()),
    ('final_cta', FinalCTABlock()),
    ('lead_form', LeadFormBlock()),
    ('lead_magnet', LeadMagnetBlock()),
    ('gallery', GalleryBlock()),
    ('document', DocumentBlock()),
]

class ContentPage(Page):
    page_description = "Standard page with modular sections (StreamField) for custom layouts."
    body = StreamField(ALL_BLOCKS, use_json_field=True)

    content_panels = Page.content_panels + [
        FieldPanel('body'),
    ]

    search_fields = Page.search_fields + [
        index.SearchField('body'),
    ]

    class Meta:
        verbose_name = "01. Content Page"

    def get_template(self, request, *args, **kwargs):
        site = getattr(request, 'site', None)
        if not site:
            from wagtail.models import Site
            site = Site.objects.get(is_default_site=True)
        config = ThemeSettings.for_site(site)
        theme = config.base_theme if config else 'modern'
        return f"themes/{theme}/pages/content_page.html"

# ==============================================
# SERVICE DETAIL PAGE
# ==============================================

class ServicePage(Page):
    page_description = "Detailed page for a specific security service (e.g., CCTV, Alarms)."
    icon = models.CharField(max_length=50, blank=True, help_text="FontAwesome class e.g. fa-shield-halved")
    featured_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    intro = models.TextField(blank=True)
    
    body = StreamField(ALL_BLOCKS, use_json_field=True)

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('icon'),
            FieldPanel('featured_image'),
            FieldPanel('intro'),
        ], heading="Service Header"),
        FieldPanel('body'),
    ]

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    def get_template(self, request, *args, **kwargs):
        site = getattr(request, 'site', None)
        if not site:
            from wagtail.models import Site
            site = Site.objects.get(is_default_site=True)
        config = ThemeSettings.for_site(site)
        theme = config.base_theme if config else 'modern'
        return f"themes/{theme}/pages/service_page.html"

    class Meta:
        verbose_name = "02. Service Page"

# ==============================================
# CONTACT PAGE
# ==============================================

class FormField(AbstractFormField):
    page = ParentalKey('ContactPage', on_delete=models.CASCADE, related_name='form_fields')

class ContactPage(AbstractEmailForm):
    page_description = "Page with a contact form, address, and emergency contact details."
    intro = StreamField([
        ('hero', HeroBlock()),
    ], use_json_field=True, blank=True)
    thank_you_text = models.TextField(blank=True)

    address = models.TextField(blank=True, help_text="Physical address for the map section")
    phone_cta = models.CharField(max_length=20, blank=True, help_text="Phone number for 'Call Now' CTA")
    map_embed_url = models.URLField(blank=True, help_text="Google Maps Embed URL")
    emergency_text = models.CharField(max_length=200, blank=True, default="Need Emergency Security? Call Now!")

    content_panels = AbstractEmailForm.content_panels + [
        FieldPanel('intro'),
        InlinePanel('form_fields', label="Form fields"),
        FieldPanel('thank_you_text'),
        MultiFieldPanel([
            FieldPanel('address'),
            FieldPanel('phone_cta'),
            FieldPanel('map_embed_url'),
            FieldPanel('emergency_text'),
        ], heading="Contact Information"),
        MultiFieldPanel([
            FieldPanel('from_address'),
            FieldPanel('to_address'),
            FieldPanel('subject'),
        ], heading="Email Notification Settings"),
    ]

    search_fields = AbstractEmailForm.search_fields + [
        index.SearchField('intro'),
    ]

    class Meta:
        verbose_name = "03. Contact Page"

# ==============================================
# BLOG SYSTEM
# ==============================================

class BlogIndexPage(Page):
    intro = models.TextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
    ]

    class Meta:
        verbose_name = "04. Articles Index"

    subpage_types = ['BlogPostPage']
    page_description = "Listing page that automatically gathers and displays article posts."

    def get_template(self, request, *args, **kwargs):
        site = getattr(request, 'site', None)
        if not site:
            from wagtail.models import Site
            site = Site.objects.get(is_default_site=True)
        config = ThemeSettings.for_site(site)
        theme = config.base_theme if config else 'modern'
        return f"themes/{theme}/pages/blog_index_page.html"

    def get_context(self, request):
        context = super().get_context(request)
        # Optimization: Fetch specific BlogPostPage objects to avoid N+1 queries
        blogposts = BlogPostPage.objects.child_of(self).live().order_by('-first_published_at')
        context['blogposts'] = blogposts
        return context

class BlogPostPage(Page):
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250)
    featured_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    category = models.CharField(max_length=100, blank=True, help_text="e.g. CCTV, Access Control, Tips")
    
    body = StreamField([
        ('heading', blocks.CharBlock(form_classname="title")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
        ('cta', CTABlock()),
        ('lead_magnet', LeadMagnetBlock()),
    ], use_json_field=True)

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('date'),
            FieldPanel('category'),
            FieldPanel('featured_image'),
        ], heading="Post Meta"),
        FieldPanel('intro'),
        FieldPanel('body'),
    ]

    class Meta:
        verbose_name = "↳ Article Post"

    parent_page_types = ['BlogIndexPage']
    page_description = "Individual news article or informative security post."

    def get_template(self, request, *args, **kwargs):
        site = getattr(request, 'site', None)
        if not site:
            from wagtail.models import Site
            site = Site.objects.get(is_default_site=True)
        config = ThemeSettings.for_site(site)
        theme = config.base_theme if config else 'modern'
        return f"themes/{theme}/pages/blog_post_page.html"

# ==============================================
# SERVICE AREA SYSTEM
# ==============================================

class ServiceAreaIndexPage(Page):
    intro = models.TextField(blank=True)

    def get_context(self, request):
        context = super().get_context(request)
        # Optimization: Fetch specific ServiceAreaPage objects
        areas = ServiceAreaPage.objects.child_of(self).live().order_by('title')
        context['areas'] = areas
        return context

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
    ]

    class Meta:
        verbose_name = "05. Area Index Page"

    subpage_types = ['ServiceAreaPage']
    page_description = "Index page to list all geographical regions where services are provided."

    def get_template(self, request, *args, **kwargs):
        site = getattr(request, 'site', None)
        if not site:
            from wagtail.models import Site
            site = Site.objects.get(is_default_site=True)
        config = ThemeSettings.for_site(site)
        theme = config.base_theme if config else 'modern'
        return f"themes/{theme}/pages/service_area_index_page.html"

class ServiceAreaPage(Page):
    location_name = models.CharField(max_length=100)
    body = StreamField(ALL_BLOCKS, use_json_field=True)

    content_panels = Page.content_panels + [
        FieldPanel('location_name'),
        FieldPanel('body'),
    ]

    class Meta:
        verbose_name = "↳ Area Detail Page"

    parent_page_types = ['ServiceAreaIndexPage']
    page_description = "Detailed page for a specific location or service region."

    def get_template(self, request, *args, **kwargs):
        site = getattr(request, 'site', None)
        if not site:
            from wagtail.models import Site
            site = Site.objects.get(is_default_site=True)
        config = ThemeSettings.for_site(site)
        theme = config.base_theme if config else 'modern'
        return f"themes/{theme}/pages/service_area_page.html"

# ==============================================
# DYNAMIC MENUS
# ==============================================

@register_snippet
class Menu(ClusterableModel):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)

    panels = [
        FieldPanel('title'),
        FieldPanel('slug'),
        InlinePanel('menu_items', label="Menu items")
    ]

    def __str__(self):
        return self.title

class MenuItem(Orderable):
    menu = ParentalKey(Menu, related_name='menu_items')
    link_title = models.CharField(max_length=50, blank=True, null=True)
    link_url = models.CharField(max_length=500, blank=True)
    link_page = models.ForeignKey(
        'wagtailcore.Page',
        null=True, blank=True,
        related_name='+',
        on_delete=models.CASCADE,
    )
    open_in_new_tab = models.BooleanField(default=False, blank=True)

    @property
    def link(self):
        if self.link_page:
            return self.link_page.url
        elif self.link_url:
            return self.link_url
        return '#'

    @property
    def title(self):
        if self.link_page and not self.link_title:
            return self.link_page.title
        elif self.link_title:
            return self.link_title
        return 'Missing Title'

    panels = [
        FieldPanel('link_title'),
        FieldPanel('link_url'),
        FieldPanel('link_page'),
        FieldPanel('open_in_new_tab'),
    ]
