from pages.models import SiteSettings, ThemeSettings
from wagtail.models import Site

def global_context(request):
    """
    Injects global SiteSettings and ThemeSettings into the template context.
    This replaces the need for eager loading tags in every template.
    """
    try:
        site = Site.find_for_request(request)
        if not site:
            site = Site.objects.get(is_default_site=True)
            
        return {
            'settings': SiteSettings.for_site(site),
            'config': ThemeSettings.for_site(site),
        }
    except Exception:
        # Fail silently to prevent 500 errors if site/settings are missing
        return {
            'settings': None,
            'config': None
        }
