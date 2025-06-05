import os
from PIL import Image, ImageDraw, ImageFont
import io
import base64
from openai import OpenAI

class DiffusionGenerator:
    def __init__(self):
        """Initialize the diffusion generator with OpenAI DALL-E"""
        self.openai_client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY", "your-openai-api-key")
        )
    
    def _load_models(self):
        """Load the diffusion models - Not needed for OpenAI DALL-E"""
        pass
    
    def prepare_reference_image(self, image, target_size=(1024, 1024)):
        """Prepare reference image for conditioning"""
        try:
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Resize while maintaining aspect ratio
            image.thumbnail(target_size, Image.Resampling.LANCZOS)
            
            # Create a new image with target size and paste the resized image
            new_image = Image.new('RGB', target_size, (255, 255, 255))
            
            # Calculate position to center the image
            x = (target_size[0] - image.width) // 2
            y = (target_size[1] - image.height) // 2
            new_image.paste(image, (x, y))
            
            return new_image
            
        except Exception as e:
            raise Exception(f"Failed to prepare reference image: {str(e)}")
    
    def generate_scene_image(self, reference_image, scene_description, 
                           guidance_scale=7.5, num_inference_steps=30, strength=0.75):
        """Generate an image for a specific scene maintaining consistency with reference"""
        try:
            # Extract visual features from reference image to enhance consistency
            from utils.image_processor import ImageProcessor
            image_processor = ImageProcessor()
            visual_features = image_processor.extract_visual_features(reference_image)
            
            # Enhanced prompt to ensure character consistency by referencing the uploaded image
            # This ensures DALL-E knows to include the same character/subject
            consistency_prompt = (
                f"Based on the uploaded reference image style and main character: {scene_description}. "
                f"Important: Feature the exact same main character/subject from the reference image "
                f"(same species, appearance, colors, and visual style). "
                f"Maintain identical art style, lighting, and composition approach as the reference. "
                f"Visual consistency elements: {visual_features[:200]}. "
                f"High quality, detailed, consistent character design."
            )
            
            full_prompt = consistency_prompt
            
            # Generate image using OpenAI DALL-E 3
            # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
            # do not change this unless explicitly requested by the user
            response = self.openai_client.images.generate(
                model="dall-e-3",
                prompt=full_prompt,
                n=1,
                size="1024x1024",
                quality="standard"
            )
            
            # Download the generated image
            import requests
            image_url = response.data[0].url
            image_response = requests.get(image_url)
            
            if image_response.status_code == 200:
                generated_image = Image.open(io.BytesIO(image_response.content))
                return generated_image
            else:
                raise Exception(f"Failed to download generated image: HTTP {image_response.status_code}")
            
        except Exception as e:
            # Return a placeholder image if generation fails
            placeholder = self._create_error_placeholder(str(e))
            return placeholder
    
    def _create_error_placeholder(self, error_message):
        """Create a placeholder image when generation fails"""
        try:
            # Create a simple placeholder image with error message
            placeholder = Image.new('RGB', (1024, 1024), (240, 240, 240))
            draw = ImageDraw.Draw(placeholder)
            
            # Try to draw error message
            try:
                # Use default font
                draw.text((50, 500), f"Image generation failed:\n{error_message[:100]}...", 
                         fill=(100, 100, 100))
            except:
                pass
            
            return placeholder
        except:
            # If even placeholder creation fails, create minimal image
            return Image.new('RGB', (512, 512), (200, 200, 200))
    
    def adjust_consistency_strength(self, scene_index, total_scenes):
        """Adjust strength parameter based on scene position for narrative flow"""
        # First scene should be most similar to reference (lower strength)
        # Middle scenes can deviate more for story progression
        # Final scene can return closer to reference for closure
        
        if scene_index == 0:
            return 0.6  # Stay close to reference
        elif scene_index == total_scenes - 1:
            return 0.7  # Return somewhat to reference
        else:
            return 0.8  # Allow more deviation for story progression
    
    def batch_generate_scenes(self, reference_image, scene_descriptions,
                            guidance_scale=7.5, num_inference_steps=30):
        """Generate all scene images in batch for better consistency"""
        generated_images = []
        
        for i, description in enumerate(scene_descriptions):
            # Adjust strength based on scene position
            strength = self.adjust_consistency_strength(i, len(scene_descriptions))
            
            try:
                image = self.generate_scene_image(
                    reference_image=reference_image,
                    scene_description=description,
                    guidance_scale=guidance_scale,
                    num_inference_steps=num_inference_steps,
                    strength=strength
                )
                generated_images.append(image)
                
            except Exception as e:
                # Add placeholder if individual generation fails
                placeholder = self._create_error_placeholder(f"Scene {i+1} generation failed: {str(e)}")
                generated_images.append(placeholder)
        
        return generated_images
