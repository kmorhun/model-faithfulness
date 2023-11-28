import json

def load_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def count_sentiments_by_example(file1, file2):
    data1 = load_json(file1)
    data2 = load_json(file2)
    print(data1)

    sentiment_counts = {'same': 0, 'different': 0}

    first_example_processed = False

    for example_key in data1.keys():
        if not first_example_processed:
            first_example_processed = True
            continue  # Skip the first example
        sentiment1 = data1[example_key].get('sentiment', None)
        sentiment2 = data2.get(example_key, {}).get('sentiment', None)

        if sentiment1 is not None and sentiment2 is not None:
            if sentiment1 == sentiment2:
                sentiment_counts['same'] += 1
            else:
                sentiment_counts['different'] += 1

    return sentiment_counts

# Example usage:
file1_path = '/Users/zackduitz/Desktop/organized/MIT/MIT_3rd_year/6.8611 NLP/model-faithfulness/data/outputs/tracked/movie_gpt_output_2023_11_26-01_35_24.json'
file2_path = '/Users/zackduitz/Downloads/movie_gpt_one_change_output_2023_11_27-20_12_25.json'

result = count_sentiments_by_example(file1_path, file2_path)

print(f"Number of examples with the same sentiment: {result['same']}")
print(f"Number of examples with different sentiments: {result['different']}")