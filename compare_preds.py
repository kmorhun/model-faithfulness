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

def analyze_confidence(confidence_swings):
    # want the number of confidence swings and the number of and number unchanged percent of both
    # want other things abut it also 
    total = 0
    positive_swing = 0
    negative_swing = 0
    zero_swing = 0
    total_shift = []
    for swing in confidence_swings:
        total += 1
        if swing > 0:
            positive_swing += 1
            total_shift.append(swing)
        elif swing < 0:
            negative_swing += 1
            total_shift.append(swing)
        else:
            zero_swing += 1
            total_shift.append(swing)
    print()
    print("Total Swings = ", total)
    print("Positive Swings = ", positive_swing)
    print("Negative Swings = ", negative_swing)
    print("Zero Swing = ", zero_swing)
    print("Average Swing = ", sum(total_shift) / total)
    print("Average Swing = ", np.mean(total_shift))
    print("Median Swing = ", np.median(total_shift))

def count_sentiments_by_example(file1, file2, type, exclude_keys = None):
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
        sentiment_counts = {'file1_1': 0, 'file1_2': 0, 'file1_3': 0, 'file1_4': 0, 'file1_5': 0, 'file2_1': 0, 'file2_2': 0, 'file2_3': 0, 'file2_4': 0, 'file2_5': 0, 'same': 0, 'different': 0, 'num_overlapping_examples': 0, "correct_direction": 0, "wrong_direction": 0}
    else:
        print("Type must be movie or restaurant. Cancelling analysis...")
        return

    ####RAW SENTIMENT COUNTS#####
    for example_key in data1.keys():
        if exclude_keys and example_key in exclude_keys:
            continue
        sentiment1 = data1[example_key].get('sentiment', None)
        if sentiment1 is not None:
            sentiment_counts['file1_'+ str(sentiment1)] += 1
    
    for example_key in data2.keys():
        if exclude_keys and example_key in exclude_keys:
            continue
        sentiment2 = data2[example_key].get('sentiment', None)
        if sentiment2 is not None:
            sentiment_counts['file2_'+ str(sentiment2)] += 1
    confidence_swings = []
    examples_w_different_sentiment = []
    ####COMPARING OUTPUTS####
    for example_key in data1.keys():
        if exclude_keys and example_key in exclude_keys:
            continue
        sentiment1 = data1[example_key].get('sentiment', None)
        sentiment2 = data2.get(example_key, {}).get('sentiment', None)

        confidence1 = data1[example_key].get('confidence', None)
        confidence2 = data2.get(example_key, {}).get('confidence', None)
        # print(confidence1, "      ", confidence2)
        total_count = 0
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
                examples_w_different_sentiment.append(example_key)
            if (type == "restaurant"):
                if sentiment1 != sentiment2:
                    if sentiment1 < 2:
                        if sentiment2 >= 2:
                            sentiment_counts["correct_direction"] += 1
                        else:
                            sentiment_counts["wrong_direction"] += 1
                    if sentiment1 > 2:
                        if sentiment2 <= 2:
                            sentiment_counts["correct_direction"] += 1
                        else:
                            sentiment_counts["wrong_direction"] += 1
                    if sentiment1 != 0 and sentiment1 != 4:
                        total_count += 1
    # print("Confidence = ", confidence_swings)
    print("sentiment_changed and not equal to 0 or 4", total_count)
    if exclude_keys:
        examples_w_different_sentiment.extend(exclude_keys)
    return sentiment_counts, confidence_swings, examples_w_different_sentiment

def get_names(data, to_print=True) -> list[str]:
    """ 
    given a json dictionary containing the reviews, get a list of all the example names
    Useful for getting a list of the error examples, or all examples with sentiment x for manual review
    """
    names = list(data.keys())
    print(names)
    return names

def get_reviews_with_sentiment_from_data(data, sentiment, to_print=True) -> dict:
    """
    This is different from the one below because it uses the dictionary directly, not the filepath
    returns a dictionary filtering reviews by the sentiment given (0, 1, 2, 3, 4, 5).
    If the sentiment doesn't exist in the dataset, an empty dictionary is returned
    """
    result = {k:v for k,v in data.items() if v["sentiment"] == sentiment}
    result_len = len(result.keys())
    if to_print:
        print(f"Found {result_len} reviews with sentiment {sentiment}")
    return result

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

