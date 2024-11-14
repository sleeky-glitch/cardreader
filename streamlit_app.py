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
      return []

def extract_info(text_list):
  """Extract relevant information from the text."""
  info = {
      'name': '',
      'phone': '',
      'email': '',
      'website': '',
      'company': '',
      'address': ''
  }
  
  # Regular expressions for matching
  email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
  phone_pattern = r'[\+$]?[1-9][0-9 .\-\($]{8,}[0-9]'
  website_pattern = r'www\.[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}|https?://[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
  
  address_indicators = ['street', 'avenue', 'road', 'lane', 'drive', 'boulevard', 'st', 'ave', 'rd', 'ln', 'dr', 'blvd']
  
  for text in text_list:
      text = text.strip()
      
      # Extract email
      if re.search(email_pattern, text.lower()):
          info['email'] = re.search(email_pattern, text.lower()).group()
          continue
          
      # Extract phone
      if re.search(phone_pattern, text):
          info['phone'] = re.search(phone_pattern, text).group()
          continue
          
      # Extract website
      if re.search(website_pattern, text.lower()):
          info['website'] = re.search(website_pattern, text.lower()).group()
          continue
          
      # Look for address
      if any(indicator in text.lower() for indicator in address_indicators):
          info['address'] = text
          continue
          
      # If text is short, it might be a name or company
      if len(text.split()) <= 3 and not info['name']:
          info['name'] = text
      elif not info['company']:
          info['company'] = text
          
  return info

def main():
  st.title("📇 Business Card Scanner")
  st.write("Upload a business card image to extract contact information")
  
  # Load OCR reader
  reader = load_ocr()
  if not reader:
      st.error("Failed to initialize OCR. Please try again.")
      return
  
  # File uploader
  uploaded_file = st.file_uploader("Choose a business card image", type=['png', 'jpg', 'jpeg'])
  
  if uploaded_file is not None:
      try:
          # Display the uploaded image
          image = Image.open(uploaded_file)
          st.image(image, caption='Uploaded Business Card', use_column_width=True)
          
          with st.spinner('Extracting information...'):
              # Extract text from image
              text_list = extract_text_from_image(image, reader)
              
              if text_list:
                  # Extract structured information
                  info = extract_info(text_list)
                  
                  # Display extracted information
                  st.subheader("📝 Extracted Information")
                  
                  col1, col2 = st.columns(2)
                  
                  with col1:
                      st.text_input("Name", info['name'])
                      st.text_input("Phone", info['phone'])
                      st.text_input("Email", info['email'])
                      
                  with col2:
                      st.text_input("Company", info['company'])
                      st.text_input("Website", info['website'])
                      st.text_input("Address", info['address'])
                  
                  # Export to Excel option
                  if st.button("Export to Excel"):
                      df = pd.DataFrame([info])
                      
                      # Convert DataFrame to Excel
                      output = io.BytesIO()
                      with pd.ExcelWriter(output, engine='openpyxl') as writer:
                          df.to_excel(writer, index=False)
                      
                      # Prepare download button
                      excel_data = output.getvalue()
                      st.download_button(
                          label="Download Excel file",
                          data=excel_data,
                          file_name="business_card_info.xlsx",
                          mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                      )
              else:
                  st.warning("No text was extracted from the image. Please try with a clearer image.")
                  
      except Exception as e:
          st.error(f"Error processing image: {str(e)}")
          
  # Add footer
  st.markdown("---")
  st.markdown(
      """
      <div style='text-align: center'>
          <p>Made with ❤️ by Your Name</p>
      </div>
      """,
      unsafe_allow_html=True
  )

if __name__ == "__main__":
  main()



