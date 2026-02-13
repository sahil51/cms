from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.documents.blocks import DocumentChooserBlock

class BaseBlock(blocks.StructBlock):
    variant = blocks.ChoiceBlock(choices=[
        ('v1', 'Variant 1'),
        ('v2', 'Variant 2'),
        ('v3', 'Variant 3'),
    ], default='v1', help_text="Select the layout variant for this block.")
    
    animation = blocks.ChoiceBlock(choices=[
        ('none', 'None'),
        ('fade-up', 'Fade Up'),
        ('fade-down', 'Fade Down'),
        ('fade-left', 'Fade Left'),
        ('fade-right', 'Fade Right'),
        ('zoom-in', 'Zoom In'),
    ], default='fade-up', help_text="Select the AOS animation effect.")

    section_id = blocks.CharBlock(
        required=False, help_text="Optional HTML id for anchor links (e.g. 'services')")
    
    visible = blocks.BooleanBlock(
        required=False, default=True, help_text="Toggle this section ON/OFF")

    def get_template(self, value, context=None):
        from django.template.loader import select_template
        from pages.models import ThemeSettings
        
        request = context.get('request') if context else None
        site = getattr(request, 'site', None) if request else None
        
        if not site:
            from wagtail.models import Site
            site = Site.objects.get(is_default_site=True)

        config = ThemeSettings.for_site(site)

        theme = config.base_theme if config else 'modern'
        block_name = getattr(self.meta, 'block_name', 'default')
        
        config_variant = getattr(config, f"{block_name}_variant", 'v1') if config else 'v1'
        variant = value.get('variant', config_variant)
        if variant == 'v1' and config_variant != 'v1':
            variant = config_variant
            
        templates = [
            f"themes/{theme}/blocks/{block_name}/{variant}.html",
            f"themes/{theme}/blocks/{block_name}/v1.html",
            f"themes/modern/blocks/{block_name}/v1.html",
        ]
        
        import os
        from django.conf import settings
        
        for t in templates:
            for template_dir in settings.TEMPLATES[0]['DIRS']:
                if os.path.exists(os.path.join(template_dir, t)):
                    return t
        
        return templates[0]

    class Meta:
        abstract = True

# ==============================================
# HERO SYSTEM
# ==============================================

class HeroBlock(BaseBlock):
    title = blocks.CharBlock(required=True)
    subtitle = blocks.TextBlock(required=False)
    image = ImageChooserBlock(required=False, help_text="Background hero image (1920x900)")
    background_video_url = blocks.URLBlock(required=False, help_text="Optional background video URL")
    overlay = blocks.BooleanBlock(required=False, default=True, help_text="Dark overlay on background")
    badge_text = blocks.CharBlock(required=False, help_text="Optional badge e.g. '24/7 Monitoring'")
    cta_text = blocks.CharBlock(required=False, label="Primary CTA Text")
    cta_link = blocks.URLBlock(required=False, label="Primary CTA Link")
    secondary_cta_text = blocks.CharBlock(required=False, label="Secondary CTA Text")
    secondary_cta_link = blocks.CharBlock(required=False, label="Secondary CTA Link (e.g. tel:123)")

    class Meta:
        block_name = "hero"
        icon = "title"
        label = "Hero Section"

class HeroSlideBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=True)
    subtitle = blocks.TextBlock(required=False)
    image = ImageChooserBlock(required=False, help_text="Slide background (1920x900)")
    background_video_url = blocks.URLBlock(required=False)
    overlay = blocks.BooleanBlock(required=False, default=True)
    badge_text = blocks.CharBlock(required=False)
    cta_text = blocks.CharBlock(required=False)
    cta_link = blocks.URLBlock(required=False)
    secondary_cta_text = blocks.CharBlock(required=False)
    secondary_cta_link = blocks.CharBlock(required=False)
    enabled = blocks.BooleanBlock(required=False, default=True)

    class Meta:
        icon = "image"
        label = "Hero Slide"

class CarouselHeroBlock(BaseBlock):
    slides = blocks.ListBlock(HeroSlideBlock())
    autoplay = blocks.BooleanBlock(required=False, default=True)
    autoplay_speed = blocks.IntegerBlock(default=5000, help_text="Autoplay speed in ms")
    pause_on_hover = blocks.BooleanBlock(required=False, default=True)
    show_arrows = blocks.BooleanBlock(required=False, default=True)
    show_dots = blocks.BooleanBlock(required=False, default=True)
    animation_type = blocks.ChoiceBlock(choices=[
        ('slide', 'Slide'), ('fade', 'Fade'),
    ], default='fade')
    animation_speed = blocks.IntegerBlock(default=800, help_text="Transition speed in ms")

    class Meta:
        block_name = "carousel_hero"
        icon = "image"
        label = "Carousel Hero"

