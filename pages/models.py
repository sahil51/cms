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
    LeadMagnetBlock, SuccessStoryBlock, PartnerBlock
)

@register_snippet
class ThemeConfig(models.Model):
    THEME_CHOICES = [
        ('modern', 'Modern'),
        ('minimal', 'Minimal'),
        ('bold', 'Bold'),
    ]
    
    base_theme = models.CharField(max_length=20, choices=THEME_CHOICES, default='modern')
    
    # Block Variants
    hero_variant = models.CharField(max_length=10, default='v1')
    about_variant = models.CharField(max_length=10, default='v1')
    services_variant = models.CharField(max_length=10, default='v1')
    faq_variant = models.CharField(max_length=10, default='v1')
    
    primary_color = models.CharField(max_length=7, default='#6C63FF')
    secondary_color = models.CharField(max_length=7, default='#FF6584')
    background_color = models.CharField(max_length=7, default='#0F172A')
    text_color = models.CharField(max_length=7, default='#FFFFFF')
    
    heading_font = models.CharField(max_length=100, default='Poppins')
    body_font = models.CharField(max_length=100, default='Inter')
    
    animation_preset = models.CharField(max_length=50, default='smooth-fade')
    
    # AI state for auditing/history
    last_ai_prompt = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name = "Theme Configuration"
        verbose_name_plural = "Theme Configuration"

    def __str__(self):
        return f"Theme Config ({self.base_theme})"

class ContentPage(Page):
    body = StreamField([
        ('hero', HeroBlock()),
        ('about', AboutBlock()),
        ('services', ServicesBlock()),
        ('faq', FAQBlock()),
        ('testimonials', TestimonialsBlock()),
        ('cta', CTABlock()),
        ('gallery', GalleryBlock()),
        ('document', DocumentBlock()),
        ('lead_magnet', LeadMagnetBlock()),
        ('success_story', SuccessStoryBlock()),
        ('partners', PartnerBlock()),
    ], use_json_field=True)

    content_panels = Page.content_panels + [
        FieldPanel('body'),
    ]

    search_fields = Page.search_fields + [
        index.SearchField('body'),
    ]

    class Meta:
        verbose_name = "Content Page"

@register_setting
class SiteSettings(BaseSiteSetting):
    logo = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    phone_number = models.CharField(max_length=20, blank=True)
    email_address = models.EmailField(blank=True)
    
    # Social Media
    facebook_url = models.URLField(blank=True, help_text="Facebook page URL")
    twitter_url = models.URLField(blank=True, help_text="Twitter profile URL")
    instagram_url = models.URLField(blank=True, help_text="Instagram profile URL")
    linkedin_url = models.URLField(blank=True, help_text="LinkedIn profile URL")

    panels = [
        MultiFieldPanel([
            FieldPanel('logo'),
            FieldPanel('phone_number'),
            FieldPanel('email_address'),
        ], heading="Business Information"),
        MultiFieldPanel([
            FieldPanel('facebook_url'),
            FieldPanel('twitter_url'),
            FieldPanel('instagram_url'),
            FieldPanel('linkedin_url'),
        ], heading="Social Media Links"),
    ]

# --- Form Builder ---

class FormField(AbstractFormField):
    page = ParentalKey('ContactPage', on_delete=models.CASCADE, related_name='form_fields')

class ContactPage(AbstractEmailForm):
    intro = StreamField([
        ('hero', HeroBlock()),
    ], use_json_field=True, blank=True)
    thank_you_text = models.TextField(blank=True)

    address = models.TextField(blank=True, help_text="Physical address for the map section")
    phone_cta = models.CharField(max_length=20, blank=True, help_text="Phone number for 'Call Now' CTA")
    map_embed_url = models.URLField(blank=True, help_text="Google Maps Embed URL")

    content_panels = AbstractEmailForm.content_panels + [
        FieldPanel('intro'),
        InlinePanel('form_fields', label="Form fields"),
        FieldPanel('thank_you_text'),
        MultiFieldPanel([
            FieldPanel('address'),
            FieldPanel('phone_cta'),
            FieldPanel('map_embed_url'),
        ], heading="Blueprint Contact Info"),
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
        verbose_name = "Contact Page"

# --- Blog System ---

class BlogIndexPage(Page):
    intro = models.TextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
    ]

    def get_template(self, request, *args, **kwargs):
        config = ThemeConfig.objects.first()
        theme = config.base_theme if config else 'modern'
        return f"themes/{theme}/pages/blog_index_page.html"

    def get_context(self, request):
        context = super().get_context(request)
        blogposts = self.get_children().live().order_by('-first_published_at')
        context['blogposts'] = blogposts
        return context

class BlogPostPage(Page):
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250)
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
        FieldPanel('date'),
        FieldPanel('intro'),
        FieldPanel('body'),
    ]

    def get_template(self, request, *args, **kwargs):
        config = ThemeConfig.objects.first()
        theme = config.base_theme if config else 'modern'
        return f"themes/{theme}/pages/blog_post_page.html"

# --- Service Area System ---

class ServiceAreaIndexPage(Page):
    intro = models.TextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
    ]

    def get_template(self, request, *args, **kwargs):
        config = ThemeConfig.objects.first()
        theme = config.base_theme if config else 'modern'
        return f"themes/{theme}/pages/service_area_index_page.html"

class ServiceAreaPage(Page):
    location_name = models.CharField(max_length=100)
    body = StreamField([
        ('hero', HeroBlock()),
        ('services', ServicesBlock()),
        ('success_stories', SuccessStoryBlock()),
        ('cta', CTABlock()),
    ], use_json_field=True)

    content_panels = Page.content_panels + [
        FieldPanel('location_name'),
        FieldPanel('body'),
    ]

    def get_template(self, request, *args, **kwargs):
        config = ThemeConfig.objects.first()
        theme = config.base_theme if config else 'modern'
        return f"themes/{theme}/pages/service_area_page.html"

# --- Dynamic Menus ---

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
        null=True,
        blank=True,
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
