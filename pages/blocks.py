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

    def get_template(self, value, context=None):
        from django.template.loader import select_template
        from pages.models import ThemeConfig
        
        config = ThemeConfig.objects.first()
        theme = config.base_theme if config else 'modern'
        block_name = getattr(self.meta, 'block_name', 'default')
        
        # Determine preferred variant
        config_variant = getattr(config, f"{block_name}_variant", 'v1') if config else 'v1'
        variant = value.get('variant', config_variant)
        if variant == 'v1' and config_variant != 'v1':
            variant = config_variant
            
        templates = [
            f"themes/{theme}/blocks/{block_name}/{variant}.html",
            f"themes/{theme}/blocks/{block_name}/v1.html",
            f"themes/modern/blocks/{block_name}/v1.html",  # Global fallback
        ]
        
        # Django's select_template will return the first one that exists
        # But for Wagtail's get_template, we just return the string.
        # However, to be extra safe, we'll check existence here.
        import os
        from django.conf import settings
        
        for t in templates:
            for template_dir in settings.TEMPLATES[0]['DIRS']:
                if os.path.exists(os.path.join(template_dir, t)):
                    return t
        
        return templates[0] # Fallback to original intent if logic fails

    class Meta:
        abstract = True

class HeroBlock(BaseBlock):
    title = blocks.CharBlock(required=True)
    subtitle = blocks.TextBlock(required=False)
    image = ImageChooserBlock(required=False)
    cta_text = blocks.CharBlock(required=False, label="Primary CTA Text")
    cta_link = blocks.URLBlock(required=False, label="Primary CTA Link")
    secondary_cta_text = blocks.CharBlock(required=False, label="Secondary CTA Text (e.g. Call Us)")
    secondary_cta_link = blocks.CharBlock(required=False, label="Secondary CTA Link (e.g. tel:123)")

    class Meta:
        block_name = "hero"
        icon = "title"

class AboutBlock(BaseBlock):
    title = blocks.CharBlock(required=True)
    content = blocks.RichTextBlock(required=True)
    image = ImageChooserBlock(required=False)

    class Meta:
        block_name = "about"
        icon = "user"

class ServicesBlock(BaseBlock):
    title = blocks.CharBlock(required=True)
    services = blocks.ListBlock(blocks.StructBlock([
        ('icon', blocks.CharBlock(required=False, help_text="Icon name (e.g. from FontAwesome)")),
        ('name', blocks.CharBlock(required=True)),
        ('description', blocks.TextBlock(required=True)),
        ('cta_text', blocks.CharBlock(required=False, default="Learn More")),
        ('link', blocks.URLBlock(required=False)),
    ]))

    class Meta:
        block_name = "services"
        icon = "list-ul"

class FAQBlock(BaseBlock):
    title = blocks.CharBlock(required=True)
    items = blocks.ListBlock(blocks.StructBlock([
        ('question', blocks.CharBlock(required=True)),
        ('answer', blocks.RichTextBlock(required=True)),
    ]))

    class Meta:
        block_name = "faq"
        icon = "help"

class TestimonialsBlock(BaseBlock):
    title = blocks.CharBlock(required=True)
    testimonials = blocks.ListBlock(blocks.StructBlock([
        ('quote', blocks.TextBlock(required=True)),
        ('author', blocks.CharBlock(required=True)),
        ('role', blocks.CharBlock(required=False)),
        ('image', ImageChooserBlock(required=False)),
    ]))

    class Meta:
        block_name = "testimonials"
        icon = "comment"

class CTABlock(BaseBlock):
    title = blocks.CharBlock(required=True)
    subtitle = blocks.TextBlock(required=False)
    button_text = blocks.CharBlock(required=True)
    button_link = blocks.URLBlock(required=True)

    class Meta:
        block_name = "cta"
        icon = "bullhorn"

class GalleryBlock(BaseBlock):
    title = blocks.CharBlock(required=True)
    images = blocks.ListBlock(ImageChooserBlock())

    class Meta:
        block_name = "gallery"
        icon = "image"

class DocumentBlock(BaseBlock):
    title = blocks.CharBlock(required=True)
    document = DocumentChooserBlock(required=True)

    class Meta:
        block_name = "document"
        icon = "doc-full"

class LeadMagnetBlock(BaseBlock):
    title = blocks.CharBlock(required=True)
    subtitle = blocks.TextBlock(required=False)
    offer_text = blocks.CharBlock(required=True, help_text="e.g. Download Free Guide")
    form_action = blocks.URLBlock(required=False)
    image = ImageChooserBlock(required=False)

    class Meta:
        block_name = "lead_magnet"
        icon = "pick"

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
