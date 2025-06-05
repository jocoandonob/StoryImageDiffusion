# 📚 Visual Story Generator

A powerful web application that generates consistent visual stories from your uploaded images. Using advanced AI models, it creates engaging narratives with matching illustrations while maintaining visual consistency throughout the story.

## ✨ Features

- **Visual Story Generation**: Upload a reference image and generate a complete story with matching illustrations
- **Consistent Character Design**: Maintains visual consistency of characters and style across all generated images
- **Customizable Story Settings**:
  - Choose story genre (Adventure, Fantasy, Mystery, Romance, Sci-Fi, Horror, Children's Story)
  - Set number of scenes (3-10)
  - Control story length and detail
  - Adjust image generation parameters
- **Interactive Web Interface**: User-friendly Streamlit interface with real-time generation
- **Download Package**: Export your complete story with all illustrations as a downloadable package

## 🚀 Getting Started

### Prerequisites

- Python 3.11 or higher
- OpenAI API key

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/StoryImageDiffusion.git
cd StoryImageDiffusion
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your OpenAI API key:
```bash
# On Windows
set OPENAI_API_KEY=your-api-key-here

# On Linux/Mac
export OPENAI_API_KEY=your-api-key-here
```

### Running the Application

Start the Streamlit application:
```bash
streamlit run app.py
```

The application will be available at `http://localhost:5000`

## 🎨 How to Use

1. **Upload Reference Image**
   - Click the upload area to select an image
   - The image will be analyzed for story generation

2. **Configure Story Settings**
   - Enter a story idea or theme
   - Select the number of scenes (3-10)
   - Choose words per page
   - Pick a story genre
   - Adjust image generation settings if desired

3. **Generate Story**
   - Click "Generate Visual Story"
   - Wait for the story and images to be generated
   - View the complete story with illustrations

4. **Download**
   - Click the download button to get a zip package containing:
     - Complete story text
     - All generated illustrations

## 🛠️ Technical Details

The application uses several advanced AI models and technologies:

- **OpenAI GPT-4**: For story generation and image analysis
- **DALL-E 3**: For high-quality image generation
- **Streamlit**: For the web interface
- **PyTorch**: For image processing capabilities

## 📝 Project Structure

```
StoryImageDiffusion/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── pyproject.toml        # Project configuration
├── utils/
│   ├── image_processor.py    # Image analysis and processing
│   ├── story_generator.py    # Story generation logic
│   └── diffusion_generator.py # Image generation
└── .streamlit/
    └── config.toml       # Streamlit configuration
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- OpenAI for providing the GPT-4 and DALL-E 3 APIs
- Streamlit for the web framework
- The open-source community for various tools and libraries 