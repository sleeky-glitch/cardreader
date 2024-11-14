import streamlit as st
import easyocr
import pandas as pd
import numpy as np
from PIL import Image
import io
import re

# Set page configuration
st.set_page_config(
    page_title="Business Card Scanner",
    page_icon="📇",
    layout="centered"
)

# Initialize EasyOCR reader
@st.cache_resource
def load_ocr():
    try:
        return easyocr.Reader(['en'])
    except Exception as e:
        st.error(f"Error loading OCR: {str(e)}")
        return None

def extract_text_from_image(image, reader):
    """Extract text from image using EasyOCR."""
    try:
        results = reader.readtext(np.array(image))
        return [text[1] for text in results]
    except Exception as e:
        st.error(f"Error in OCR: {str(e)}")



