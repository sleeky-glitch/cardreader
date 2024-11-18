import streamlit as st
import pandas as pd
from PIL import Image, ImageEnhance, ImageFilter
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

  # Preprocess the image
  image = image.convert('L')  # Convert to grayscale
  image = image.filter(ImageFilter.SHARPEN)  # Sharpen the image
  enhancer = ImageEnhance.Contrast(image)
  image = enhancer.enhance(2)  # Increase contrast

  # Use pytesseract to extract text from the image
  text = pytesseract.image_to_string(image, config='--psm 6')
  st.write("Extracted Text:")
  st.write(text)

  # Simple parsing logic (this can be improved based on card format)
  lines = text.split('\n')
  data = {'Name': '', 'Phone': '', 'Email': '', 'Company': ''}

  for line in lines:
      if "@" in line and "." in line:
          data['Email'] = line.strip()
      elif any(char.isdigit() for char in line):
          data['Phone'] = line.strip()
      elif len(line.split()) > 1:
          data['Name'] = line.strip()
      else:
          data['Company'] = line.strip()

  # Display extracted data
  st.write("Extracted Data:")
  st.write(data)

  # Convert data to a DataFrame
  df = pd.DataFrame([data])

  # Button to download the data as an Excel file
  if st.button("Download as Excel"):
      df.to_excel("visiting_card_data.xlsx", index=False)
      st.write("Data saved to visiting_card_data.xlsx")

