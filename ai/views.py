from django.shortcuts import render, redirect
from django.contrib import messages
from .services import ThemeMutationService
from pages.models import ContentPage

def ai_generate_view(request):
    pages = ContentPage.objects.live().all()
    
    if request.method == 'POST':
        prompt = request.POST.get('prompt')
        page_id = request.POST.get('page_id')
        block_id = request.POST.get('block_id')
        
        if prompt:
            try:
                if page_id and block_id and page_id != 'global':
                    # Targeted mutation
                    ThemeMutationService.apply_targeted_mutation(prompt, page_id, block_id)
                    messages.success(request, f"AI has updated the section on page {page_id} based on: '{prompt}'")
                else:
                    # Global theme mutation
                    ThemeMutationService.apply_mutation(prompt)
                    messages.success(request, f"AI has updated the global theme based on: '{prompt}'")
                
                return redirect('wagtailadmin_home')
            except Exception as e:
                messages.error(request, f"Theme Mutation Failed: {str(e)}")
        else:
            messages.error(request, "Please enter a design prompt.")
            
    return render(request, 'ai/admin/generate.html', {
        'pages': pages
    })
