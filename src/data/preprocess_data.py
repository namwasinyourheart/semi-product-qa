import json
import os
from tqdm import tqdm


def clean_product_ids(product_types, qna_dirs, tar_dirs):

    
    
    for product_type in product_types:
        print(product_type)
        
        qna_dir = qna_dirs[product_type]
        
        tar_dir  = tar_dirs[product_type]

        all_qna_files = [fn for fn in os.listdir(qna_dir) if fn.endswith('.json')]

        # Iterate over each JSON file
        for fn in tqdm(all_qna_files[:]):

            try:
                fp = os.path.join(qna_dir, fn)
                with open(fp, 'r', encoding='utf-8') as f:
                    qna = json.load(f)


                qna_str = str(qna)

                # Replace the product ID based on the product type
                if product_type == 'phone':
                    qna_str = qna_str.replace("'product_id': 'dtdd-", "'product_id': 'phone-")
                    qna_str = qna_str.replace('p_dtdd', 'p_phone')

                elif product_type == 'tablet':
                    qna_str = qna_str.replace("'product_id': 'may-tinh-bang-", "'product_id': 'tablet-")
                    qna_str = qna_str.replace('p_may-tinh-bang', 'p_tablet')
                

                qna_str = qna_str.replace("'questions':", "'questions_answers':")

                qna_str = qna_str.replace('\'', '"')

                qna = json.loads(qna_str)

                # Write the updated JSON data to a new file in the target directory
                with open(os.path.join(tar_dir, fn.replace('.json', '_cleaned.json')), 'w') as file:
                    json.dump(qna, file, indent=4,ensure_ascii=False)

            except:
                print("Error at fn:", fn)
                continue

# tar_dirs = {
#     'phone': 'data/tgdd_data/questions_and_answers/phone/cleaned',
#     'tablet': 'data/tgdd_data/questions_and_answers/tablet/cleaned',
#     'laptop': 'data/tgdd_data/questions_and_answers/laptop/cleaned'
# }
# qna_dirs = QNA_DIRS

# product_types = ['tablet', 'phone', 'laptop']
# clean_product_ids(product_types, qna_dirs, tar_dirs)


# clean_product_ids(product_types, qna_dirs, tar_dirs)

def flatten_dict(d, parent_key='', sep=': '):
    items = {}
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, dict):
            items.update(flatten_dict(v, new_key, sep=sep))
        else:
            items[new_key] = v
    return items

# product_data_flattened = [flatten_dict(line) for line in phone_list]
# df = pd.DataFrame(product_data_flattened)

def replace_list_values_with_string(json_file_path):
    """
    Replaces list values with string representation in each line of a JSON file.

    Args:
    json_file_path (str): The path to the JSON file.
    """

    def convert_lists_to_string(data):
        for key, value in data.items():
            if isinstance(value, list):
                # print(value)
                data[key] = ', '.join(value)
            elif isinstance(value, dict):
                convert_lists_to_string(value)

    # Read lines from the JSON file
    with open(json_file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Process each line
    for i, line in enumerate(lines):
        data = json.loads(line.strip())
        # Convert lists to string recursively
        convert_lists_to_string(data)
        # Replace the line with updated data
        lines[i] = json.dumps(data, ensure_ascii=False) + '\n'

    # Write the updated lines back to the file
    with open(json_file_path.replace('.json', '_cleaned.json'), 'w', encoding='utf-8') as f:
        f.writelines(lines)
