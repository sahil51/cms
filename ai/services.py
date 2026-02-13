import json
import logging
import os
from dotenv import load_dotenv
from google import genai
from django.core.exceptions import ValidationError
from pages.models import ThemeSettings, ContentPage

load_dotenv()

logger = logging.getLogger(__name__)

ALLOWED_BASE_THEMES = ['modern', 'minimal', 'bold']
ALLOWED_VARIANTS = ['v1', 'v2', 'v3']

class ThemeMutationService:
    @staticmethod
    def get_gemini_design(prompt, site=None, page_titles=None):
        """Calls Gemini API with fallback models to get a structured design JSON using modern SDK."""
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            logger.error("GEMINI_API_KEY is missing from environment.")
            raise ValidationError("GEMINI_API_KEY not configured in environment.")
        
        # Site-specific context
        site_name = "this project"
        if site:
            try:
                from .models import SiteSettings
                settings = SiteSettings.for_site(site)
                site_name = settings.site_name or site.site_name
            except Exception:
                pass

        client = genai.Client(api_key=api_key)
        
        # Models to try in order
        fallback_models = [
            'models/gemini-2.5-flash-lite',
            'models/gemini-2.5-flash',
            'models/gemini-3-flash-preview',
        ]
        
        system_instruction = f"""
        You are a Senior UI/UX Designer and Conversion Strategist for '{site_name}'.
        Your goal is to generate a sophisticated, conversion-optimized design system blueprint that fits this specific project's identity.

        ### Project Structure (Pages):
        The project currently contains the following core pages:
        {', '.join(page_titles) if page_titles else 'Multiple modular content pages'}
        
        ### Project Architecture (Available Blocks):
        You are modifying a high-end CMS built with the following components:
        1. Hero & Carousel Hero (Above-the-fold impact)
        2. About, Services, & Industries (Content layers)
        3. Why Choose Us & Process Steps (Value props)
        4. Trust Bar, Testimonials, & Success Stories (Social proof)
        5. Lead Magnet, Lead Form, & CTAs (Conversion anchors)
        6. Gallery & Documents (Resource layers)

        ### Design Principles to Enforce:
        1. Visual Hierarchy: Establish a clear F-pattern layout. Use intentional contrast to guide the user's eye.
        2. Color Theory: Apply professional color harmonies. Ensure WCAG-compliant contrast.
        3. Typography: Pair fonts that evoke 'Trust', 'Authority', and 'Modernity'. 
        4. Spatial System: Implement rhythmic whitespace (the 8pt grid system).
        5. Component Logic: Use 'Primary Action Emphasis' for quotes and 'Secondary Ghost Buttons' for indirect contact.

        ### Technical Response Format:
        Respond ONLY with a valid JSON object. No prose.
        
        The JSON schema must be:
        {{
            "base_theme": "modern" | "minimal" | "bold",
            "primary_color": "Hex color",
            "secondary_color": "Hex color",
            "background_color": "Hex color",
            "text_color": "Hex color",
            "hero_variant": "v1" | "v2" | "v3",
            "about_variant": "v1" | "v2" | "v3",
            "services_variant": "v1" | "v2" | "v3",
            "faq_variant": "v1" | "v2" | "v3",
            "typography": {{
                "heading_font": "Google Font Name (e.g., Outfit, Inter, Roboto)",
                "body_font": "Google Font Name (e.g., Outfit, Inter, Roboto)"
            }},
            "animation_preset": "smooth-fade" | "parallax" | "bounce" | "slide" | "none"
        }}
        """
        
        last_error = None
        for model_name in fallback_models:
            try:
                logger.info(f"Attempting theme generation with model: {model_name}")
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                    config={
                        'system_instruction': system_instruction,
                        'response_mime_type': 'application/json'
                    }
                )
                
                content = response.text.strip()
                
                # Basic JSON validation check
                json.loads(content)
                return content
            except Exception as e:
                logger.warning(f"Model {model_name} failed: {str(e)}")
                last_error = e
                continue
        
        raise ValidationError(f"All Gemini models failed. Last error: {str(last_error)}")

    @staticmethod
    def validate_theme_json(data):
        """
        Validates the structured JSON from AI to ensure it only contains safe 
        and recognized theme parameters.
        """
        required_keys = ['base_theme', 'primary_color', 'secondary_color', 'typography']
        for key in required_keys:
            if key not in data:
                raise ValidationError(f"Missing required key in AI response: {key}")
        
        if data.get('base_theme') not in ALLOWED_BASE_THEMES:
            data['base_theme'] = 'modern'
            
        for color_key in ['primary_color', 'secondary_color', 'background_color', 'text_color']:
            color = data.get(color_key)
            if color:
                if not isinstance(color, str) or not color.startswith('#') or len(color) > 9:
                     raise ValidationError(f"Invalid color format for {color_key}")

    @staticmethod
    def apply_targeted_mutation(prompt, page_id, block_id, site=None):
        """
        Calls Gemini to get a mutation for a SPECIFIC block on a SPECIFIC page.
        """
        page = ContentPage.objects.get(id=page_id)
        target_block = None
        block_index = -1
        
        for i, block in enumerate(page.body):
            if getattr(block, 'id', str(i)) == block_id:
                target_block = block
                block_index = i
                break
        
        if not target_block:
            raise ValidationError(f"Block with ID {block_id} not found on page {page_id}")

        # Site-specific context for targeted mutation
        site_name = "this project"
        if site:
            try:
                from .models import SiteSettings
                settings = SiteSettings.for_site(site)
                site_name = settings.site_name or site.site_name
            except Exception:
                pass

        # Construct a specialized prompt for a single block
        system_instruction = f"""
        You are a Senior UI/UX Designer for '{site_name}'. 
        Generate a conversion-optimized payload for the '{target_block.block_type}' section on the '{page.title}' page.

        ### Section-Specific UX Psychology:
        - Hero: Frictionless CTAs. Focus on above-the-fold impact for '{site_name}'.
        - Services: Micro-copy that highlights 'Value'. entry point for '{page.title}'.
        - Lead Magnet: Authritative and premium.
        - Success Story: Authenticity. data-driven story titles.
        - Trust Bar: 'Echo of Authority'. premium corporate feel.
        
        ### Copywriting Rules:
        - Be direct, professional, and authoritative.
        - Use context from the project name '{site_name}' and page '{page.title}'.
        
        Respond ONLY with a valid JSON object matching the section's JSON schema fields exactly.
        """
        
        # We can reuse get_gemini_design since it now handles the system_instruction correctly via config
        # However, for targeted mutation we might want to pass the system_instruction explicitly
        api_key = os.getenv('GEMINI_API_KEY')
        client = genai.Client(api_key=api_key)
        
        response = client.models.generate_content(
            model='models/gemini-2.5-flash-lite',
            contents=prompt,
            config={
                'system_instruction': system_instruction,
                'response_mime_type': 'application/json'
            }
        )
        data = json.loads(response.text)
        
        # update the block in the StreamField
        new_value = target_block.value.copy()
        for key, val in data.items():
            if key in new_value:
                new_value[key] = val
        
        # StreamField items are (block_type, value, id)
        page.body[block_index] = (target_block.block_type, new_value, block_id)
        
        page.save_revision().publish()
        return page

    @staticmethod
    def apply_mutation(prompt, ai_json_str=None, site=None, page_titles=None):
        """
        Parses AI JSON string, validates it, and updates the tenant's ThemeConfig.
        If ai_json_str is None, it calls Gemini to get it.
        """
        try:
            if ai_json_str is None:
                ai_json_str = ThemeMutationService.get_gemini_design(prompt, site=site, page_titles=page_titles)

            data = json.loads(ai_json_str)
            ThemeMutationService.validate_theme_json(data)
            
            if not site:
                from wagtail.models import Site
                site = Site.objects.filter(is_default_site=True).first()
                if not site:
                    site = Site.objects.first()
            
            # Use for_site to get the correct setting for this authenticated site
            # This handles getting or creating the setting for the specific site
            config = ThemeSettings.for_site(site)
            
            config.base_theme = data.get('base_theme', config.base_theme)
            config.primary_color = data.get('primary_color', config.primary_color)
            config.secondary_color = data.get('secondary_color', config.secondary_color)
            config.background_color = data.get('background_color', config.background_color)
            config.text_color = data.get('text_color', config.text_color)
            
            config.hero_variant = data.get('hero_variant', config.hero_variant)
            config.about_variant = data.get('about_variant', config.about_variant)
            config.services_variant = data.get('services_variant', config.services_variant)
            config.faq_variant = data.get('faq_variant', config.faq_variant)
            
            typography = data.get('typography', {})
            config.heading_font = typography.get('heading_font', config.heading_font)
            config.body_font = typography.get('body_font', config.body_font)
                
            config.animation_preset = data.get('animation_preset', config.animation_preset)
            config.last_ai_prompt = prompt
            
            config.save()
            return config
            
        except (json.JSONDecodeError, ValidationError) as e:
            logger.error(f"Theme mutation failed for prompt '{prompt}': {str(e)}")
            raise ValidationError(f"AI response validation failed: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error in ThemeMutationService: {str(e)}")
            raise e
