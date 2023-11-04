import pandas as pd
import spacy
import re

# Load the spaCy NER model
nlp = spacy.load("en_core_web_sm")

# ... (same code to read the file and start_reading)
file_path = "Pick Place for Yabby3 4G V3.1.txt"
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
    parts = re.split(r'\s{2,}', line)
    structured_data.append(parts + entities)

# Ensure consistent column count
max_columns = max(len(row) for row in structured_data)
structured_data = [row + [''] * (max_columns - len(row)) for row in structured_data]

# Create a DataFrame
df = pd.DataFrame(structured_data, columns=[f"Col_{i}" for i in range(max_columns)])

df = df[['Col_0', 'Col_2', 'Col_4', 'Col_5', 'Col_6']]
df.columns = ['Designator', 'Layer', 'Center-X', 'Center-Y', 'Rotation']
df = df[~df['Designator'].str.contains('Comment')]
# Print the modified DataFrame

df.to_excel('excel_pinck_.xlsx', index=False)

print(df)
