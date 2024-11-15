import streamlit as st
import easyocr
import pandas as pd
import numpy as np
from PIL import Image
import io
import re
from pathlib import Path

# Set page configuration
st.set_page_config(
  page_title="Business Card Scanner",
  page_icon="📇",
  layout="centered"
)

# Create a downloads directory if it doesn't exist
DOWNLOADS_DIR = Path("downloads")
DOWNLOADS_DIR.mkdir(exist_ok=True)

# Initialize EasyOCR reader with better caching
@st.cache_resource(show_spinner=False)
def load_ocr():
  try:
      return easyocr.Reader(['en'], gpu=False)  # Explicitly disable GPU for cloud deployment
  except Exception as e:
      st.error(f"Error loading OCR: {str(e)}")
      return None

# Optimize image processing
@st.cache_data(show_spinner=False)
def process_image(image):
  """Preprocess image for better OCR results"""
  img_array = np.array(image)
  return img_array

@st.cache_data(show_spinner=False)
def extract_text_from_image(image_array, reader):
  """Extract text from image using EasyOCR with caching"""
  try:
      results = reader.readtext(image_array)
      return [text[1] for text in results]
  except Exception as e:
      st.error(f"Error in OCR: {str(e)}")
      return []

# Optimize information extraction with better patterns
@st.cache_data(show_spinner=False)
def extract_info(text_list):
  """Extract relevant information from the text with improved patterns"""
  info = {
      'name': '',
      'phone': '',
      'email': '',
      'website': '',
      'company': '',
      'address': ''
  }
  
  patterns = {
      'email': r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
      'phone': r'[\+]?[\d]{0,3}[\s.-]?$?\d{3}$?[\s.-]?\d{3}[\s.-]?\d{4}',
      'website': r'(?:www\.)?[a-zA-Z0-9][a-zA-Z0-9-]{1,61}[a-zA-Z0-9]\.[a-zA-Z]{2,}'
  }
  
  address_indicators = {'street', 'avenue', 'road', 'lane', 'drive', 'boulevard', 
                       'st', 'ave', 'rd', 'ln', 'dr', 'blvd'}
  
  for text in text_list:
      text = text.strip()
      
      # Extract using patterns
      for key, pattern in patterns.items():
          if not info[key] and re.search(pattern, text.lower()):
              info[key] = re.search(pattern, text.lower()).group()
              continue
      
      # Address detection
      if any(indicator in text.lower() for indicator in address_indicators):
          info['address'] = text
          continue
      
      # Name and company detection
      words = text.split()
      if len(words) <= 3 and not info['name']:
          info['name'] = text
      elif not info['company']:
          info['company'] = text
  
  return info

def create_excel_file(info):
  """Create Excel file from extracted information"""
  df = pd.DataFrame([info])
  output = io.BytesIO()
  with pd.ExcelWriter(output, engine='openpyxl') as writer:
      df.to_excel(writer, index=False)
  return output.getvalue()

def main():
  st.title("📇 Business Card Scanner")
  st.write("Upload a business card image to extract contact information")
  
  # Initialize OCR with progress indicator
  with st.spinner('Initializing OCR engine...'):
      reader = load_ocr()
  
  if not reader:
      st.error("Failed to initialize OCR. Please refresh the page.")
      return
  
  uploaded_file = st.file_uploader("Choose a business card image", 
                                 type=['png', 'jpg', 'jpeg'],
                                 help="Upload a clear image of a business card")
  
  if uploaded_file:
      try:
          # Process image
          image = Image.open(uploaded_file)
          st.image(image, caption='Uploaded Business Card', use_column_width=True)
          
          with st.spinner('Extracting information...'):
              # Process and extract text
              image_array = process_image(image)
              text_list = extract_text_from_image(image_array, reader)
              
              if text_list:
                  info = extract_info(text_list)
                  
                  # Display results in a clean layout
                  st.subheader("📝 Extracted Information")
                  
                  col1, col2 = st.columns(2)
                  with col1:
                      for field in ['name', 'phone', 'email']:
                          st.text_input(field.capitalize(), info[field], key=field)
                  
                  with col2:
                      for field in ['company', 'website', 'address']:
                          st.text_input(field.capitalize(), info[field], key=field)
                  
                  # Export functionality
                  if st.button("Export to Excel", type="primary"):
                      excel_data = create_excel_file(info)
                      st.download_button(
                          label="📥 Download Excel file",
                          data=excel_data,
                          file_name="business_card_info.xlsx",
                          mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                      )
              else:
                  st.warning("No text detected. Please try with a clearer image.")
                  
      except Exception as e:
          st.error(f"Error processing image: {str(e)}")
  
  # Footer
  st.markdown("---")
  st.markdown(
      """
      <div style='text-align: center'>
          <p>Made with ❤️ by Nishant @ BSPL</p>
      </div>
      """,
      unsafe_allow_html=True
  )

if __name__ == "__main__":
  main()
