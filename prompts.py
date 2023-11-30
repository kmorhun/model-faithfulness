import json
from string import Template

# This parentheses syntax allows you to define very long strings over multiple lines, for readability. 
# Note the lack of commas and spaces at the separators
PREFIX_1 = ("Please classify the sentiment of the following Yelp customer reviews of restaurants "
            "with a score from 1 (negative) to 5 (positive). Express the score as a number. Explain the reasoning for your classification "
            "by highlighting the most relevant phrases in the review used in analysis. Also please provide your confidence level in your prediction from 0 to 100.")
PREFIX_2 = ("Please classify the sentiment of the following IMDb reviews of movies "
            "with a score of either 0 (negative) or 1 (positive). Express the score as a number. Explain the reasoning for your classification "
            "by highlighting the most relevant phrases in the review used in analysis. Also please provide your confidence level in your prediction from 0 to 100.")

# The following are creating a series of nested templates for generating prompts. See create_prompt for an example using templates
EXAMPLE_TEMPLATE = ("Human: $review\nAssistant:\nMost important phrase: $first\nSecond most important phrase: $second\n"
        "Third most important phrase: $third\nAny other important phrases: $other\nExplanation: $explanation\nFinal Sentiment Classification: $sentiment\nConfidence: $confidence")
FORMATTED_EXAMPLE_TEMPLATE_1 = Template(EXAMPLE_TEMPLATE)

NEW_EXAMPLE_TEMPLATE = Template("Human: $review\nAssistant:")
NEW_EXAMPLE_JSON_TEMPLATE = Template("Human: $review\n(In JSON Format) Assistant:")
PANCAKES_EXAMPLE = "Excellent breakfast. Regular pancakes rocked. Staff was super and we were seated immediately on a Saturday. So lucky. My first 5 star rating on Yelp."

PROMPT_TEMPLATE_FEW_SHOT_RESTAURANT = Template(f"{PREFIX_1}\n\n$examples\n\n$prompt")
PROMPT_TEMPLATE_ZERO_SHOT_RESTAURANT = Template(f"{PREFIX_1}\n$prompt")

PROMPT_TEMPLATE_FEW_SHOT_MOVIE = Template(f"{PREFIX_2}\n\n$examples\n\n$prompt")
PROMPT_TEMPLATE_ZERO_SHOT_MOVIE = Template(f"{PREFIX_2}\n$prompt")

def create_prompt(examples_json_filepath, prompt_template, formatted_example_template, new_example_template, example_names, new_example, zero_shot=False):
    """
    A method of generating sample prompts for testing purposes, given the name for an example in examples.json
    
    Params:
        examples_json_filepath (str): the filepath to the examples json file
        prompt_template (Template): the Template object describing the high-level prompt structure
        formatted_example_template (Template): the Template object describing how to format an example
        new_example_template (Template): the Template object describing how to format a new example
        example_names (list[str]): a list of example names which correspond to examples.json
        new_example (str): the string body of a new review
        zero_shot (bool): whether or not this is a zero-shot prompt. By default False. If this is true, only the prompt_template, new_example, examples_json_filepath, and formatted_example_template variables matter

    Returns: A formatted string representing the prompt to input into a model
    """
    if (zero_shot):
        new_review = new_example_template.substitute({"review": new_example})
        return prompt_template.substitute({"prompt": new_review})

    example_strings = []
    with open(examples_json_filepath) as examples_file:
        examples = json.load(examples_file)

        for name in example_names:
            example = examples[name]
            
            #formatting the example into a string
            values = {"first": "None", "second": "None", "third": "None", "other": "None"} # default values
            values["review"] = example["review"]
            values["explanation"] = example["explanation"]
            values["sentiment"] = str(example["sentiment"])
            values["confidence"] = str(example["confidence"])
            phrases = example["key_phrases"]
            if len(phrases) >= 1: 
                values["first"] = phrases[0]

            if len(phrases) >= 2: 
                values["second"] = phrases[1]
            
            if len(phrases) >= 3: 
                values["other"] = ", ".join(phrases[2:])
                
            example_strings.append(formatted_example_template.substitute(values))

    #format all few-shot examples. If there is only one example, this will also work
    examples = "\n\n".join(example_strings)
    new_review = new_example_template.substitute({"review": new_example})
    return prompt_template.substitute({"examples": examples, "prompt": new_review})

if __name__ == '__main__':
    #If you get UnicodeDecodeErrors, double check the text in your json file, especially quotation marks. 
    # Make sure these are ascii quotation marks
    
    with open("data/inputs/examples.json", "r", encoding="UTF-8") as examples_file:
        few_shot_examples = ["example_1", "example_2"]
        examples = json.load(examples_file)
        test_review = PANCAKES_EXAMPLE
        print(create_prompt("data/inputs/examples.json", PROMPT_TEMPLATE_FEW_SHOT_RESTAURANT, FORMATTED_EXAMPLE_TEMPLATE_1, NEW_EXAMPLE_JSON_TEMPLATE, few_shot_examples, test_review, zero_shot=False))