def trim_to_overlapping_reviews(file1, file2, to_print=True):
    """
    Given two file paths leading to output files,
    returns two new output files that are trimmed to have the same reviews between them. 
    """
    data1 = load_json(file1)
    data2 = load_json(file2)

    new_data1 = {}
    new_data2 = {}
    # print(data1)
    
    ####COMPARING OUTPUTS####
    for example_key in data1.keys():
        entry1 = data1[example_key]
        entry2 = data2.get(example_key, None)

        if entry1 is not None and entry2 is not None:
            ####OVERLAPPING EXAMPLES#####
            new_data1[example_key] = entry1
            new_data2[example_key] = entry2

    if to_print:
        print(f"number of reviews in data1: {len(new_data1.keys())}")
        print(f"number of reviews in data2: {len(new_data2.keys())}")
    return new_data1, new_data2


def compare_confidence_by_unchanged_sentiment(before_change_filepath, after_change_filepath, to_print=True) -> None:
    """
    before_change_data and after_change_data are both dictionary objects with the same number of reviews
    These should have the same reviews in them

    This looks at reviews that *don't* change sentiment after the data is modified
    """

    data1, data2 = trim_to_overlapping_reviews(before_change_filepath, after_change_filepath)

    result = {}
    for sentiment in range(6): # 0, 1, 2, 3, 4, 5
        result[sentiment] = {"average_confidence_shift": 0.0, "median_confidence_shift": 0.0}
        data1_with_sentiment = get_reviews_with_sentiment_from_data(data1, sentiment)

        confidence_diffs = np.array((0,))
        for name in data1_with_sentiment.keys(): #only look through reviews that have this sentiment
            sentiment_after = data2[name]["sentiment"]

            if sentiment == sentiment_after:
                #this review didn't change sentiment! What happened to the confidence?
                confidence_diff = data2[name]["confidence"] - data1[name]["confidence"]
                confidence_diffs = np.append(confidence_diffs, confidence_diff)
        
        result[sentiment]["average_confidence_shift"] = np.mean(confidence_diffs)
        result[sentiment]["median_confidence_shift"] = np.median(confidence_diffs)
    if to_print:
        print(result)
    return result

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

movielong_baseline = baseline_path + 'movielong_gpt_output_2023_11_30-16_11_45.json'
movielong_one_change = one_change_path + 'movielong_gpt_output_one_change2023_12_09-19_53_55.json'
movielong_two_change = two_change_path + 'movielong_gpt_output_two_changes.json'
movielong_three_change = three_change_path + 'movielong_gpt_output_3_change.json'

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

yelplong_baseline = baseline_path + 'yelplong_gpt_output_baseline.json'
yelplong_one_change = one_change_path + 'yelplong_gpt_output_one_change.json'
yelplong_two_change = two_change_path + 'yelplong_gpt_output_two_change.json'
yelplong_three_change = three_change_path + 'yelplong_gpt_output_three_changes.json'

yelpshort_baseline_errors = baseline_path + 'yelpshort_gpt_errors_baseline.json'
yelpshort_one_change_errors = one_change_path + 'yelpshort_gpt_errors_one_change.json'
yelpshort_two_change_errors = two_change_path + 'yelpshort_gpt_errors_two_change.json'
yelpshort_three_change_errors = three_change_path + 'yelpshort_gpt_errors_three_changes.json'
yelpshort_gradient_errors = gradient_path + 'yelpshort_gpt_errors_gradient.json'

#EXAMPLE USAGE
# output_profile(yelpshort_three_change, yelpshort_three_change_errors)

sentiment_counts, confidence_swings, changed_keys = count_sentiments_by_example(yelplong_baseline, yelplong_one_change, 'restaurant')
print("Results", sentiment_counts)
analyze_confidence(confidence_swings)
print()
# print("STARTING SECOND EXPERIMENT")
# sentiment_counts2, confidence_swings2, changed_keys2 = count_sentiments_by_example(yelplong_baseline, yelplong_two_change, 'restaurant', exclude_keys = changed_keys)
# print("Results", sentiment_counts2)
# analyze_confidence(confidence_swings2)
# print()
# print("STARTING Third EXPERIMENT")
# sentiment_counts3, confidence_swings3, changed_keys3 = count_sentiments_by_example(yelplong_baseline, yelplong_three_change, 'restaurant', exclude_keys = changed_keys2)
# print("Results", sentiment_counts3)
# analyze_confidence(confidence_swings3)

# print(f"Number of examples with the same sentiment: {result['same']}")
# print(f"Number of examples with different sentiments: {result['different']}")
# result = count_sentiments_by_example(yelpshort_two_change, yelpshort_three_change, 'restaurant')
# print("Results", result)

# compare_confidence_by_unchanged_sentiment(movieshort_baseline, movieshort_one_change)
