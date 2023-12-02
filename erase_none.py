import json

def filter_and_update(input_file, existing_output_file, output_file):
    # Read the existing output file
    with open(existing_output_file, 'r') as f:
        existing_data = json.load(f)

    # Read the input file
    with open(input_file, 'r') as f:
        input_data = json.load(f)
    count = 0
    examples = []
    # Update the existing data and remove keys with third key phrase as "None"
    for example_key, example_value in input_data.items():
        if (type(example_value) == str):
            continue
        key_phrases = example_value.get('key_phrases', [])
        if key_phrases and key_phrases[2] != "None":
            pass
        elif example_key in existing_data:
            count += 1
            examples.append(example_key.split('_')[-1])
            del existing_data[example_key]
    print("number of files with 3rd phrase as none = ", count)
    print("list of file numbers = ", examples)
    # Write the updated data to the output file
    with open(output_file, 'w') as f:
        json.dump(existing_data, f, indent=2)

if __name__ == "__main__":
    input_json_file = "data/outputs/tracked/baseline/yelpshort_gpt_output_baseline.json"  # replace with your input file path
    existing_output_json_file = "data/inputs/three_changes/yelpshort_dataset_opposite_three_change.json"  # replace with your existing output file path
    output_json_file = "updated_three_change_output.json"  # replace with your output file path

    filter_and_update(input_json_file, existing_output_json_file, output_json_file)
