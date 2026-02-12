import json
import logging
import os
from google import genai
from django.core.exceptions import ValidationError
from pages.models import ThemeConfig

logger = logging.getLogger(__name__)

ALLOWED_BASE_THEMES = ['modern', 'minimal', 'bold']
ALLOWED_VARIANTS = ['v1', 'v2', 'v3']

class ThemeMutationService:
    @staticmethod
    def get_gemini_design(prompt):
        """Calls Gemini API with fallback models to get a structured design JSON using modern SDK."""
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValidationError("GEMINI_API_KEY not configured in environment.")

        client = genai.Client(api_key=api_key)
        
        # Models to try in order
        fallback_models = [
            'gemini-2.0-flash',
            'gemini-2.0-flash-exp',
            'gemini-1.5-flash',
            'gemini-1.5-pro'
        ]
        
        system_instruction = """
        You are an expert web designer and copywriter. Based on the user's prompt, generate a conversion-optimized website configuration.
        Follow this blueprint strictly for section logic:
        - Hero: Primary CTA (e.g. Get a Quote) AND Secondary CTA (e.g. Call Us Link).
        - Services: Each service must have a clear 'Learn More' CTA.
        - Trust: Include Partner logos and Success Stories.
        - Lead Magnet: A section specifically to 'Download Free Guide' or similar offer.
        
        Respond ONLY with a valid JSON object.
        
        The JSON schema must be:
        {
            "base_theme": "modern" | "minimal" | "bold",
            "primary_color": "Hex color",
            "secondary_color": "Hex color",
            "background_color": "Hex color",
            "text_color": "Hex color",
            "hero_variant": "v1" | "v2" | "v3",
            "about_variant": "v1" | "v2" | "v3",
            "services_variant": "v1" | "v2" | "v3",
            "faq_variant": "v1" | "v2" | "v3",
            "typography": {
                "heading_font": "Font Name",
                "body_font": "Font Name"
            },
            "animation_preset": "smooth-fade" | "parallax" | "bounce" | "slide" | "none"
        }
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
    def apply_targeted_mutation(prompt, page_id, block_id):
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

        # Construct a specialized prompt for a single block
        system_instruction = f"""
        You are a conversion-optimized web designer. Generate content for a {target_block.block_type} section.
        Follow these specific structural rules:
        - Hero: Must have a primary 'Call to Action' and a secondary 'Contact' link.
        - Services: Each service must have a 'Learn More' link.
        - Lead Magnet: Focus on a specific offer like 'Download Free Guide'.
        - Success Story: Highlight specific client names and story titles.
        - Partners: Display logos of trusted collaborators.
        
        Respond ONLY with a valid JSON object matching the section's fields.
        """
        
        # We can reuse get_gemini_design since it now handles the system_instruction correctly via config
        # However, for targeted mutation we might want to pass the system_instruction explicitly
        api_key = os.getenv('GEMINI_API_KEY')
        client = genai.Client(api_key=api_key)
        
        response = client.models.generate_content(
            model='gemini-2.0-flash',
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
    def apply_mutation(prompt, ai_json_str=None):
        """
        Parses AI JSON string, validates it, and updates the tenant's ThemeConfig.
        If ai_json_str is None, it calls Gemini to get it.
        """
        try:
            if ai_json_str is None:
                ai_json_str = ThemeMutationService.get_gemini_design(prompt)

            data = json.loads(ai_json_str)
            ThemeMutationService.validate_theme_json(data)
            
            config = ThemeConfig.objects.first()
            if not config:
                config = ThemeConfig()
            
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
