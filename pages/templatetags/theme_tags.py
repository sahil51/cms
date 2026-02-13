from django import template
from pages.models import ThemeSettings

register = template.Library()

@register.simple_tag(takes_context=True)
def get_theme_config(context):
    """Returns the current site's ThemeSettings with fallback."""
    try:
        from wagtail.models import Site
        request = context.get('request')
        site = getattr(request, 'site', None)
        
        if not site:
            site = Site.objects.get(is_default_site=True)
            
        return ThemeSettings.for_site(site)
    except Exception:
        return None
@register.simple_tag
def get_google_fonts_url(config):
    """Generates a Google Fonts URL for the configured fonts."""
    if not config:
        return "https://fonts.googleapis.com/css2?family=Inter:wght@400;700&family=Poppins:wght@400;700&display=swap"
    
    fonts = []
    if config.heading_font:
        fonts.append(config.heading_font.replace(" ", "+") + ":wght@400;700")
    if config.body_font:
        fonts.append(config.body_font.replace(" ", "+") + ":wght@400;700")
    
    if not fonts:
        return ""
        
    family_str = "&family=".join(fonts)
    return f"https://fonts.googleapis.com/css2?family={family_str}&display=swap"

@register.simple_tag
def get_menu(slug):
    """Returns a Menu snippet by slug."""
    try:
        from pages.models import Menu
        return Menu.objects.get(slug=slug)
    except Exception:
        return None

@register.simple_tag(takes_context=True)
def get_site_settings(context):
    """Returns the current site's SiteSettings with fallback."""
    try:
        from wagtail.models import Site
        from pages.models import SiteSettings
        request = context.get('request')
        site = getattr(request, 'site', None)
        
        if not site:
            site = Site.objects.get(is_default_site=True)
            
        return SiteSettings.for_site(site)
    except Exception:
        return None
