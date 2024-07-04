import os
import streamlit as st
from PIL import Image
import openai
import numpy as np
from pdf2image import convert_from_path
import easyocr
from spellchecker import SpellChecker

# Load the OpenAI API key from an environment variable or directly (not recommended in production)
api_key = "sk-proj-VKAsVR32RCUTdhjh2MKXT3BlbkFJD93dBuFOG303eLbjpkqa"
if not api_key:
    st.error("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")
else:
    openai.api_key = api_key
 
# Lazy load heavy libraries to improve initial load time
def load_ocr_tools():
    return easyocr.Reader(['en'])

reader = load_ocr_tools()

# Function to process images and extract text
def ocr_image(image):
    try:
        # Adjusting OCR settings for handwritten text detection
        reader = easyocr.Reader(['en'], gpu=False, model_storage_directory='.')
        
        bounds = reader.readtext(np.array(image), detail=0, allowlist='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
        return '\n'.join([b for b in bounds])
    except Exception as e:
        st.error(f"Failed to process image: {str(e)}")
        return ""


# Function to process PDFs and extract text
def ocr_pdf(pdf_file):
    try:
        images = convert_from_path(pdf_file)
        text_pages = [ocr_image(image) for image in images]
        return '\n'.join(text_pages)
    except Exception as e:
        st.error(f"Failed to process PDF: {str(e)}")
        return ""

# Function to autocorrect the extracted text
def autocorrect_text(extracted_text):
    spell = SpellChecker()
    corrected_text = []
    
    # Split text into words and autocorrect each word
    words = extracted_text.split()
    for word in words:
        corrected_word = spell.correction(word)
        corrected_text.append(corrected_word)
    
    # Join corrected words back into a single string
    return ' '.join(corrected_text)

# Function to interact with OpenAI GPT and get page range, chapter name, and topic
def get_chatgpt_response(extracted_text):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are an assistant specialized in class 11 and 12 NCERT books. When given extracted text from OCR, provide the page range, chapter name, and topic relevant only to these classes."},
                {"role": "user", "content": f"Extracted Text:\n{extracted_text}"}
            ]
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        st.error(f"Failed to get response from GPT: {str(e)}")
        return "Error obtaining response."

# Streamlit UI setup
st.title("NCERT Textbook Helper")

# File uploader for PDF and image files
uploaded_file = st.file_uploader("Upload an Image or PDF from NCERT Books", type=["png", "jpg", "jpeg", "pdf"])

if uploaded_file:
    file_details = {"FileName": uploaded_file.name, "FileType": uploaded_file.type}
    st.write(f"Processing {file_details['FileType'].split('/')[-1].upper()} file: {file_details['FileName']}")

    if file_details["FileType"] == "application/pdf":
        text = ocr_pdf(uploaded_file)
    else:
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image', use_column_width=True)
        text = ocr_image(image)

    st.write("### Extracted Text:")
    edited_text = st.text_area("Edit Extracted Text", text)

    if st.button("NCERT HELP BOOK"):
        response = get_chatgpt_response(edited_text)
        st.write("### NCERT HELP BOOK:")
        st.write(response)
