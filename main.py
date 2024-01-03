import streamlit as st
from pathlib import Path
from PIL import Image

import google.generativeai as genai

# Set page configuration
st.set_page_config(
    page_title="ُEDA AI Chat",
    page_icon="https://www.edaegypt.gov.eg/media/wc3lsydo/group-287.png",
    layout="wide",
)

# Display header
st.markdown('''
<img src="icon.png" width="250" height="100">
''', unsafe_allow_html=True)

# Display powered by information
st.markdown('''
<img src="https://www.edaegypt.gov.eg/media/wc3lsydo/group-287.png" width="250" height="100">''', unsafe_allow_html=True)
st.markdown('''
Powered by Google AI <img src="https://seeklogo.com/images/G/google-ai-logo-996E85F6FD-seeklogo.com.png" width="20" height="20"> Streamlit <img src="https://global.discourse-cdn.com/business7/uploads/streamlit/original/2X/f/f0d0d26db1f2d99da8472951c60e5a1b782eb6fe.png" width="22" height="22"> Python <img src="https://png2.cleanpng.com/sh/38d322d41e2d6d5738e129190b8c33a7/L0KzQYq3VsI0N5Ruf5H0aYP2gLBuTgB6fJl0hp9sb33zhcXskr1qa5Dzi595cnBqgrL0jflvb15xedDwdXHqdX7smPVkfaVmRadtMHazcbKAg8c5bpM4RqI9MUS7Q4e4UcU3OWM7TqoANUi0R4W1kP5o/kisspng-python-computer-icons-programming-language-executa-5d0f0aa7c78fb3.0414836115612668558174.png" width="22" height="22">''', unsafe_allow_html=True)


langcols = st.columns([0.2,0.8])
with langcols[0]:
  lang = st.selectbox('Select your language',
  ('English', 'العربية'),index=1)

if 'lang' not in st.session_state:
    st.session_state.lang = lang
st.divider()

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
genai.configure(api_key="AIzaSyCFPALEVIiwvWSREvVdBOzNd1VeyqQWt9o")
model = genai.GenerativeModel(
    model_name="gemini-pro-vision",
    generation_config=generation_config,
    safety_settings=safety_settings,
)

# Function to handle file upload and model response
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

# File upload and response display
uploaded_file, response_en, response_ar = upload_file(st.file_uploader)

# Display responses
st.text("Uploaded File: " + uploaded_file)
st.text("English Response:")
st.write(response_en)
st.text("Arabic Response:")
st.write(response_ar)
