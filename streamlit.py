import streamlit as st
import pytesseract
import pandas as pd
import numpy as np
from PIL import Image
import re
import io

# Set page configuration
st.set_page_config(
    page_title="Business Card Scanner",
    page_icon="📇",
    layout="centered"
)

def extract_text_from_image(image):
    """
    Extract text from image using Tesseract OCR
    """
    try:
        text = pytesseract.image_to_string(image)
        return text.split('\n')
    except Exception as e:
        st.error(f"Error in OCR: {str(e)}")
        return []

def extract_info(text_lines):
    """
    Extract relevant information from OCR text
    """
    # Remove empty lines and strip whitespace
    text_lines = [line.strip() for line in text_lines if line.strip()]