# ==============================================
# CONTENT SECTIONS
# ==============================================

class AboutBlock(BaseBlock):
    title = blocks.CharBlock(required=True)
    content = blocks.RichTextBlock(required=True)
    image = ImageChooserBlock(required=False)

    class Meta:
        block_name = "about"
        icon = "user"
        label = "About Section"

class ServicesBlock(BaseBlock):
    title = blocks.CharBlock(required=True)
    subtitle = blocks.TextBlock(required=False)
    services = blocks.ListBlock(blocks.StructBlock([
        ('icon', blocks.CharBlock(required=False, help_text="FontAwesome icon class e.g. 'fa-shield-halved'")),
        ('image', ImageChooserBlock(required=False, help_text="Service featured image")),
        ('name', blocks.CharBlock(required=True)),
        ('description', blocks.TextBlock(required=True)),
        ('cta_text', blocks.CharBlock(required=False, default="Learn More")),
        ('link', blocks.URLBlock(required=False)),
    ]))

    class Meta:
        block_name = "services"
        icon = "list-ul"
        label = "Services Grid"

class WhyChooseUsBlock(BaseBlock):
    title = blocks.CharBlock(required=True)
    subtitle = blocks.TextBlock(required=False)
    image = ImageChooserBlock(required=False, help_text="Side image")
    reasons = blocks.ListBlock(blocks.StructBlock([
        ('icon', blocks.CharBlock(required=False, help_text="FontAwesome icon class")),
        ('title', blocks.CharBlock(required=True)),
        ('description', blocks.TextBlock(required=True)),
    ]))
    cta_text = blocks.CharBlock(required=False)
    cta_link = blocks.URLBlock(required=False)

    class Meta:
        block_name = "why_choose_us"
        icon = "tick-inverse"
        label = "Why Choose Us"

class IndustriesBlock(BaseBlock):
    title = blocks.CharBlock(required=True)
    subtitle = blocks.TextBlock(required=False)
    industries = blocks.ListBlock(blocks.StructBlock([
        ('icon', blocks.CharBlock(required=False)),
        ('name', blocks.CharBlock(required=True)),
        ('image', ImageChooserBlock(required=False)),
    ]))

    class Meta:
        block_name = "industries"
        icon = "globe"
        label = "Industries We Serve"

class ProcessStepsBlock(BaseBlock):
    title = blocks.CharBlock(required=True)
    subtitle = blocks.TextBlock(required=False)
    steps = blocks.ListBlock(blocks.StructBlock([
        ('icon', blocks.CharBlock(required=False)),
        ('title', blocks.CharBlock(required=True)),
        ('description', blocks.TextBlock(required=True)),
    ]))

    class Meta:
        block_name = "process_steps"
        icon = "order"
        label = "Process Steps"

class TrustBarBlock(BaseBlock):
    title = blocks.CharBlock(required=False, default="Trusted By")
    logos = blocks.ListBlock(blocks.StructBlock([
        ('name', blocks.CharBlock(required=True)),
        ('logo', ImageChooserBlock(required=True)),
        ('link', blocks.URLBlock(required=False)),
    ]))

    class Meta:
        block_name = "trust_bar"
        icon = "group"
        label = "Trust / Certification Bar"

# ==============================================
# SOCIAL PROOF
# ==============================================

class TestimonialsBlock(BaseBlock):
    title = blocks.CharBlock(required=True)
    testimonials = blocks.ListBlock(blocks.StructBlock([
        ('quote', blocks.TextBlock(required=True)),
        ('author', blocks.CharBlock(required=True)),
        ('role', blocks.CharBlock(required=False)),
        ('location', blocks.CharBlock(required=False)),
        ('rating', blocks.IntegerBlock(required=False, min_value=1, max_value=5, default=5)),
        ('image', ImageChooserBlock(required=False, help_text="Avatar")),
    ]))

    class Meta:
        block_name = "testimonials"
        icon = "openquote"
        label = "Testimonials"

