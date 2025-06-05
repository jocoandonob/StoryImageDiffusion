import base64
import io
from PIL import Image
import os
from openai import OpenAI

class ImageProcessor:
    def __init__(self):
        """Initialize the image processor with OpenAI client"""
        self.openai_client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY", "your-openai-api-key")
        )
    
    def image_to_base64(self, image):
        """Convert PIL Image to base64 string"""
        try:
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Save to bytes buffer
            buffer = io.BytesIO()
            image.save(buffer, format='JPEG', quality=85)
            buffer.seek(0)
            
            # Encode to base64
            image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
            return image_base64
        except Exception as e:
            raise Exception(f"Failed to convert image to base64: {str(e)}")
    
    def resize_image(self, image, max_size=(1024, 1024)):
        """Resize image while maintaining aspect ratio"""
        try:
            image.thumbnail(max_size, Image.Resampling.LANCZOS)
            return image
        except Exception as e:
            raise Exception(f"Failed to resize image: {str(e)}")
    
    def analyze_image(self, image):
        """Analyze uploaded image using OpenAI's vision capabilities"""
        try:
            # Resize image to reasonable size for API
            processed_image = self.resize_image(image.copy())
            
            # Convert to base64
            image_base64 = self.image_to_base64(processed_image)
            
            # Analyze with OpenAI vision
            # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
            # do not change this unless explicitly requested by the user
            response = self.openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "Analyze this image in detail for story generation purposes. "
                                      "Describe the following aspects:\n"
                                      "1. Main subjects/characters and their appearance\n"
                                      "2. Setting, environment, and atmosphere\n"
                                      "3. Colors, lighting, and mood\n"
                                      "4. Visual style and artistic elements\n"
                                      "5. Potential story themes or narrative directions\n"
                                      "6. Key visual elements that should be maintained for consistency\n"
                                      "Provide a comprehensive analysis that will guide both story creation and visual consistency."
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{image_base64}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=800
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            raise Exception(f"Failed to analyze image: {str(e)}")
    
    def extract_visual_features(self, image):
        """Extract key visual features for consistency prompts"""
        try:
            # Resize image for processing
            processed_image = self.resize_image(image.copy())
            image_base64 = self.image_to_base64(processed_image)
            
            # Extract specific visual features for consistency
            # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
            # do not change this unless explicitly requested by the user
            response = self.openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "Extract key visual consistency elements from this image for maintaining character and style consistency across multiple generated images. "
                                      "Focus on:\n"
                                      "- Character appearance details (if any)\n"
                                      "- Art style and rendering approach\n"
                                      "- Color palette and lighting style\n"
                                      "- Visual composition elements\n"
                                      "Provide specific, detailed descriptions that can be used as conditioning prompts."
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{image_base64}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=500
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            raise Exception(f"Failed to extract visual features: {str(e)}")
