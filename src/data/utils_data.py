import os
import json

import matplotlib.pyplot as plt

PRODUCT_DATA_PATHS = {
    'phone': 'save/output-scraping-tgdd/product_data/phone_products_20240406_203410.json',
    'tablet': 'save/output-scraping-tgdd/product_data/tablet_products_20240406_211406.json',
    'laptop': 'save/output-scraping-tgdd/product_data/laptop_products_20240407_113058.json'
    }


QNA_DIRS = {

    'phone': 'save/data-synthesis/qna_dtdd__1_20apq_1/20240406',
    'tablet': 'save/data-synthesis/qna_tablet_1_20apq/20240407',
    'laptop': 'save/data-synthesis/qna_laptop_1_20apq/20240407'

}

def load_product_data(product_id, product_data_paths):
    product_data_dict = get_all_product_data(product_data_paths)

    product_type = product_id.split('-')[0]
    product_type = product_type_map[product_type]

    return product_data_dict[product_type][product_id]

def get_all_product_data(product_data_paths):
    product_data_dict = {}
    for product_type, product_path  in product_data_paths.items():
        with open(product_path, 'r', encoding='utf-8') as file:
            product_data_dict[product_type] ={}
            for line in file:
                product_data = json.loads(line)
                product_id = product_data['product_id']
                product_data_dict[product_type][product_id] = product_data

    return product_data_dict

product_type_map = {
    'dtdd': 'phone',
    'may-tinh-bang': 'tablet',
    'laptop': 'laptop'
}

def load_qna_data(product_id, qna_dir):

    def get_qna_path_mapping(qna_dir):
        # Map product_id to its corresponding qa json path
        all_qna_paths = [fp for fp in os.listdir(qna_dir) if fp.endswith('.json')]
        qna_path_mapping = {}

        
        for qna_path in all_qna_paths:
            if qna_path.startswith('qna_'):
                product_id = qna_path.split('_')[1]
                # print(product_id)
                full_path = os.path.join(qna_dir, qna_path)
                qna_path_mapping[product_id] = full_path
        # assert len(qna_path_mapping) == len(all_qna_paths), print(f'{len(qna_path_mapping)} != {len(all_qna_paths)}')
        return qna_path_mapping
    
    product_type = product_id.split('-')[0]
    product_type = product_type_map[product_type]

    get_qna_path_mapping = get_qna_path_mapping(qna_dir[product_type])
    qna_file_path = get_qna_path_mapping[product_id]
    if os.path.exists(qna_file_path):
        with open(qna_file_path, 'r', encoding='utf-8') as qna_file:
            qna_data = json.load(qna_file)
        # return qna_data.get('questions', [])
            return qna_data
    else:
        return []

def plot_qa_counts(qa_counts):
    # Calculate total QA counts for each product type
    total_counts = {product_type: sum(qa_counts[product_type].values()) for product_type in qa_counts}

    # Prepare labels with percentage and count
    labels = [f"{product_type}\n{total_counts[product_type]} - {total_counts[product_type] / sum(total_counts.values()) * 100:.1f}%" for product_type in total_counts]

    # Bar chart
    plt.figure(figsize=(10, 6))

    # Create bars and iterate through them
    bars = plt.bar(total_counts.keys(), total_counts.values(), color='skyblue')
    for i, bar in enumerate(bars):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, height+2, f"{height} ({height / sum(total_counts.values()) * 100:.1f}%)", ha='center', va='bottom')

    plt.xlabel('Product Type')
    plt.ylabel('#QA Pairs')
    plt.title('Distribution of #QA Pairs')
    plt.ylim(0, max(total_counts.values()) * 1.1)  # Adjust the y-axis limit
    plt.show()

# # Sample data
# qa_counts = {
#     'Product1': {'QA1': 10, 'QA2': 20, 'QA3': 30},
#     'Product2': {'QA1': 15, 'QA2': 25, 'QA3': 35},
#     'Product3': {'QA1': 8, 'QA2': 12, 'QA3': 18}
# }

# # Plot the QA counts
# plot_qa_counts(qa_counts)


def plot_histogram_qa_counts(qa_counts):
    # Prepare a list to store the counts of product IDs
    counts = []

    # Iterate through product types and their corresponding product IDs and counts
    for product_type, product_data in qa_counts.items():
        for count in product_data.values():
            counts.append(count)

    # Define the bins for the histogram based on the range of QA counts
    bins = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

    # Create histogram
    plt.figure(figsize=(10, 6))
    frequencies, _, _ = plt.hist(counts, bins=bins, color='skyblue', edgecolor='black')

    # Label each bar by frequency
    for i in range(len(bins) - 1):
        plt.text((bins[i] + bins[i + 1]) / 2, frequencies[i], f"{int(frequencies[i])}", ha='center', va='bottom')

    plt.xlabel('#QA Pairs')
    plt.ylabel('#Products')
    plt.title('Histogram of #Product')
    plt.xticks(bins)
    plt.grid(axis='y', alpha=0.5)
    plt.show()


# # Plot the histogram
# plot_histogram_qa_counts(qa_counts)



def get_qna_path_mapping(qna_dir):
    # Map product_id to its corresponding qa json path
    all_qna_paths = [fp for fp in os.listdir(qna_dir) if fp.endswith('.json')]
    qna_path_mapping = {}

    
    for qna_path in all_qna_paths:
        if qna_path.startswith('qna_'):
            product_id = qna_path.split('_')[1]
            # print(product_id)
            full_path = os.path.join(qna_dir, qna_path)
            qna_path_mapping[product_id] = full_path
    # assert len(qna_path_mapping) == len(all_qna_paths), print(f'{len(qna_path_mapping)} != {len(all_qna_paths)}')
    return qna_path_mapping


# laptop_qna_path_mapping = get_qna_path_mapping(QNA_DIRS['laptop'])
# phone_qna_path_mapping = get_qna_path_mapping(QNA_DIRS['phone'])
# tablet_qna_path_mapping = get_qna_path_mapping(QNA_DIRS['tablet'])

def find_duplicates(lst):
    # Convert the list to a set to remove duplicates
    unique_items = set(lst)
    
    # If the lengths are different, there are duplicates
    if len(unique_items) != len(lst):
        # Return the duplicate items
        duplicates = [item for item in unique_items if lst.count(item) > 1]
        return duplicates
    else:
        return None  # No duplicates found

# # Example usage:
# my_list = id_list
# duplicates = find_duplicates(my_list)
# if duplicates:
#     print("Duplicates found:", duplicates)
# else:
#     print("No duplicates found.")
