# This file contains the API calls to GPT 4
import os
import openai
from openai import OpenAI
from prompts import *

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
prompt_1 = create_prompt(PROMPT_TEMPLATE_FEW_SHOT, FORMATTED_EXAMPLE_TEMPLATE_1, NEW_EXAMPLE_JSON_TEMPLATE, ["example_1", "example_2", "example_3"], PANCAKES_EXAMPLE)
prompt_2 = create_prompt(PROMPT_TEMPLATE_ZERO_SHOT, None, NEW_EXAMPLE_JSON_TEMPLATE, [], PANCAKES_EXAMPLE, zero_shot=True)

def test():
    client = OpenAI()
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt_1,
            }
        ],
        model="gpt-4-1106-preview",
        temperature = 0.1,
        response_format={ "type": "json_object" }
    )
    print(chat_completion.choices[0].message.content)
    print()
    print(chat_completion.choices[0].finish_reason)
