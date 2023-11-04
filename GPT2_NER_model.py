import pandas as pd
from transformers import GPT2Tokenizer, GPT2LMHeadModel
import re
import torch

# Define the path to your file
file_path = "Pick Place for Yabby3 4G V3.1.txt"

# Initialize GPT-2 tokenizer and model
model_name = "gpt2"  # You can specify different versions of GPT-2
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPT2LMHeadModel.from_pretrained(model_name)

# Read the file to get the semi-structured data
data = []
start_reading = False  # Flag to indicate when to start reading data

# Read the file line by line
with open(file_path, 'r', encoding='latin1') as file:
    for line in file:
        # Check if the line contains "Designator" to start reading data
        if "Designator" in line:
            start_reading = True

        if start_reading:
            data.append(line.strip())

# Recognize entities using GPT-2
recognized_entities = []
for line in data:
    input_text = "Recognize entities in: " + line
    input_ids = tokenizer.encode(input_text, return_tensors="pt")
    with torch.no_grad():
        output = model.generate(input_ids, max_length=150, num_return_sequences=1, no_repeat_ngram_size=2, top_k=50)
    generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
    recognized_entities.append(generated_text[len("Recognize entities in: "):])

# Organize the recognized entities into structured data
structured_data = []
for line, entities in zip(data, recognized_entities):
    parts = re.split(r'\s{2,}', line)
    entities = entities.split()  # Split entities by spaces
    structured_data.append(parts + entities)

# Ensure consistent column count
max_columns = max(len(row) for row in structured_data)
structured_data = [row + [''] * (max_columns - len(row)) for row in structured_data]

# Create a DataFrame
df = pd.DataFrame(structured_data, columns=[f"Col_{i}" for i in range(max_columns)])
# Select and rename the desired columns
df = df[['Col_0', 'Col_2', 'Col_4', 'Col_5', 'Col_6']]
df.columns = ['Designator', 'Layer', 'Center-X', 'Center-Y', 'Rotation']
df = df[~df['Designator'].str.contains('Comment')]
# Print the modified DataFrame
print(df)
df.to_excel('excel_pinck_.xlsx')
