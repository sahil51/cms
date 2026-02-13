from django.urls import path
from wagtail import hooks
from wagtail.admin.menu import MenuItem
from django.urls import reverse

from .views import ai_generate_view, export_static_site
from .api import get_page_sections

@hooks.register('register_admin_urls')
def register_admin_urls():
    import logging
    logger = logging.getLogger(__name__)
    logger.info("Registering AI Admin URLs")
    return [
        path('ai-generate/', ai_generate_view, name='ai_generate'),
        path('ai-generate/export-static/', export_static_site, name='ai_static_export'),
        path('ai-generate/api/sections/<int:page_id>/', get_page_sections, name='ai_get_page_sections'),
    ]

@hooks.register('register_admin_menu_item')
def register_admin_menu_item():
    return MenuItem(
        'AI Theme Generator',
        reverse('ai_generate'),
        icon_name='magic',
        order=1000
    )
