import json
from string import Template

# This parentheses syntax allows you to define very long strings over multiple lines, for readability. 
# Note the lack of commas and spaces at the separators
PREFIX_1 = ("Please classify the sentiment of the following Yelp customer reviews of restaurants "
            "with a score from 1 (negative) to 5 (positive). Express the score as a number. Explain the reasoning for your classification "
            "by highlighting the most relevant phrases in the review used in analysis.")
PREFIX_2 = ("Please classify the sentiment of the following IMDb reviews of movies "
            "with a score of either 0 (negative) or 1 (positive). Express the score as a number. Explain the reasoning for your classification "
            "by highlighting the most relevant phrases in the review used in analysis.")

# The following are creating a series of nested templates for generating prompts. See create_prompt for an example using templates
EXAMPLE_TEMPLATE = ("Human: $review\nAssistant:\nMost important phrase: $first\nSecond most important phrase: $second\n"
        "Third most important phrase: $third\nAny other important phrases: $other\nExplanation: $explanation\nFinal Sentiment Classification: $sentiment")
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
        
# prompt = """Please classify the sentiment of the following Yelp customer reviews of restaurants with a score from 1 (negative) to 5 (positive). Explain the reasoning for your classification by highlighting the most relevant phrases in the review used in analysis.

# Human: Far away from real Chinese food. Doesn't even taste good as American style Chinese food. 

# Assistant: 

# Most important phrase: Doesn’t taste good
# Second most important phrase: real Chinese food
# Third most important phrase: Far away from
# Any other important phrases: None

# The speaker values real Chinese food over American style Chinese food, and they believe that the restaurant doesn’t measure up to their already lowered expectations of American style Chinese food. 

# Final sentiment classification: 2
# ________________________________________________________________________________________________________

# Human: Sushi selection limited...  Miso soup tasted a little fishy.

# Assistant: 

# Most important phrase: sushi selection limited
# Second most important phrase: Miso soup tasted a little fishy
# Third most important phrase: None
# Any other important phrases: None

# Sushi is often the main meal at a restaurant when it is available. A limited menu is disappointing, but not the end of the world. The speaker only had mild complaints about the soup 

# Final sentiment classification: 3
# ________________________________________________________________________________________________________

# Human: Meticulously organized and a great selection. Definitely worth a stop.

# Assistant: 

# Most important phrase: definitely worth a stop
# Second most important phrase: great selection
# Third most important phrase: meticulously organized
# Any other important phrases: None

# This customer thought the food selection is great, which is very important for a high rating. Also, the restaurant was organized, which could suggest that the place is well-kept, clean, and efficient. “Definitely worth a stop” is the most important phrase because it is a direct recommendation to eat at the restaurant.

# Final sentiment classification: 5
# ________________________________________________________________________________________________________

# Human: Excellent breakfast. Regular pancakes rocked. Staff was super and we were seated immediately on a Saturday. So lucky. My first 5 star rating on Yelp.

# In JSON format Assistant:
# """

# prompt_2 = """
# Please classify the sentiment of the following Yelp customer reviews of restaurants with a score from 1 (negative) to 5 (positive). Explain the reasoning for your classification by highlighting the most relevant phrases in the review used in analysis.

# Human: Far away from real Chinese food. Doesn't even taste good as American style Chinese food. 

# Assistant: 

# Most important phrase: Doesn’t taste good
# Second most important phrase: real Chinese food
# Third most important phrase: Far away from
# Any other important phrases: None

# The speaker values real Chinese food over American style Chinese food, and they believe that the restaurant doesn’t measure up to their already lowered expectations of American style Chinese food. 

# Final sentiment classification: 2
# ________________________________________________________________________________________________________

# Human: Sushi selection limited...  Miso soup tasted a little fishy.

# Assistant: 

# Most important phrase: sushi selection limited
# Second most important phrase: Miso soup tasted a little fishy
# Third most important phrase: None
# Any other important phrases: None

# Sushi is often the main meal at a restaurant when it is available. A limited menu is disappointing, but not the end of the world. The speaker only had mild complaints about the soup 

# Final sentiment classification: 3
# ________________________________________________________________________________________________________

# Human: Meticulously organized and a great selection. Definitely worth a stop.

# Assistant: 

# Most important phrase: definitely worth a stop
# Second most important phrase: great selection
# Third most important phrase: meticulously organized
# Any other important phrases: None

# This customer thought the food selection is great, which is very important for a high rating. Also, the restaurant was organized, which could suggest that the place is well-kept, clean, and efficient. “Definitely worth a stop” is the most important phrase because it is a direct recommendation to eat at the restaurant.

# Final sentiment classification: 5
# ________________________________________________________________________________________________________

# Human: Excellent breakfast. Regular pancakes rocked. Staff was super and we were seated immediately on a Saturday. So lucky. My first 5 star rating on Yelp.

# Assistant: 

# Most important phrase: my first 5 star rating
# Second most important phrase: excellent breakfast
# Third most important phrase: staff was super
# Any other important phrases: so lucky, pancakes rocked

# This customer was so excited about this restaurant that they felt compelled to write a review for the first time, indicating extraordinary satisfaction. They thought the food and service were also very good. Saturdays are busy times for restaurants, so the customer was pleasantly surprised to not have to wait very long to be seated. 

# Final sentiment classification: 5
# ________________________________________________________________________________________________________

# Human: Had the gnocchi delivered. Absolutely terrible. Gnocci's had to have been 2 years old. Delivery guy was shady too.

# Assistant: 

# Most important phrase: absolutely terrible
# Second most important phrase: Gnocci’s had to have been 2 years old
# Third most important phrase: Delivery guy was shady
# Any other important phrases: had the gnocchi delivered

# The implication here is that the customer did not receive fresh gnocchi when they had them delivered, and they exaggerate their discontent with hyperbole, claiming the gnocchi were 2 years old. They may have also felt unsafe around the delivery guy, contributing to their bad experience.

# Final sentiment classification: 1
# ________________________________________________________________________________________________________



# """
# prompt_3 = """
# Please classify the following Yelp review's sentiment on a scale of 1 (most negative) to 5 (most positive). Explain the reasoning for your classification by highlighting the most relevant phrases in the review used in analysis. Return the answer in JSON format.

# Human: Sushi selection limited...  Miso soup tasted a little fishy.

# Assistant:
# """