from django.shortcuts import render, redirect
from django.contrib import messages
from wagtail.models import Page, Site
from .models import ThemeSettings


def search(request):
    search_query = request.GET.get("query", None)
    page = request.GET.get("page", 1)

    # Search
    if search_query:
        search_results = Page.objects.live().search(search_query)
    else:
        search_results = Page.objects.none()

    # Pagination
    paginator = Paginator(search_results, 10)
    try:
        search_results = paginator.page(page)
    except PageNotAnInteger:
        search_results = paginator.page(1)
    except EmptyPage:
        search_results = paginator.page(paginator.num_pages)

    return render(
        request,
        "search/search.html",
        {
            "search_query": search_query,
            "search_results": search_results,
        },
    )

def theme_customizer(request):
    """View for side-by-side theme editing."""
    from wagtail.admin.forms.models import WagtailAdminModelForm
    from django import forms
    
    current_site = Site.find_for_request(request)
    if not current_site:
        current_site = Site.objects.get(is_default_site=True)
    
    config = ThemeSettings.for_site(current_site)
    
    # Create a dynamic form for ThemeSettings
    class ThemeSettingsForm(forms.ModelForm):
        class Meta:
            model = ThemeSettings
            fields = [
                'base_theme', 'primary_color', 'secondary_color', 
                'background_color', 'text_color', 'heading_font', 'body_font'
            ]
            widgets = {
                'primary_color': forms.TextInput(attrs={'type': 'color'}),
                'secondary_color': forms.TextInput(attrs={'type': 'color'}),
                'background_color': forms.TextInput(attrs={'type': 'color'}),
                'text_color': forms.TextInput(attrs={'type': 'color'}),
            }

    if request.method == 'POST':
        form = ThemeSettingsForm(request.POST, instance=config)
        if form.is_valid():
            form.save()
            messages.success(request, "Theme settings updated successfully!")
            return redirect('theme_customizer')
    else:
        form = ThemeSettingsForm(instance=config)

    return render(request, 'pages/admin/customizer.html', {
        'form': form,
        'preview_url': '/',  # Use relative path to avoid host mismatch issues
        'config': config,
    })
