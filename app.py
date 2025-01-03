import streamlit as st
import cv2
import pytesseract
from pytesseract import Output
import numpy as np
import os

# Function to extract text from an image
def extract_text_from_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    custom_config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(thresh, config=custom_config, output_type=Output.STRING)
    return text

# Function to parse extracted text
def parse_title_and_author(extracted_text):
    lines = extracted_text.strip().split("\n")
    title = lines[0] if lines else "Unknown Title"
    author = lines[1] if len(lines) > 1 else "Unknown Author"
    return title, author

# Streamlit App
st.title("Book Cover Text Extractor")
st.write("Upload an image of a book cover, and we'll extract the title and author for you!")

uploaded_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    file_bytes = np.frombuffer(uploaded_file.read(), np.uint8)
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    st.image(image, caption="Uploaded Image", use_column_width=True)

    extracted_text = extract_text_from_image(image)
    title, author = parse_title_and_author(extracted_text)

    st.write(f"**Title**: {title}")
    st.write(f"**Author**: {author}")

    result_text = f"Title: {title}\nAuthor: {author}\n"
    st.download_button("Download Extracted Text", result_text, "extracted_text.txt", "text/plain")