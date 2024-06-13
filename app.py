import streamlit as st
from PIL import Image
import pytesseract
from pdf2image import convert_from_path
import tempfile
import os


def ocr_image(image):
    img = Image.open(image)
    text = pytesseract.image_to_string(img, config='--psm 6')
    return text

def ocr_pdf(uploaded_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        temp_file.write(uploaded_file.read())
        temp_file.flush()
        images = convert_from_path(temp_file.name, output_folder=os.path.dirname(temp_file.name))
        text = ""
        for image in images:
            text += pytesseract.image_to_string(image, config='--psm 6') + "\n"
        return text

st.title("Handwritten OCR with Streamlit")

st.sidebar.title("Upload Files")
uploaded_file = st.sidebar.file_uploader("Choose an image or PDF", type=["jpg", "jpeg", "png", "pdf"])

if uploaded_file is not None:
    file_type = uploaded_file.type

    if file_type in ["image/jpeg", "image/png", "image/jpg"]:
        st.image(uploaded_file, caption='Uploaded Image', use_column_width=True)
        st.write("Extracted Text:")
        text = ocr_image(uploaded_file)
        st.text(text)

    elif file_type == "application/pdf":
        st.write("Uploaded PDF")
        text = ocr_pdf(uploaded_file)
        st.write("Extracted Text:")
        st.text(text)

else:
    st.info("Please upload an image or PDF file.")


''"""sumary_line"""

