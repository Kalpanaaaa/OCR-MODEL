# NCERT Textbook Helper

This project is a web application built with Streamlit that helps users extract text from NCERT textbooks (both images and PDFs), autocorrect the extracted text, and obtain relevant information such as page range, chapter name, and topic using OpenAI's GPT-4-turbo model.

## Features

- Extract text from uploaded images or PDF files.
- Autocorrect extracted text using a spell checker.
- Interact with OpenAI GPT-4-turbo to obtain relevant NCERT information (page range, chapter name, topic).

### Running the Application
```
streamlit run app.py

```
Open your web browser and go to http://localhost:8501 to access the application.

### Usage
1. Upload an Image or PDF:
Click the "Browse files" button to upload an image (PNG, JPG, JPEG) or PDF file from NCERT books.

2. Process the File:
For PDFs, specify the maximum number of pages to process and the image resolution (DPI).
The application will extract text from the uploaded file and display it in a text area.

3. Edit Extracted Text:
Review and edit the extracted text in the text area if needed.

4. Get NCERT Help:
Click the "NCERT HELP BOOK" button to get the relevant NCERT page range, chapter name, and topic from OpenAI GPT-4-turbo based on the extracted text.

