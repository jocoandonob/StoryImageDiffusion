import streamlit as st
import io
import base64
from PIL import Image
import zipfile
import os
from utils.image_processor import ImageProcessor
from utils.story_generator import StoryGenerator
from utils.diffusion_generator import DiffusionGenerator
from dotenv import load_dotenv
load_dotenv()
# Check if OpenAI API key is loaded
if os.getenv("OPENAI_API_KEY"):
    print("[INFO] OPENAI_API_KEY loaded successfully.")
else:
    print("[WARNING] OPENAI_API_KEY is NOT set. Please set it in your environment.")

# Configure page
st.set_page_config(
    page_title="Cartoon Story Creator",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark theme and cartoon style
st.markdown("""
<style>
    /* Global styles */
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        color: #e0e0e0;
    }
    
    /* Main header with cartoon style */
    .main-header {
        text-align: center;
        padding: 2rem;
        background: linear-gradient(90deg, #ff6b6b 0%, #ff8e53 100%);
        color: white;
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(255, 107, 107, 0.2);
        border: 4px solid #ffd93d;
        font-family: 'Comic Sans MS', cursive;
    }
    
    .main-header h1 {
        font-size: 3.5rem;
        margin: 0;
        text-shadow: 3px 3px 0 #ffd93d;
    }
    
    .main-header p {
        font-size: 1.5rem;
        margin: 1rem 0 0;
        opacity: 0.9;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #16213e 0%, #1a1a2e 100%);
    }
    
    .config-section {
        background: rgba(255, 255, 255, 0.05);
        padding: 1.5rem;
        border-radius: 15px;
        border: 2px solid #ffd93d;
        margin-bottom: 1.5rem;
        backdrop-filter: blur(10px);
    }
    
    .config-section h3 {
        color: #ffd93d;
        font-family: 'Comic Sans MS', cursive;
        font-size: 1.8rem;
        margin-bottom: 1rem;
    }
    
    /* Scene container styling */
    .scene-container {
        background: rgba(255, 255, 255, 0.05);
        border: 3px solid #ffd93d;
        border-radius: 20px;
        padding: 2rem;
        margin: 1.5rem 0;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
    }
    
    .story-title {
        color: #ffd93d;
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        margin: 2rem 0;
        font-family: 'Comic Sans MS', cursive;
        text-shadow: 2px 2px 0 #ff6b6b;
    }
    
    .scene-title {
        color: #ff8e53;
        font-size: 1.8rem;
        font-weight: 600;
        margin-bottom: 1.5rem;
        padding-bottom: 0.8rem;
        border-bottom: 3px dashed #ffd93d;
        font-family: 'Comic Sans MS', cursive;
    }
    
    /* Image upload area styling */
    .image-upload-area {
        border: 4px dashed #ffd93d;
        border-radius: 20px;
        padding: 3rem;
        text-align: center;
        background: rgba(255, 255, 255, 0.05);
        margin: 2rem 0;
        transition: all 0.3s ease;
    }
    
    .image-upload-area:hover {
        border-color: #ff6b6b;
        background: rgba(255, 255, 255, 0.08);
    }
    
    /* Button styling */
    .stButton>button {
        background: linear-gradient(90deg, #ff6b6b 0%, #ff8e53 100%);
        color: white;
        border: none;
        padding: 0.8rem 2rem;
        border-radius: 50px;
        font-size: 1.2rem;
        font-weight: bold;
        box-shadow: 0 4px 15px rgba(255, 107, 107, 0.3);
        transition: all 0.3s ease;
        border: 2px solid #ffd93d;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(255, 107, 107, 0.4);
    }
    
    /* Slider styling */
    .stSlider {
        color: #ffd93d;
    }
    
    .stSlider>div>div>div {
        background: linear-gradient(90deg, #ff6b6b 0%, #ff8e53 100%);
    }
    
    /* Text input styling */
    .stTextArea>div>div>textarea {
        background: rgba(255, 255, 255, 0.05);
        border: 2px solid #ffd93d;
        border-radius: 15px;
        color: #e0e0e0;
    }
    
    /* Selectbox styling */
    .stSelectbox>div>div {
        background: rgba(255, 255, 255, 0.05);
        border: 2px solid #ffd93d;
        border-radius: 15px;
        color: #e0e0e0;
    }
    
    /* Progress bar styling */
    .stProgress>div>div>div>div {
        background: linear-gradient(90deg, #ff6b6b 0%, #ff8e53 100%);
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: #1a1a2e;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #ffd93d;
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #ff6b6b;
    }
    
    /* Story text styling */
    .story-text {
        font-family: 'Comic Sans MS', cursive;
        font-size: 1.2rem;
        line-height: 1.6;
        color: #e0e0e0;
        padding: 1rem;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        border-left: 4px solid #ffd93d;
    }
    
    /* Image container styling */
    .image-container {
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
        border: 3px solid #ffd93d;
    }
    
    /* Download button styling */
    .download-button {
        background: linear-gradient(90deg, #4CAF50 0%, #45a049 100%);
        color: white;
        padding: 1rem 2rem;
        border-radius: 50px;
        font-size: 1.2rem;
        font-weight: bold;
        border: 2px solid #ffd93d;
        box-shadow: 0 4px 15px rgba(76, 175, 80, 0.3);
    }
</style>
""", unsafe_allow_html=True)

def initialize_generators():
    """Initialize the AI generators"""
    if "story_generator" not in st.session_state:
        st.session_state.story_generator = StoryGenerator()
    if "image_processor" not in st.session_state:
        st.session_state.image_processor = ImageProcessor()
    if "diffusion_generator" not in st.session_state:
        st.session_state.diffusion_generator = DiffusionGenerator()

def create_story_package(story_data, scene_images):
    """Create a downloadable package of the story and images"""
    try:
        # Create a zip file in memory
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            # Add story text
            story_text = f"""# {story_data['title']}

{story_data['introduction']}

"""
            for i, scene in enumerate(story_data['scenes']):
                story_text += f"""
## Scene {i+1}

{scene['narrative']}
"""
            story_text += f"""

{story_data['conclusion']}
"""
            zip_file.writestr('story.txt', story_text)
            
            # Add images
            for i, image in enumerate(scene_images):
                img_buffer = io.BytesIO()
                image.save(img_buffer, format='PNG')
                zip_file.writestr(f'scene_{i+1}.png', img_buffer.getvalue())
        
        # Prepare the zip file for download
        zip_buffer.seek(0)
        st.download_button(
            label="📥 Download Story Package",
            data=zip_buffer,
            file_name="cartoon_story.zip",
            mime="application/zip",
            use_container_width=True
        )
    except Exception as e:
        st.error(f"Failed to create story package: {str(e)}")

def main():
    # Main header with cartoon style
    st.markdown('''
        <div class="main-header">
            <h1>🎨 Cartoon Story Creator</h1>
            <p>Create magical cartoon stories from your imagination!</p>
        </div>
    ''', unsafe_allow_html=True)
    
    # Initialize generators
    initialize_generators()
    
    # Sidebar for configuration with cartoon style
    with st.sidebar:
        st.markdown("### 🎭 Story Settings")
        
        story_idea = st.text_area(
            "💡 Your Story Idea", 
            placeholder="What kind of magical adventure would you like to create?",
            help="Let your imagination run wild! Describe your story idea...",
            height=100
        )
        
        col1, col2 = st.columns(2)
        with col1:
            num_scenes = st.slider("🖼️ Number of Scenes", min_value=3, max_value=10, value=5)
        with col2:
            words_per_page = st.slider("📝 Story Length", min_value=20, max_value=200, value=50, step=10)
        
        story_genre = st.selectbox(
            "🎨 Story Style",
            ["Magical Adventure", "Funny Friends", "Space Journey", "Underwater World", 
             "Forest Friends", "City Adventures", "Fantasy Kingdom"]
        )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("### ⚡ Generation Settings")
        
        guidance_scale = st.slider("🎯 Style Strength", min_value=5.0, max_value=20.0, value=7.5, step=0.5)
        num_inference_steps = st.slider("✨ Detail Level", min_value=20, max_value=50, value=30)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Main content area
    col1, col2 = st.columns([1, 2])

    uploaded_file = None  # Ensure variable is always defined
    image = None          # Ensure variable is always defined

    with col1:
        st.markdown('<div class="image-upload-area">', unsafe_allow_html=True)
        uploaded_file = st.file_uploader(
            "📸 Upload Your Character Image",
            type=["jpg", "jpeg", "png"],
            help="Upload an image of your main character or scene"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        if uploaded_file:
            image = Image.open(uploaded_file)
            st.image(image, use_column_width=True, caption="Your Character")

    with col2:
        if uploaded_file and image is not None:
            if st.button("🎨 Create Cartoon Story", use_container_width=True):
                with st.spinner("Creating your magical story..."):
                    try:
                        # Process image and generate story
                        image_processor = ImageProcessor()
                        image_analysis = image_processor.analyze_image(image)
                        
                        story_generator = StoryGenerator()
                        story_data = story_generator.generate_story(
                            image_analysis=image_analysis,
                            num_scenes=num_scenes,
                            genre=story_genre,
                            story_idea=story_idea,
                            words_per_page=words_per_page
                        )
                        
                        # Display story
                        st.markdown(f'<div class="story-title">{story_data["title"]}</div>', unsafe_allow_html=True)
                        st.markdown(f'<div class="story-text">{story_data["introduction"]}</div>', unsafe_allow_html=True)
                        
                        # Generate and display scenes
                        diffusion_generator = DiffusionGenerator()
                        scene_images = diffusion_generator.batch_generate_scenes(
                            image,
                            [scene["description"] for scene in story_data["scenes"]],
                            guidance_scale=guidance_scale,
                            num_inference_steps=num_inference_steps
                        )
                        
                        for i, (scene, scene_image) in enumerate(zip(story_data["scenes"], scene_images)):
                            st.markdown(f'<div class="scene-container">', unsafe_allow_html=True)
                            st.markdown(f'<div class="scene-title">Scene {i+1}</div>', unsafe_allow_html=True)
                            st.image(scene_image, use_column_width=True)
                            st.markdown(f'<div class="story-text">{scene["narrative"]}</div>', unsafe_allow_html=True)
                            st.markdown('</div>', unsafe_allow_html=True)
                        
                        st.markdown(f'<div class="story-text">{story_data["conclusion"]}</div>', unsafe_allow_html=True)
                        
                        # Download button
                        if st.button("📥 Download Story Package", use_container_width=True):
                            create_story_package(story_data, scene_images)
                            
                    except Exception as e:
                        st.error(f"Oops! Something went wrong: {str(e)}")
        else:
            st.markdown('''
                <div style="text-align: center; padding: 2rem;">
                    <h2 style="color: #ffd93d;">🎨 Let's Create a Story!</h2>
                    <p style="font-size: 1.2rem;">Upload an image to start your magical adventure!</p>
                </div>
            ''', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
