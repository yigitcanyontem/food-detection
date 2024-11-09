import os

def update_label_files(label_map, path):
    """
    Update .txt label files by replacing keys in label_map with their corresponding values.

    Args:
    - label_map (dict): A dictionary where keys are labels to be changed and values are the new labels.
    - path (str): The path to the directory containing the .txt files.
    """
    # Check if the provided path exists
    if not os.path.exists(path):
        print(f"The provided path does not exist: {path}")
        return

    # Iterate over all files in the directory
    for filename in os.listdir(path):
        if filename.endswith('.txt'):
            file_path = os.path.join(path, filename)
            print(f"Updating file: {file_path}")

            # Read the contents of the file
            with open(file_path, 'r') as file:
                content = file.readlines()

            # Update the content based on the label_map
            updated_content = []
            for line in content:
                # Split the line by spaces to handle label and coordinates
                parts = line.strip().split()
                if parts:
                    label = parts[0]  # The first part is the label index
                    # Replace label if it exists in the label_map
                    if int(label) in label_map:
                        parts[0] = str(label_map[int(label)])  # Update the label
                    updated_content.append(' '.join(parts) + '\n')  # Join back into a line

            # Write the updated content back to the file
            with open(file_path, 'w') as file:
                file.writelines(updated_content)

            print(f"Updated {filename} successfully.")

# Example usage:
if __name__ == "__main__":
    # Define the dictionary for label changes
    label_map =  {0: 2, 1: 8, 2: 173, 3: 302, 4: 303, 5: 17, 6: 19, 7: 21, 8: 24, 9: 27, 10: 182, 11: 304, 12: 35, 13: 37, 14: 195, 15: 41, 16: 42, 17: 164, 18: 200, 19: 49, 20: 56, 21: 305, 22: 59, 23: 208, 24: 306, 25: 61, 26: 68, 27: 69, 28: 70, 29: 223, 30: 73, 31: 74, 32: 79, 33: 227, 34: 228, 35: 166, 36: 87, 37: 101, 38: 102, 39: 307, 40: 105, 41: 308, 42: 111}

    # Specify the path to the directory containing the .txt files
    directory_path = '../datasets/food_dataset/ingredients/train/labels'  # Change this to your directory

    # Call the function to update the label files
    update_label_files(label_map, directory_path)
