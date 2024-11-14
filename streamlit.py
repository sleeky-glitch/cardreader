import streamlit as st
import easyocr
import pandas as pd
import numpy as np
import cv2
from PIL import Image
import re
import os
import io
import tempfile

# Set page configuration
st.set_page_config(
    page_title="Business Card Scanner",
    page_icon="📇",
    layout="wide"
)

# Initialize EasyOCR reader
@st.cache_resource
def load_ocr():
    return easyocr.Reader(['en'])

def extract_info(text_list):
    """
    Extract relevant information from OCR text
    """
    # Initialize dictionary to store information
    info = {
        'name': '',
        'phone': '',
        'email': '',
        'company': '',
        'website': '',
        'address': ''
    }
    
    # Regular expressions for different fields
