import pandas as pd
import spacy
import re
import string
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import csv  # Import the csv module

# Load the spaCy NER model
nlp = spacy.load("en_core_web_sm")

# ... (same code to read the file and start_reading)
file_path = "/content/drive/MyDrive/Colab_Notebooks/Pick Place for Yabby3 4G V3.1.txt"
start_reading = False  # Initialize start_reading
data = []  # Initialize data as an empty list

with open(file_path, 'r', encoding='latin1') as file:
    for line in file:
        # Check if the line contains "Designator" to start reading data
        if "Designator" in line:
            start_reading = True

        if start_reading:
            data.append(line.strip())

# Recognize entities using spaCy NER
recognized_entities = []
for line in data:
    doc = nlp(line)
    entities = [ent.text for ent in doc.ents]
    recognized_entities.append(entities)

# Organize the recognized entities into structured data
structured_data = []
for line, entities in zip(data, recognized_entities):
    parts = csv.reader([line], delimiter=' ', quotechar='"', skipinitialspace=True).__next__()  # Change this line
    # Pad entities with empty strings to match the length of parts
    entities += [''] * (len(parts) - len(entities))
    structured_data.append(parts + entities)

# Ensure consistent column count
max_columns = max(len(row) for row in structured_data)
structured_data = [row + [''] * (max_columns - len(row)) for row in structured_data]

# Create a DataFrame
df = pd.DataFrame(structured_data, columns=[f"Col_{i}" for i in range(max_columns)])

# Select relevant columns and rename them
df = df[['Col_0', 'Col_2', 'Col_4', 'Col_5', 'Col_6']]
df.columns = ['Designator', 'Layer', 'Center-X(mm)', 'Center-Y(mm)', 'Rotation']
df = df.drop(df.index[0])
# Clean the "Designator" column to handle the issue with single space
df['Designator'] = df['Designator'].apply(lambda x: re.sub(r'\s(?=[A-Z])', '', x))

# Filter out rows where the "Designator" column contains the string "Comment"
df = df[~df['Designator'].str.contains('Comment')]

# Write the DataFrame to an Excel file
df.to_excel('/content/drive/MyDrive/Colab_Notebooks/excel_pinck_.xlsx', index=False)

# Print the modified DataFrame
df.head(65)
