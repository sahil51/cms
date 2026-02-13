from django.urls import path
from django.utils.translation import gettext_lazy as _
from wagtail import hooks
from wagtail.admin.menu import MenuItem
from .views import theme_customizer

@hooks.register('register_admin_urls')
def register_customizer_urls():
    return [
        path('customizer/', theme_customizer, name='theme_customizer'),
    ]

@hooks.register('register_admin_menu_item')
def register_customizer_menu_item():
    return MenuItem(
        _('Visual Customizer'),
        '/admin/customizer/',
        icon_name='palette',
        order=100
    )
