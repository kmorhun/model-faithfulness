import json
import numpy as np

# When working with the data outputs, you can generally assume that the first "COMMENT_" has been removed

def load_json(file_path) -> dict:
    with open(file_path, 'r') as file:
        data = json.load(file)
    data.pop("COMMENT_")
    return data

def output_profile(output_file_path, error_file_path) -> None:
    """
    Generates some basic statistics about a particular data output and its errors
    """
    output_data = load_json(output_file_path)
    error_data = load_json(error_file_path)

    num_successful = len(output_data.keys())
    num_failed = len(error_data.keys())

    print("Dataset: ", output_file_path)
    print("Number of successful examples = ", num_successful)
    print("Number of failed examples = ", num_failed)

    for sentiment in range(6): #0, 1, 2, 3, 4, 5
        get_percent_with_sentiment(output_file_path, sentiment)

    error_example_names = get_names(error_data)
    print(f"Examples which caused an error: {error_example_names}")

def count_sentiments_by_example(file1, file2, type) -> dict[str, int] | None:
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
    for example_key in data1.keys():
        sentiment1 = data1[example_key].get('sentiment', None)
        if sentiment1 is not None:
            sentiment_counts['file1_'+ str(sentiment1)] += 1
    
    for example_key in data2.keys():
        sentiment2 = data2[example_key].get('sentiment', None)
        if sentiment2 is not None:
            sentiment_counts['file2_'+ str(sentiment2)] += 1
    
    ####COMPARING OUTPUTS####
    for example_key in data1.keys():
        sentiment1 = data1[example_key].get('sentiment', None)
        sentiment2 = data2.get(example_key, {}).get('sentiment', None)

        if sentiment1 is not None and sentiment2 is not None:
            ####OVERLAPPING EXAMPLES#####
            sentiment_counts['num_overlapping_examples'] += 1
            ####SENTIMENT COMPARISON#####
            if sentiment1 == sentiment2:
                sentiment_counts['same'] += 1
            else:
                sentiment_counts['different'] += 1

    return sentiment_counts

def get_names(data, to_print=True) -> list[str]:
    """ 
    given a json dictionary containing the reviews, get a list of all the example names
    Useful for getting a list of the error examples, or all examples with sentiment x for manual review
    """
    names = list(data.keys())
    print(names)
    return names

def get_reviews_with_sentiment(filepath, sentiment, to_print=True) -> dict:
    """
    returns a dictionary filtering reviews by the sentiment given (0, 1, 2, 3, 4, 5).
    If the sentiment doesn't exist in the dataset, an empty dictionary is returned
    """
    data = load_json(filepath)
    result = {k:v for k,v in data.items() if v["sentiment"] == sentiment}
    result_len = len(result.keys())
    if to_print:
        print(f"Found {result_len} reviews with sentiment {sentiment}")
    return result

def get_percent_with_sentiment(filepath, sentiment, to_print=True) -> float | None:
    """
    returns the percent of reviews in the given dictionary with the given sentiment. 
    If the sentiment doesn't exist in the dictionary, return 0
    """
    data = load_json(filepath)
    total_reviews = len(data.keys())
    reviews_with_sentiment = get_reviews_with_sentiment(filepath, sentiment, print)
    
    try:
        percent = len(reviews_with_sentiment.keys())/total_reviews
        if to_print:
            print(f"{percent*100}% of reviews in this data have sentiment {sentiment}")
        return percent
    except ZeroDivisionError:
        print("ERROR: data is empty")
        return None

def compare_confidence_by_sentiment(before_change_data, after_change_data) -> None:
    """
    before_change_data and after_change_data are both dictionary objects

    feel free to add more bits of analysis if you want
    """
    pass
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
movieshort_gradient = gradient_path + 'movieshort_gpt_output_gradient.json'

movieshort_baseline_errors = baseline_path + 'movieshort_gpt_errors_baseline.json'
movieshort_one_change_errors = one_change_path + 'movieshort_gpt_errors_one_change.json'
movieshort_two_change_errors = two_change_path + 'movieshort_gpt_errors_two_change.json'
movieshort_three_change_errors = three_change_path + 'movieshort_gpt_errors_three_changes.json'
movieshort_gradient_errors = gradient_path + 'movieshort_gpt_errors_gradient.json'

yelpshort_baseline = baseline_path + 'yelpshort_gpt_output_baseline.json'
yelpshort_one_change = one_change_path + 'yelpshort_gpt_output_one_change.json'
yelpshort_two_change = two_change_path + 'yelpshort_gpt_output_two_change.json'
yelpshort_three_change = three_change_path + 'yelpshort_gpt_output_three_changes.json'
yelpshort_gradient = gradient_path + 'yelpshort_gpt_output_gradient.json'

yelpshort_baseline_errors = baseline_path + 'yelpshort_gpt_errors_baseline.json'
yelpshort_one_change_errors = one_change_path + 'yelpshort_gpt_errors_one_change.json'
yelpshort_two_change_errors = two_change_path + 'yelpshort_gpt_errors_two_change.json'
yelpshort_three_change_errors = three_change_path + 'yelpshort_gpt_errors_three_changes.json'
yelpshort_gradient_errors = gradient_path + 'yelpshort_gpt_errors_gradient.json'

#EXAMPLE USAGE
# print(output_profile(yelpshort_three_change, yelpshort_three_change_errors))

# result = count_sentiments_by_example(movieshort_two_change, movieshort_one_change, 'movie')
# print("Results", result)