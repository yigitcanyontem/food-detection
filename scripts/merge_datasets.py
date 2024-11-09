import yaml

# Define the paths to the YAML files
file1_path = 'merged.yaml'
file2_path = '../datasets/food_dataset/ingredients/data.yaml'
output_path = 'merged.yaml'

# Load both YAML files
with open(file1_path, 'r') as file:
    data1 = yaml.safe_load(file)

with open(file2_path, 'r') as file:
    data2 = yaml.safe_load(file)

# Initialize merged data with data1 content
merged_data = {
    'train': data1['train'],
    'val': data1['val'],
    'test': data1['test'],
    'nc': data1['nc'] + data2['nc'],  # Total count of unique items will be determined after merging
    'names': data1['names'][:]
}

# Create a mapping only for elements in the second array
index_map = {}

# Merge names without duplicates and create the index map for data2['names'] only
for i, name in enumerate(data2['names']):
    if name not in merged_data['names']:
        merged_index = len(merged_data['names'])
        merged_data['names'].append(name)
    else:
        merged_index = merged_data['names'].index(name)

    index_map[i] = merged_index  # Map original index in data2 to merged index

# Update the 'nc' value with the unique count of names
merged_data['nc'] = len(merged_data['names'])

# Save the merged data and index map
with open(output_path, 'w') as file:
    yaml.dump(merged_data, file)

print("Merged data saved to:", output_path)
print("Index map for data2 elements:", index_map)