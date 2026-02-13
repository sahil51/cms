from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import FileResponse
from .services import ThemeMutationService
from .utils import StaticSiteExporter
from pages.models import ContentPage

def ai_generate_view(request):
    pages = ContentPage.objects.live().all()
    selected_page_id = 'global'
    preview_url = '/'
    last_prompt = ''
    
    if request.method == 'POST':
        prompt = request.POST.get('prompt')
        page_id = request.POST.get('page_id')
        block_id = request.POST.get('block_id')
        last_prompt = prompt
        selected_page_id = page_id
        
        if prompt:
            try:
                from wagtail.models import Site
                try:
                    site = Site.find_for_request(request)
                except Exception:
                    site = Site.objects.filter(is_default_site=True).first()

                if page_id and block_id and page_id != 'global':
                    # Targeted mutation
                    ThemeMutationService.apply_targeted_mutation(prompt, page_id, block_id, site=site)
                    messages.success(request, f"Section updated on page {page_id}")
                else:
                    # Global theme mutation
                    page_titles = [p.title for p in pages]
                    ThemeMutationService.apply_mutation(prompt, site=site, page_titles=page_titles)
                    messages.success(request, f"Global theme updated from AI prompt")
                
                if page_id and page_id != 'global':
                    try:
                        target_page = ContentPage.objects.get(id=page_id)
                        preview_url = target_page.url
                    except Exception:
                        pass
            except Exception as e:
                import logging
                logger = logging.getLogger(__name__)
                logger.error(f"AI Generation Error: {str(e)}", exc_info=True)
                messages.error(request, f"Theme Mutation Failed: {str(e)}")
        else:
            messages.error(request, "Please enter a design prompt.")
            
    # Convert for easy template comparison
    try:
        if selected_page_id != 'global':
            selected_page_id = int(selected_page_id)
    except (ValueError, TypeError):
        selected_page_id = 'global'

    return render(request, 'ai/admin/generate_v2.html', {
        'pages': pages,
        'last_prompt': last_prompt,
        'preview_url': preview_url,
        'selected_page_id': selected_page_id
    })

def export_static_site(request):
    """View to trigger the static site export and download the ZIP."""
    try:
        exporter = StaticSiteExporter(request=request)
        zip_buffer = exporter.export()
        
        response = FileResponse(zip_buffer, content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename="static_site_export.zip"'
        return response
    except Exception as e:
        messages.error(request, f"Export failed: {str(e)}")
        return redirect('ai_generate')
