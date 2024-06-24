

import streamlit as st
import easyocr
from pdf2image import convert_from_path
import numpy as np
from PIL import Image
import openai
import os

# Set your OpenAI API key
openai.api_key = "sk-proj-ylH8E6fOfLnnlQzSjH7RT3BlbkFJqNN7zmQyBVeB8RbFTAi9"



# Initialize the OCR reader
reader = easyocr.Reader(['en'])

# Function to process images
def ocr_image(image):
    bounds = reader.readtext(np.array(image))
    text = '\n'.join([b[1] for b in bounds])
    return text

# Function to process PDFs
def ocr_pdf(pdf_file):
    images = convert_from_path(pdf_file)
    text = ''
    for image in images:
        text += ocr_image(image) + '\n'
    return text

# Function to interact with OpenAI GPT
def get_chatgpt_response(extracted_text):
    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "You are an NCERT page finder. When given extracted text from OCR, provide the page number and topic of the text."},
            {"role": "user", "content": f"Extracted Text:\n{extracted_text}"}
        ]
    )
    return response.choices[0].message['content'].strip()

# Streamlit UI
st.title("Handwritten Notes to Text")

uploaded_file = st.file_uploader("Upload an Image or PDF", type=["png", "jpg", "jpeg", "pdf"])

if uploaded_file is not None:
    file_details = {"FileName": uploaded_file.name, "FileType": uploaded_file.type}

    if file_details["FileType"] == "application/pdf":
        st.write(f"Processing PDF file: {file_details['FileName']}")
        text = ocr_pdf(uploaded_file)
    else:
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image', use_column_width=True)
        st.write(f"Processing Image file: {file_details['FileName']}")
        text = ocr_image(image)
    
    st.write("### Extracted Text:")
    st.write(text)
    
    # Get ChatGPT response
    if st.button("Find NCERT Page and Topic"):
        response = get_chatgpt_response(text)
        st.write("### NCERT Page and Topic:")
        st.write(response)
