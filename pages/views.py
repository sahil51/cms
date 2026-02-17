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
    """View for full-page visual theme editing."""
    from django import forms
    from wagtail.images.models import Image
    
    current_site = Site.find_for_request(request)
    if not current_site:
        current_site = Site.objects.get(is_default_site=True)
    
    config = ThemeSettings.for_site(current_site)
    
    FONT_CHOICES = [
        ('Inter', 'Inter'), ('Roboto', 'Roboto'), ('Poppins', 'Poppins'),
        ('Montserrat', 'Montserrat'), ('Open Sans', 'Open Sans'),
        ('Lato', 'Lato'), ('Raleway', 'Raleway'), ('Outfit', 'Outfit'),
        ('Playfair Display', 'Playfair Display'), ('DM Sans', 'DM Sans'),
        ('Space Grotesk', 'Space Grotesk'), ('Oswald', 'Oswald'),
    ]
    
    ANIMATION_CHOICES = [
        ('smooth-fade', 'Smooth Fade'), ('slide-up', 'Slide Up'),
        ('zoom-in', 'Zoom In'), ('none', 'No Animation'),
    ]
    
    class ThemeSettingsForm(forms.ModelForm):
        logo_upload = forms.ImageField(required=False, label="Upload New Logo")
        hero_image_upload = forms.ImageField(required=False, label="Upload Hero Background")
        
        class Meta:
            model = ThemeSettings
            fields = [
                'base_theme', 'site_name',
                'primary_color', 'secondary_color', 'background_color', 'text_color',
                'heading_font', 'body_font',
                'hero_video_url', 'animation_preset',
            ]
            widgets = {
                'base_theme': forms.Select(attrs={'class': 'vc-select'}),
                'site_name': forms.TextInput(attrs={'class': 'vc-input', 'placeholder': 'Your Site Name'}),
                'primary_color': forms.TextInput(attrs={'type': 'color', 'class': 'vc-color'}),
                'secondary_color': forms.TextInput(attrs={'type': 'color', 'class': 'vc-color'}),
                'background_color': forms.TextInput(attrs={'type': 'color', 'class': 'vc-color'}),
                'text_color': forms.TextInput(attrs={'type': 'color', 'class': 'vc-color'}),
                'heading_font': forms.Select(choices=FONT_CHOICES, attrs={'class': 'vc-select'}),
                'body_font': forms.Select(choices=FONT_CHOICES, attrs={'class': 'vc-select'}),
                'hero_video_url': forms.URLInput(attrs={'class': 'vc-input', 'placeholder': 'https://...video.mp4'}),
                'animation_preset': forms.Select(choices=ANIMATION_CHOICES, attrs={'class': 'vc-select'}),
            }

    if request.method == 'POST':
        form = ThemeSettingsForm(request.POST, request.FILES, instance=config)
        if form.is_valid():
            obj = form.save(commit=False)
            
            # Handle logo upload
            logo_file = form.cleaned_data.get('logo_upload')
            if logo_file:
                logo_image = Image(title=f"Logo - {logo_file.name}", file=logo_file)
                logo_image.save()
                obj.logo = logo_image
            
            # Handle hero background upload
            hero_file = form.cleaned_data.get('hero_image_upload')
            if hero_file:
                hero_image = Image(title=f"Hero BG - {hero_file.name}", file=hero_file)
                hero_image.save()
                obj.hero_bg_image = hero_image
            
            obj.save()
            messages.success(request, f"Theme updated to '{obj.base_theme}' successfully!")
            return redirect('theme_customizer')
        else:
            messages.error(request, f"Error saving theme: {form.errors}")

    else:
        form = ThemeSettingsForm(instance=config)

    # Get all images for the image browser
    images = Image.objects.order_by('-created_at')[:30]
    
    return render(request, 'pages/admin/customizer.html', {
        'form': form,
        'preview_url': '/',
        'config': config,
        'images': images,
        'current_logo': config.logo,
        'current_hero_bg': config.hero_bg_image,
    })
