import os
import zipfile
import tempfile
import shutil
from io import BytesIO
from django.conf import settings
from django.http import HttpRequest
from django.template.loader import render_to_string
from wagtail.models import Page, Site
from django.utils.text import slugify

class StaticSiteExporter:
    """
    Utility to render all live Wagtail pages into a portable static HTML site.
    Bundles HTML, CSS, JS, and Media into a single ZIP archive.
    """

    def __init__(self, request=None, site_id=None):
        if request:
            try:
                self.site = Site.find_for_request(request)
            except Exception:
                self.site = Site.objects.filter(is_default_site=True).first()
        elif site_id:
            self.site = Site.objects.get(id=site_id)
        else:
            self.site = Site.objects.filter(is_default_site=True).first()
            
        self.temp_dir = tempfile.mkdtemp()
        self.assets_dir = os.path.join(self.temp_dir, 'assets')
        os.makedirs(self.assets_dir, exist_ok=True)

    def _mock_request(self, path):
        """Creates a robust mock HttpRequest for rendering."""
        from django.contrib.auth.models import AnonymousUser
        from django.contrib.sessions.middleware import SessionMiddleware
        
        request = HttpRequest()
        request.path = path
        request.method = 'GET'
        request.META['SERVER_NAME'] = self.site.hostname
        request.META['SERVER_PORT'] = str(self.site.port)
        request.META['HTTP_HOST'] = f"{self.site.hostname}:{self.site.port}"
        request.site = self.site
        request.user = AnonymousUser()
        
        # Add session support if needed
        middleware = SessionMiddleware(lambda r: None)
        middleware.process_request(request)
        request.session.save()
        
        return request

    def _localize_html(self, html):
        """
        Rewrites absolute internal paths to relative ones using Regex for robustness.
        Handles static/, media/, and internal page links including fragments.
        """
        import re

        # 1. Localize Static and Media Assets
        asset_patterns = [
            (r'(src|href)=["\']/?static/(.*?)["\']', r'\1="assets/static/\2"'),
            (r'(src|href)=["\']/?media/(.*?)["\']', r'\1="assets/media/\2"'),
        ]
        
        for pattern, replacement in asset_patterns:
            html = re.sub(pattern, replacement, html)
        
        # 2. Site-wide link localization for internal pages
        live_pages = Page.objects.live().descendant_of(self.site.root_page, inclusive=True)
        # Sort by URL length descending to avoid greedy matches on short paths
        sorted_pages = sorted(live_pages, key=lambda p: len(p.url or ""), reverse=True)

        for page in sorted_pages:
            url = page.url
            if url:
                target = "index.html" if page.id == self.site.root_page_id else f"{page.slug}.html"
                
                # Match links to this page, including optional trailing slash and fragments
                url_quoted = re.escape(url.rstrip('/'))
                link_pattern = rf'href=["\']/?{url_quoted}/?(#.*?)?["\']'
                html = re.sub(link_pattern, rf'href="{target}\1"', html)
        
        # 3. Final safety net for root/fragment links
        html = re.sub(r'href=["\']/?(#.*?)?["\']', r'href="index.html\1"', html)
                
        return html

    def export(self):
        """Renders all pages and bundles assets into a ZIP buffer."""
        pages = Page.objects.live().descendant_of(self.site.root_page, inclusive=True)
        
        # 1. Render all pages using .specific
        for page in pages:
            specific_page = page.specific
            # Use the actual page URL for mocking
            request = self._mock_request(specific_page.url or '/')
            
            try:
                # Get the response from Wagtail's serve method
                response = specific_page.serve(request)
                if hasattr(response, 'render'):
                    content = response.render().content.decode('utf-8')
                else:
                    content = response.content.decode('utf-8')
                
                localized_content = self._localize_html(content)
                
                # Site root is ALWAYS index.html for static hosting
                if specific_page.id == self.site.root_page_id:
                    filename = 'index.html'
                else:
                    filename = f"{specific_page.slug or specific_page.id}.html"
                    
                filepath = os.path.join(self.temp_dir, filename)
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(localized_content)
            except Exception as e:
                import logging
                logging.getLogger(__name__).error(f"Failed to render page {specific_page.title}: {str(e)}")

        # 2. Bundle Static files (more robust collection)
        static_dest = os.path.join(self.assets_dir, 'static')
        os.makedirs(static_dest, exist_ok=True)
        
        # A: Check STATIC_ROOT
        if getattr(settings, 'STATIC_ROOT', None) and os.path.exists(settings.STATIC_ROOT):
            for item in os.listdir(settings.STATIC_ROOT):
                s = os.path.join(settings.STATIC_ROOT, item)
                d = os.path.join(static_dest, item)
                if os.path.isdir(s):
                    shutil.copytree(s, d, dirs_exist_ok=True)
                else:
                    shutil.copy2(s, d)
        
        # B: Force collect from known app/project static dirs (Crucial for dev)
        from django.contrib.staticfiles import finders
        for finder in finders.get_finders():
            for path, storage in finder.list([]):
                if storage.exists(path):
                    target_path = os.path.join(static_dest, path)
                    os.makedirs(os.path.dirname(target_path), exist_ok=True)
                    try:
                        # storage.path(path) might fail for some storages, so we use open/read
                        if not os.path.isdir(storage.path(path)):
                            shutil.copy2(storage.path(path), target_path)
                    except (AttributeError, NotImplementedError):
                        # Fallback for non-file storage (unlikely here but safe)
                        with storage.open(path) as source_file:
                            with open(target_path, 'wb') as dest_file:
                                dest_file.write(source_file.read())

        # 3. Bundle Media files
        media_dest = os.path.join(self.assets_dir, 'media')
        if getattr(settings, 'MEDIA_ROOT', None) and os.path.exists(settings.MEDIA_ROOT):
            shutil.copytree(settings.MEDIA_ROOT, media_dest, dirs_exist_ok=True)

        # 4. Create ZIP
        buffer = BytesIO()
        with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for root, dirs, files in os.walk(self.temp_dir):
                for file in files:
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, self.temp_dir)
                    zip_file.write(full_path, rel_path)

        # Cleanup
        shutil.rmtree(self.temp_dir)
        
        buffer.seek(0)
        return buffer
