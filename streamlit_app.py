import streamlit as st
import pandas as pd
from PIL import Image
import pytesseract

# Set up the Streamlit app
st.title("Visiting Card Reader")
st.write("Upload an image of a visiting card to extract information.")

# File uploader for the visiting card image
uploaded_file = st.file_uploader("Choose an image file", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Open the image file
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Visiting Card', use_column_width=True)

    # Use pytesseract to extract text from the image
    text = pytesseract.image_to_string(image)
    st.write("Extracted Text:")
    st.write(text)

    # Simple parsing logic (this can be improved based on card format)

