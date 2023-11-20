# This file contains the API calls to GPT 4
import os
import openai
from openai import OpenAI


# def get_gpt_completion(prompt, model = "gpt-3.5-turbo"):
#     messages = [{"role": "user", "content": prompt}]

#     response = openai.Completion.create(

#     model=model,

#     messages=messages,

#     temperature=0,

#     )

#     return response.choices[0].message["content"]


# def generate_chat_response(prompt):
#     response = openai.Completion.create(
#         engine='text-davinci-003',
#         prompt=prompt,
#         max_tokens=50,
#         temperature=0.7,
#         n=1,
#         stop=None
#     )
#     return response.choices[0].text.strip()
prompt = """Please classify the sentiment of the following Yelp customer reviews of restaurants with a score from 1 (negative) to 5 (positive). Explain the reasoning for your classification by highlighting the most relevant phrases in the review used in analysis.

Human: Far away from real Chinese food. Doesn't even taste good as American style Chinese food. 

Assistant: 

Most important phrase: Doesn’t taste good
Second most important phrase: real Chinese food
Third most important phrase: Far away from
Any other important phrases: None

The speaker values real Chinese food over American style Chinese food, and they believe that the restaurant doesn’t measure up to their already lowered expectations of American style Chinese food. 

Final sentiment classification: 2
________________________________________________________________________________________________________

Human: Sushi selection limited...  Miso soup tasted a little fishy.

Assistant: 

Most important phrase: sushi selection limited
Second most important phrase: Miso soup tasted a little fishy
Third most important phrase: None
Any other important phrases: None

Sushi is often the main meal at a restaurant when it is available. A limited menu is disappointing, but not the end of the world. The speaker only had mild complaints about the soup 

Final sentiment classification: 3
________________________________________________________________________________________________________

Human: Meticulously organized and a great selection. Definitely worth a stop.

Assistant: 

Most important phrase: definitely worth a stop
Second most important phrase: great selection
Third most important phrase: meticulously organized
Any other important phrases: None

This customer thought the food selection is great, which is very important for a high rating. Also, the restaurant was organized, which could suggest that the place is well-kept, clean, and efficient. “Definitely worth a stop” is the most important phrase because it is a direct recommendation to eat at the restaurant.

Final sentiment classification: 5
________________________________________________________________________________________________________

Human: Excellent breakfast. Regular pancakes rocked. Staff was super and we were seated immediately on a Saturday. So lucky. My first 5 star rating on Yelp.

In JSON format Assistant:
"""

prompt_2 = """
Please classify the sentiment of the following Yelp customer reviews of restaurants with a score from 1 (negative) to 5 (positive). Explain the reasoning for your classification by highlighting the most relevant phrases in the review used in analysis.

Human: Far away from real Chinese food. Doesn't even taste good as American style Chinese food. 

Assistant: 

Most important phrase: Doesn’t taste good
Second most important phrase: real Chinese food
Third most important phrase: Far away from
Any other important phrases: None

The speaker values real Chinese food over American style Chinese food, and they believe that the restaurant doesn’t measure up to their already lowered expectations of American style Chinese food. 

Final sentiment classification: 2
________________________________________________________________________________________________________

Human: Sushi selection limited...  Miso soup tasted a little fishy.

Assistant: 

Most important phrase: sushi selection limited
Second most important phrase: Miso soup tasted a little fishy
Third most important phrase: None
Any other important phrases: None

Sushi is often the main meal at a restaurant when it is available. A limited menu is disappointing, but not the end of the world. The speaker only had mild complaints about the soup 

Final sentiment classification: 3
________________________________________________________________________________________________________

Human: Meticulously organized and a great selection. Definitely worth a stop.

Assistant: 

Most important phrase: definitely worth a stop
Second most important phrase: great selection
Third most important phrase: meticulously organized
Any other important phrases: None

This customer thought the food selection is great, which is very important for a high rating. Also, the restaurant was organized, which could suggest that the place is well-kept, clean, and efficient. “Definitely worth a stop” is the most important phrase because it is a direct recommendation to eat at the restaurant.

Final sentiment classification: 5
________________________________________________________________________________________________________

Human: Excellent breakfast. Regular pancakes rocked. Staff was super and we were seated immediately on a Saturday. So lucky. My first 5 star rating on Yelp.

Assistant: 

Most important phrase: my first 5 star rating
Second most important phrase: excellent breakfast
Third most important phrase: staff was super
Any other important phrases: so lucky, pancakes rocked

This customer was so excited about this restaurant that they felt compelled to write a review for the first time, indicating extraordinary satisfaction. They thought the food and service were also very good. Saturdays are busy times for restaurants, so the customer was pleasantly surprised to not have to wait very long to be seated. 

Final sentiment classification: 5
________________________________________________________________________________________________________

Human: Had the gnocchi delivered. Absolutely terrible. Gnocci's had to have been 2 years old. Delivery guy was shady too.

Assistant: 

Most important phrase: absolutely terrible
Second most important phrase: Gnocci’s had to have been 2 years old
Third most important phrase: Delivery guy was shady
Any other important phrases: had the gnocchi delivered

The implication here is that the customer did not receive fresh gnocchi when they had them delivered, and they exaggerate their discontent with hyperbole, claiming the gnocchi were 2 years old. They may have also felt unsafe around the delivery guy, contributing to their bad experience.

Final sentiment classification: 1
________________________________________________________________________________________________________



"""
prompt_3 = """
Please classify the following Yelp review's sentiment on a scale of 1 (most negative) to 5 (most positive). Explain the reasoning for your classification by highlighting the most relevant phrases in the review used in analysis. Return the answer in JSON format.

Human: Sushi selection limited...  Miso soup tasted a little fishy.

Assistant:
"""
def test():
    client = OpenAI()
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt_3,
                
            }
        ],
        model="gpt-4-1106-preview",
        temperature = 0.1,
        response_format={ "type": "json_object" }
    )
    print(chat_completion.choices[0].message.content)
    print()
    print(chat_completion.choices[0].finish_reason)
   


