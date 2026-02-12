from django.http import JsonResponse
from pages.models import ContentPage
from django.shortcuts import get_object_or_404

def get_page_sections(request, page_id):
    """Returns a list of blocks/sections for a given page."""
    page = get_object_or_404(ContentPage, id=page_id)
    sections = []
    
    # page.body is a StreamField
    for i, block in enumerate(page.body):
        # We use a combined label of the block type and index/ID
        # StreamField blocks usually have a unique ID in Wagtail 2.x+
        block_id = getattr(block, 'id', str(i))
        sections.append({
            'id': block_id,
            'type': block.block_type,
            'label': f"{block.block_type.capitalize()} (Section {i+1})",
            'current_variant': block.value.get('variant', 'v1') if hasattr(block.value, 'get') else 'v1'
        })
        
    return JsonResponse({'sections': sections})
