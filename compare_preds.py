import json
import numpy as np

def load_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def output_profile(output_file_path, error_file_path):
    output_data = load_json(output_file_path)
    error_data = load_json(error_file_path)

    num_successful = len(output_data.keys()) - 1 #account for comment at the beginning
    num_failed = len(error_data.keys()) - 1

    print("Dataset: ", output_file_path)
    print("Successful examples = ", num_successful)
    print("Failed examples = ", num_failed)

def analyze_confidence(confidence_swings):
    # want the number of confidence swings and the number of and number unchanged percent of both
    # want other things abut it also 
    total = 0
    positive_swing = 0
    negative_swing = 0
    zero_swing = 0
    for swing in confidence_swings:
        total += 1
        if swing > 0:
            positive_swing += 1
        elif swing < 0:
            negative_swing += 1
        else:
            zero_swing += 1
    print()
    print("Total Swings = ", total)
    print("Positive Swings = ", positive_swing)
    print("Negative Swings = ", negative_swing)
    print("Zero Swing = ", zero_swing)

def count_sentiments_by_example(file1, file2, type):
    """
    type is movie or restaurant
    """
    data1 = load_json(file1)
    data2 = load_json(file2)
    # print(data1)

    ####SETUP####
    if type == "movie":
        sentiment_counts = {'file1_1': 0, 'file1_0': 0, 'file2_1': 0, 'file2_0': 0, 'same': 0, 'different': 0, 'num_overlapping_examples': 0}
    elif type == "restaurant":
        sentiment_counts = {'file1_1': 0, 'file1_2': 0, 'file1_3': 0, 'file1_4': 0, 'file1_5': 0, 'file2_1': 0, 'file2_2': 0, 'file2_3': 0, 'file2_4': 0, 'file2_5': 0, 'same': 0, 'different': 0, 'num_overlapping_examples': 0}
    else:
        print("Type must be movie or restaurant. Cancelling analysis...")
        return

    ####RAW SENTIMENT COUNTS#####
    first_example_processed = False
    for example_key in data1.keys():
        if not first_example_processed:
            first_example_processed = True
            continue  # Skip the first example
        sentiment1 = data1[example_key].get('sentiment', None)
        if sentiment1 is not None:
            sentiment_counts['file1_'+ str(sentiment1)] += 1
    
    first_example_processed = False
    for example_key in data2.keys():
        if not first_example_processed:
            first_example_processed = True
            continue  # Skip the first example
        sentiment2 = data2[example_key].get('sentiment', None)
        if sentiment2 is not None:
            sentiment_counts['file2_'+ str(sentiment2)] += 1
    confidence_swings = []
    ####COMPARING OUTPUTS####
    first_example_processed = False
    for example_key in data1.keys():
        if not first_example_processed:
            first_example_processed = True
            continue  # Skip the first example
        sentiment1 = data1[example_key].get('sentiment', None)
        sentiment2 = data2.get(example_key, {}).get('sentiment', None)

        confidence1 = data1[example_key].get('confidence', None)
        confidence2 = data2.get(example_key, {}).get('confidence', None)
        # print(confidence1, "      ", confidence2)

        if sentiment1 is not None and sentiment2 is not None:
            ####OVERLAPPING EXAMPLES#####
            sentiment_counts['num_overlapping_examples'] += 1
            ####SENTIMENT COMPARISON#####
            if sentiment1 == sentiment2:
                sentiment_counts['same'] += 1
                if confidence2 and confidence1:
                    confidence_swings.append(int(confidence2) - int(confidence1))
            else:
                sentiment_counts['different'] += 1
    # print("Confidence = ", confidence_swings)
    return sentiment_counts, confidence_swings

# Example usage:
# file1_path = '/Users/zackduitz/Desktop/organized/MIT/MIT_3rd_year/6.8611 NLP/model-faithfulness/data/outputs/tracked/movie_gpt_output_2023_11_26-01_35_24.json'
# file2_path = '/Users/zackduitz/Downloads/movie_gpt_one_change_output_2023_11_27-20_12_25.json'

#USEFUL FILEPATHS
baseline_path = 'data/outputs/tracked/baseline/'
one_change_path = 'data/outputs/tracked/one_change/'
two_change_path = 'data/outputs/tracked/two_changes/'
three_change_path = 'data/outputs/tracked/three_changes/'
gradient_path = 'data/outputs/tracked/gradient/'

movieshort_baseline = baseline_path + 'movieshort_gpt_output_baseline.json'
movieshort_one_change = one_change_path + 'movieshort_gpt_output_one_change.json'
movieshort_two_change = two_change_path + 'movieshort_gpt_output_two_change.json'
movieshort_three_change = three_change_path + 'movieshort_gpt_output_three_changes.json'

movieshort_baseline_errors = baseline_path + 'movieshort_gpt_errors_baseline.json'
movieshort_one_change_errors = one_change_path + 'movieshort_gpt_errors_one_change.json'
movieshort_two_change_errors = two_change_path + 'movieshort_gpt_errors_two_change.json'
movieshort_three_change_errors = three_change_path + 'movieshort_gpt_errors_three_changes.json'

#EXAMPLE USAGE
print(output_profile(movieshort_three_change, movieshort_three_change_errors))
# print(output_profile(movieshort_one_change, movieshort_one_change_errors))

sentiment_counts, confidence_swings = count_sentiments_by_example(movieshort_baseline, movieshort_three_change, 'movie')
print("Results", sentiment_counts)
analyze_confidence(confidence_swings)
# print(f"Number of examples with the same sentiment: {result['same']}")
# print(f"Number of examples with different sentiments: {result['different']}")