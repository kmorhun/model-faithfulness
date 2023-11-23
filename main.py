import os
import openai
from flan_call import get_hugg_completion
from gpt_api import test
from transformers import T5Tokenizer, T5ForConditionalGeneration
import google.generativeai as palm
from dotenv import load_dotenv
from prompts import *

def run_gpt():
    # print(os.environ)
    # print(os.getenv("OPENAI_API_KEY"))
    os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
    openai_api_key = os.getenv("OPENAI_API_KEY")
    openai.api_key = openai_api_key
    # get_gpt_completion("What is your name?")
    test()


def run_hugg_flan():
    tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-base", token = os.getenv("HUGGING_FACE_KEY"))
    model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-base", token = os.getenv("HUGGING_FACE_KEY")) 
    prompt = create_prompt(PROMPT_TEMPLATE_FEW_SHOT, FORMATTED_EXAMPLE_TEMPLATE_1, NEW_EXAMPLE_JSON_TEMPLATE, ["example_1", "example_2"], PANCAKES_EXAMPLE)
    get_hugg_completion(prompt, tokenizer, model)
    get_hugg_completion("can you tell me what sport the following prompt relates too and give me your resoning? prompt: I like to shoot balls into a circle. Answer either: basketball, baseball", tokenizer, model)
    

def run_bard():
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/zackduitz/Downloads/first-website-374821-7893c1f2d758.json'
    palm.configure(api_key = os.getenv("PALM_KEY"))
    prompt = create_prompt(PROMPT_TEMPLATE_FEW_SHOT, FORMATTED_EXAMPLE_TEMPLATE_1, NEW_EXAMPLE_JSON_TEMPLATE, ["example_1", "example_2"], PANCAKES_EXAMPLE)
    response = palm.generate_text(prompt=prompt, model ='models/text-bison-001', temperature = 0.0, max_output_tokens = 1024)
    print( "From text-bison: ", response)
    response2 = palm.chat(messages=prompt, model ='models/chat-bison-001', temperature = 0.0)
    print("From chat-bison", response2.last)
    # for m in palm.list_models():
    #     print(m)

if __name__ == '__main__':
    # Get the absolute path to the directory containing this script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Load .env using the absolute path
    dotenv_path = os.path.join(script_dir, 'environment.env')
    load_dotenv(dotenv_path)

    # Run the different model tests
    # run_gpt()
    # run_bard()
    run_hugg_flan()

    