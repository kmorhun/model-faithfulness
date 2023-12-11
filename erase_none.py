import json

def filter_and_update(input_file, existing_output_file, output_file, changed_list = []):
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
        if example_key not in changed_list and key_phrases and key_phrases[2] != "None":
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
    input_json_file = "data/outputs/tracked/baseline/movielong_gpt_output_2023_11_30-16_11_45.json"  # replace with your input file path
    existing_output_json_file = "data/inputs/three_change/movielong_dataset_opposite_three_change.json"  # replace with your existing output file path
    output_json_file = "data/inputs/three_change/movielong_three_change_output.json"  # replace with your output file path


    used = ['Example_2', 'Example_4', 'Example_7', 'Example_10', 'Example_13', 'Example_18', 'Example_24', 'Example_25', 'Example_30', 'Example_31', 'Example_34', 'Example_43', 'Example_50', 'Example_52', 'Example_54', 'Example_62', 'Example_64', 'Example_65', 'Example_74', 'Example_77', 'Example_79', 'Example_83', 'Example_84', 'Example_86', 'Example_88', 'Example_92', 'Example_96', 'Example_99', 'Example_101', 'Example_102', 'Example_103', 'Example_106', 'Example_114', 'Example_117', 'Example_122', 'Example_123', 'Example_140', 'Example_143', 'Example_146', 'Example_148', 'Example_163', 'Example_170', 'Example_172', 'Example_192', 'Example_203', 'Example_206', 'Example_229', 'Example_237', 'Example_242', 'Example_253', 'Example_263', 'Example_265', 'Example_267', 'Example_271', 'Example_276', 'Example_281', 'Example_285', 'Example_288', 'Example_300', 'Example_1', 'Example_3', 'Example_6', 'Example_8', 'Example_11', 'Example_12', 'Example_14', 'Example_17', 'Example_19', 'Example_20', 'Example_21', 'Example_23', 'Example_29', 'Example_32', 'Example_35', 'Example_36', 'Example_38', 'Example_39', 'Example_40', 'Example_45', 'Example_46', 'Example_56', 'Example_57', 'Example_58', 'Example_60', 'Example_63', 'Example_66', 'Example_67', 'Example_68', 'Example_69', 'Example_70', 'Example_73', 'Example_76', 'Example_81', 'Example_82', 'Example_87', 'Example_89', 'Example_90', 'Example_91', 'Example_93', 'Example_95', 'Example_100', 'Example_104', 'Example_107', 'Example_108', 'Example_109', 'Example_110', 'Example_111', 'Example_115', 'Example_116', 'Example_118', 'Example_120', 'Example_121', 'Example_124', 'Example_126', 'Example_127', 'Example_130', 'Example_132', 'Example_133', 'Example_134', 'Example_135', 'Example_137', 'Example_138', 'Example_139', 'Example_141', 'Example_147', 'Example_149', 'Example_150', 'Example_151', 'Example_152', 'Example_174', 'Example_179', 'Example_188', 'Example_198', 'Example_202', 'Example_204', 'Example_212', 'Example_231', 'Example_234', 'Example_235', 'Example_244', 'Example_247', 'Example_251', 'Example_261', 'Example_262', 'Example_264', 'Example_268', 'Example_270', 'Example_273', 'Example_283', 'Example_293']
    filter_and_update(input_json_file, existing_output_json_file, output_json_file, used)
