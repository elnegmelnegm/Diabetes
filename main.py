import streamlit as st
from pathlib import Path
from PIL import Image
import pandas as pd
from gradio import Interface

import google.generativeai as genai
from google.colab import userdata
from PIL import Image
import requests

genai.__version__

genai.configure(api_key="AIzaSyCFPALEVIiwvWSREvVdBOzNd1VeyqQWt9o")

# Set up the model
generation_config = {
  "temperature": 0.4,
  "top_p": 1,
  "top_k": 32,
  "max_output_tokens": 4096,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  }
]

model = genai.GenerativeModel(model_name="gemini-pro-vision",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

# Language selection
langcols = st.columns([0.2, 0.8])
with langcols[0]:
    lang = st.selectbox('Select your language', ('English', 'العربية'), index=1)

# Update input prompt
input_prompt = """
               As an expert specializing in assessing the suitability of fruits and foods for individuals with diabetes, your task involves analyzing input images featuring various food items. Your first objective is to identify the type of fruit or food present in the image. Subsequently, you must determine the glycemic index of the identified item. Based on this glycemic index, provide recommendations on whether individuals with diabetes can include the detected food in their diet. If the food is deemed suitable, specify the recommended quantity for consumption. Use English and Arabic languages for response.
               """


def input_image_setup(file_loc):
    if not (img := Path(file_loc)).exists():
        raise FileNotFoundError(f"Could not find image: {img}")

    image_parts = [
        {
            "mime_type": "image/jpeg",
            "data": Path(file_loc).read_bytes()
        }
    ]
    return image_parts


def generate_gemini_response(input_prompt, image_loc):
    image_prompt = input_image_setup(image_loc)
    prompt_parts = [input_prompt, image_prompt[0]]

    # Generate response in English
    response_en = model.generate_content(prompt_parts)

    # Generate response in Arabic
    response_ar = model.generate_content(prompt_parts, lang="ar")

    return response_en.text, response_ar.text


def upload_file(files):
    file_paths = [file.name for file in files]
    if file_paths:
        response_en, response_ar = generate_gemini_response(input_prompt, file_paths[0])
    return file_paths[0], response_en, response_ar


with Interface() as demo:
    file_output = gr.Textbox()
    image_output = gr.Image()
    combined_output = [image_output, file_output]
    upload_button = gr.UploadButton("Click to Upload an Image of the Food that you want to eat",
                                    file_types=["image"],
                                    file_count="multiple")
    upload_button.upload(upload_file, upload_button, combined_output)

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

# Rest of the code remains unchanged
# ...
# ...

# Run the app
st.run_app(debug=True)
