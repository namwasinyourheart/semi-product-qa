import pickle
import json
import os
import torch.nn as nn

from sklearn.model_selection import train_test_split

from datetime import datetime

def get_current_date():
    """
    Get the current date in the format YYYY-MM-DD.

    Returns:
        str: The current date in the format YYYY-MM-DD.
    """
    return datetime.today().strftime('%Y%m%d')

# # Example usage:
# current_date = get_current_date()
# print("Current date:", current_date)


def save_to_txt_file(content, filename):
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(content)
        print("Content has been saved to", filename)
    except Exception as e:
        print("An error occurred:", str(e))

def count_elements_in_values(my_dict):
    counts = {}
    
    for key, value in my_dict.items():
        counts[key] = len(value)
    
    return counts

def download_ggderive_file(url, output=None):
    gdown.download(url, output)

def download_ggdrive_folder(url, output=None):

    if url.split('/')[-1] == '?usp=sharing':
        url= url.replace('?usp=sharing','')
    gdown.download_folder(url, output)


def load_pickle(pickle_path):
    """Utility function for loading .pkl pickle files.

    Arguments
    ---------
    pickle_path : str
        Path to pickle file.

    Returns
    -------
    out : object
        Python object loaded from pickle.
    """
    with open(pickle_path, "rb") as f:
        out = pickle.load(f)
    return out

    
def save_pickle(data, save_path):
    with open(save_path, 'wb') as file:
        pickle.dump(data, file)
    print(f'Saved to {save_path}.')
    

def save_list_to_txt_file(list, save_path):
    with open(save_path, 'w') as f:
        f.write('\n'.join(list))
    print(f'Saved to {save_path}.')


def load_txt_file(txt_file_path):
    with open(txt_file_path, 'r') as f:
        lines = f.readlines()

    lines = [line.strip() for line in lines]

    return lines

def save_dict_to_txt(dictionary, filename):
    # Convert the dictionary to a JSON-formatted string
    json_data = json.dumps(dictionary, indent=4)  # indent for pretty formatting, optional

    # Write the JSON data to a text file
    with open(filename, 'w') as file:
        file.write(json_data)

def load_dict_from_txt(filename):
    try:
        # Read the JSON data from the text file
        with open(filename, 'r') as file:
            json_data = file.read()

        # Convert the JSON data to a Python dictionary
        dictionary = json.loads(json_data)
        
        return dictionary

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: Unable to decode JSON from file '{filename}'.")
        return None

def is_file(file_path):
    return os.path.exists(file_path)


# Simple MLP
class MLP(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(MLP, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        return x




def split_data_with_stratification(X, y, test_size=0.1, random_state=42):
    """
    Split the data into training, development, and test sets while ensuring class stratification.

    Parameters:
    - X: Features
    - y: Labels
    - test_size: Proportion of the dataset to include in the test split
    - random_state: Seed for random number generation

    Returns:
    A dictionary containing three splits: 'train', 'dev', and 'val', each with 'X' (features) and 'y' (labels).
    """
    # Split the data into training (80%) and temporary (20%)
    X_train_temp, X_temp, y_train_temp, y_temp = train_test_split(
        X, y, test_size=2*test_size, random_state=random_state, stratify=y
    )

    # Split the temporary data into development (50%) and validation (50%)
    X_dev, X_test, y_dev, y_test = train_test_split(
        X_temp, y_temp, test_size=0.5, random_state=random_state, stratify=y_temp
    )

    return {
        'train': {'X': X_train_temp, 'y': y_train_temp},
        'dev': {'X': X_dev, 'y': y_dev},
        'test': {'X': X_test, 'y': y_test}
    }
def generate_directory_tree(root_path, max_items_per_level=5, depth=0):
    if depth == 0:
        print(root_path)

    # List all entries (files and directories) in the current directory
    entries = os.listdir(root_path)

    # Separate directories and files
    subdirectories = []
    files = []

    for entry in entries:
        full_path = os.path.join(root_path, entry)
        if os.path.isdir(full_path):
            subdirectories.append(entry)
        else:
            files.append(entry)


    # for i, subdirectory in enumerate(subdirectories[:max_items_per_level]):
    #     print(f"{'  ' * depth}|-- {subdirectory}")
    #     generate_directory_tree(os.path.join(root_path, subdirectory), max_items_per_level, depth + 1)

    # # Display the head of each file name up to max_items_per_level files
    # for i, file in enumerate(files[:max_items_per_level]):
    #     file_name_parts = file.split('_')
    #     if len(file_name_parts) > 5:
    #         file_head = '_'.join(file_name_parts[:5])
    #     else:
    #         file_head = file
    #     print(f"{'  ' * depth}|-- {file_head}")


    # Display up to max_items_per_level subdirectories
    for i, subdirectory in enumerate(subdirectories[:max_items_per_level]):
        prefix = "│   " * depth + "├── "
        print(f"{prefix}{subdirectory}")
        generate_directory_tree(os.path.join(root_path, subdirectory), max_items_per_level, depth + 1)

    # # Display the head of each file name up to max_items_per_level files
    for i, file in enumerate(files[:max_items_per_level]):
        prefix = "│   " * depth + "├── "
        file_name_parts = file.split('_')
        if len(file_name_parts) > 5:
            # file_head = '_'.join(file_name_parts[:])
            file_head = file
        else:
            file_head = file
        print(f"{prefix}{file_head}")

def count_files(directory):
        count = 0
        for root, dirs, files in os.walk(directory):
            count += len(files)
        return count

def colabpath_to_vscodepath():
    pass

def extract_relative_path(full_path, base_path):
    return os.path.relpath(full_path, base_path)