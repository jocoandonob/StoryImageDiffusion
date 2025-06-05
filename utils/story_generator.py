import json
import os
from openai import OpenAI

class StoryGenerator:
    def __init__(self):
        """Initialize the story generator with OpenAI client"""
        self.openai_client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY", "your-openai-api-key")
        )
    
    def generate_story(self, image_analysis, num_scenes=5, genre="Adventure", story_idea="", words_per_page=50):
        """Generate a coherent story based on image analysis"""
        try:
            # Build the story prompt with user's idea
            story_direction = f"Story direction: {story_idea}" if story_idea.strip() else ""
            
            story_prompt = f"""
            Based on the following image analysis, create a compelling {genre.lower()} story with exactly {num_scenes} scenes.
            
            Image Analysis:
            {image_analysis}
            
            {story_direction}
            
            CRITICAL REQUIREMENTS FOR CHARACTER CONSISTENCY:
            1. IDENTIFY the main character/subject from the image analysis (animal, person, object)
            2. This SAME character must be the protagonist in EVERY scene without exception
            3. Each scene description must explicitly mention this character by name/type
            4. The character should maintain the same appearance, colors, and species throughout
            5. Each narrative should be approximately {words_per_page} words
            
            Story Structure Requirements:
            1. Create a story title featuring the main character
            2. Write a brief introduction establishing the main character
            3. Generate exactly {num_scenes} connected scenes where:
               - Scene description STARTS with the main character name/type
               - Description includes specific visual details of the character
               - Narrative follows the character's journey/adventure
            4. Provide a conclusion featuring the same character
            5. Maintain logical story flow and character development
            
            Genre: {genre}
            
            IMPORTANT: Every scene description must begin with "The [character type/name] from the reference image" to ensure visual consistency in generated images.
            
            Respond with a JSON object in this exact format:
            {{
                "title": "Story Title",
                "introduction": "Introduction paragraph",
                "scenes": [
                    {{
                        "description": "Brief visual description for image generation that includes the main character",
                        "narrative": "Story narrative for this scene (approximately {words_per_page} words)"
                    }}
                ],
                "conclusion": "Conclusion paragraph"
            }}
            """
            
            # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
            # do not change this unless explicitly requested by the user
            response = self.openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert storyteller and creative writer. "
                                 "Create engaging, coherent stories that can be visualized effectively. "
                                 "Always respond with valid JSON format."
                    },
                    {
                        "role": "user",
                        "content": story_prompt
                    }
                ],
                response_format={"type": "json_object"},
                max_tokens=2000
            )
            
            content = response.choices[0].message.content
            if content:
                story_data = json.loads(content)
            else:
                raise Exception("No content received from OpenAI")
            
            # Validate the response structure
            self._validate_story_structure(story_data, num_scenes)
            
            return story_data
            
        except json.JSONDecodeError as e:
            raise Exception(f"Failed to parse story JSON: {str(e)}")
        except Exception as e:
            raise Exception(f"Failed to generate story: {str(e)}")
    
    def _validate_story_structure(self, story_data, expected_scenes):
        """Validate the generated story structure"""
        required_fields = ['title', 'introduction', 'scenes', 'conclusion']
        
        for field in required_fields:
            if field not in story_data:
                raise Exception(f"Missing required field in story: {field}")
        
        if not isinstance(story_data['scenes'], list):
            raise Exception("Scenes must be a list")
        
        if len(story_data['scenes']) != expected_scenes:
            raise Exception(f"Expected {expected_scenes} scenes, got {len(story_data['scenes'])}")
        
        for i, scene in enumerate(story_data['scenes']):
            if 'description' not in scene or 'narrative' not in scene:
                raise Exception(f"Scene {i+1} missing required fields (description, narrative)")
    
    def enhance_scene_description(self, scene_description, visual_features, style):
        """Enhance scene description with visual consistency prompts"""
        try:
            enhancement_prompt = f"""
            Enhance this scene description for image generation while maintaining visual consistency:
            
            Original scene: {scene_description}
            
            Visual consistency requirements:
            {visual_features}
            
            Desired style: {style}
            
            Create an enhanced prompt that:
            1. Maintains the original scene's essence
            2. Incorporates visual consistency elements
            3. Specifies the desired artistic style
            4. Is optimized for diffusion model generation
            5. Is concise but descriptive (under 200 words)
            
            Return only the enhanced prompt text.
            """
            
            # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
            # do not change this unless explicitly requested by the user
            response = self.openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert at creating prompts for AI image generation models. "
                                 "Focus on visual consistency and artistic quality."
                    },
                    {
                        "role": "user",
                        "content": enhancement_prompt
                    }
                ],
                max_tokens=300
            )
            
            content = response.choices[0].message.content
            return content.strip() if content else scene_description
            
        except Exception as e:
            # Return original description if enhancement fails
            return scene_description
