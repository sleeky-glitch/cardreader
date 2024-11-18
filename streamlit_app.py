# Example parsing logic
lines = text.split('\n')
data = {'Name': '', 'Phone': '', 'Email': '', 'Company': ''}

for line in lines:
  line = line.strip()
  if "@" in line and "." in line:
      data['Email'] = line
  elif line.startswith("+") and any(char.isdigit() for char in line):
      data['Phone'] = line
  elif "Software" in line or "Pvt Ltd" in line:
      data['Company'] = line
  elif len(line.split()) > 1 and not data['Name']:
      data['Name'] = line

# Display extracted data
st.write("Extracted Data:")
st.write(data)

