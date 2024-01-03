import streamlit as st
from pathlib import Path
from PIL import Image

import google.generativeai as genai

# Set up the model
generation_config = {
    "temperature": 0.4,
    "top_p": 1,
    "top_k": 32,
    "max_output_tokens": 4096,
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

model = genai.GenerativeModel(
    model_name="gemini-pro-vision",
    generation_config=generation_config,
    safety_settings=safety_settings,
)

# Function to handle file upload and model response
def generate_gemini_response(input_prompt, image_loc):
    image_prompt = input_image_setup(image_loc)
    prompt_parts = [input_prompt, image_prompt[0]]

    # Generate response in English
    response_en = model.generate_content(prompt_parts)

    # Generate response in Arabic
    response_ar = model.generate_content(prompt_parts, lang="ar")

    return response_en.text, response_ar.text

def input_image_setup(file_loc):
    if not (img := Path(file_loc)).exists():
        raise FileNotFoundError(f"Could not find image: {img}")

    image_parts = [
        {"mime_type": "image/jpeg", "data": Path(file_loc).read_bytes()}
    ]
    return image_parts

def upload_file(file_uploader):
    uploaded_file = file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    
    if uploaded_file:
        try:
            response_en, response_ar = generate_gemini_response(input_prompt, uploaded_file)
            return uploaded_file.name, response_en, response_ar
        except Exception as e:
            return f"Error processing image: {e}", "", ""
    else:
        return "", "", ""

# Set page configuration
st.set_page_config(
    page_title="Diabetes AI Assistant",
    page_icon="icon.png",
    layout="wide",
)

# Display header
st.markdown('''
<img src="icon.png" width="250" height="100">
''', unsafe_allow_html=True)

# Display powered by information
st.markdown('''
Powered by Google AI <img src="google_ai_logo.png" width="20" height="20"> Streamlit <img src="streamlit_logo.png" width="22" height="22"> Python <img src="python_logo.png" width="22" height="22">''', unsafe_allow_html=True)

# Language selection
langcols = st.columns([0.2, 0.8])
with langcols[0]:
    lang = st.selectbox('Select your language', ('English', 'العربية'), index=1)

# File upload and response display
try:
    uploaded_file, response_en, response_ar = upload_file(st.file_uploader)
except Exception as e:
    st.error(f"Error: {e}")

# Display responses
st.text("Uploaded File: " + uploaded_file)
st.text("English Response:")
st.write(response_en)
st.text("Arabic Response:")
st.write(response_ar)