class SuccessStoryBlock(BaseBlock):
    title = blocks.CharBlock(required=True)
    stories = blocks.ListBlock(blocks.StructBlock([
        ('client_name', blocks.CharBlock(required=True)),
        ('story_title', blocks.CharBlock(required=True)),
        ('summary', blocks.TextBlock(required=True)),
        ('image', ImageChooserBlock(required=False)),
        ('link', blocks.URLBlock(required=False)),
    ]))

    class Meta:
        block_name = "success_story"
        icon = "success"
        label = "Success Stories"

class PartnerBlock(BaseBlock):
    title = blocks.CharBlock(required=True)
    partners = blocks.ListBlock(blocks.StructBlock([
        ('name', blocks.CharBlock(required=True)),
        ('logo', ImageChooserBlock(required=True)),
        ('link', blocks.URLBlock(required=False)),
    ]))

    class Meta:
        block_name = "partners"
        icon = "group"
        label = "Partners"

# ==============================================
# CTA & CONVERSION BLOCKS
# ==============================================

class CTABlock(BaseBlock):
    title = blocks.CharBlock(required=True)
    subtitle = blocks.TextBlock(required=False)
    background_image = ImageChooserBlock(required=False)
    icon = blocks.CharBlock(required=False, help_text="FontAwesome icon class")
    button_text = blocks.CharBlock(required=True)
    button_link = blocks.URLBlock(required=True)

    class Meta:
        block_name = "cta"
        icon = "bullhorn"
        label = "CTA Banner"

class FinalCTABlock(BaseBlock):
    title = blocks.CharBlock(required=True)
    subtitle = blocks.TextBlock(required=False)
    background_image = ImageChooserBlock(required=False)
    primary_cta_text = blocks.CharBlock(required=True)
    primary_cta_link = blocks.URLBlock(required=True)
    secondary_cta_text = blocks.CharBlock(required=False)
    secondary_cta_link = blocks.URLBlock(required=False)

    class Meta:
        block_name = "final_cta"
        icon = "pick"
        label = "Final Conversion Block"

class LeadFormBlock(BaseBlock):
    title = blocks.CharBlock(required=True)
    subtitle = blocks.TextBlock(required=False)
    form_action = blocks.URLBlock(required=False, help_text="Form submit URL")
    success_message = blocks.CharBlock(
        required=False, default="Thank you! We'll be in touch shortly.")
    fields = blocks.ListBlock(blocks.StructBlock([
        ('label', blocks.CharBlock(required=True)),
        ('field_type', blocks.ChoiceBlock(choices=[
            ('text', 'Text'), ('email', 'Email'), ('tel', 'Phone'),
            ('textarea', 'Textarea'), ('select', 'Dropdown'),
        ])),
        ('required', blocks.BooleanBlock(required=False, default=True)),
        ('placeholder', blocks.CharBlock(required=False)),
    ]))

    class Meta:
        block_name = "lead_form"
        icon = "mail"
        label = "Lead Capture Form"

class LeadMagnetBlock(BaseBlock):
    title = blocks.CharBlock(required=True)
    subtitle = blocks.TextBlock(required=False)
    offer_text = blocks.CharBlock(required=True, help_text="e.g. Download Free Guide")
    form_action = blocks.URLBlock(required=False)
    image = ImageChooserBlock(required=False)

    class Meta:
        block_name = "lead_magnet"
        icon = "pick"
        label = "Lead Magnet"

# ==============================================
# FAQ & CONTENT
# ==============================================

class FAQBlock(BaseBlock):
    title = blocks.CharBlock(required=True)
    enable_schema = blocks.BooleanBlock(
        required=False, default=True, help_text="Output FAQ Schema.org structured data")
    items = blocks.ListBlock(blocks.StructBlock([
        ('question', blocks.CharBlock(required=True)),
        ('answer', blocks.RichTextBlock(required=True)),
    ]))

    class Meta:
        block_name = "faq"
        icon = "help"
        label = "FAQ Accordion"

class GalleryBlock(BaseBlock):
    title = blocks.CharBlock(required=True)
    images = blocks.ListBlock(ImageChooserBlock())

    class Meta:
        block_name = "gallery"
        icon = "image"
        label = "Gallery"

class DocumentBlock(BaseBlock):
    title = blocks.CharBlock(required=True)
    document = DocumentChooserBlock(required=True)

    class Meta:
        block_name = "document"
        icon = "doc-full"
        label = "Document Download"
