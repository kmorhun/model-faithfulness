# This file contains the API calls to GPT 4
import os
import openai
from openai import OpenAI


def get_gpt_completion(prompt, model = "gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]

    response = openai.Completion.create(

    model=model,

    messages=messages,

    temperature=0,

    )

    return response.choices[0].message["content"]


def generate_chat_response(prompt):
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=prompt,
        max_tokens=50,
        temperature=0.7,
        n=1,
        stop=None
    )
    return response.choices[0].text.strip()

def test():
    client = OpenAI()
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": "Say this is a test",
            }
        ],
        model="gpt-3.5-turbo",
    )
    print(chat_completion)



