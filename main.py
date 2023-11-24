import os
import openai
from flan_call import get_hugg_completion
from gpt_api import get_gpt_completion, gpt_save_output_json
from transformers import T5Tokenizer, T5ForConditionalGeneration
import google.generativeai as palm
from dotenv import load_dotenv
from prompts import *
from datetime import datetime

prompt_1 = create_prompt(PROMPT_TEMPLATE_FEW_SHOT, FORMATTED_EXAMPLE_TEMPLATE_1, NEW_EXAMPLE_JSON_TEMPLATE, ["example_1", "example_2", "example_3"], PANCAKES_EXAMPLE)
prompt_2 = create_prompt(PROMPT_TEMPLATE_FEW_SHOT, FORMATTED_EXAMPLE_TEMPLATE_1, NEW_EXAMPLE_JSON_TEMPLATE, ["example_1", "example_2"], PANCAKES_EXAMPLE)
prompt_3 = create_prompt(PROMPT_TEMPLATE_ZERO_SHOT, None, NEW_EXAMPLE_JSON_TEMPLATE, [], PANCAKES_EXAMPLE, zero_shot=True)

def extract_review(prompt):
    #this gets the part of the prompt after "Human: "
    review_assistant = prompt.split("Human: ")[-1]
    # print("review_assistant ", review_assistant, "\n")

    #this gets the actual review
    review = review_assistant.split("\n")[0]
    # print("review ", review, "\n")

    return review

def run_gpt(prompts):
    """
    Prompts GPT-4, and reformats the model's response into a json file, which gets saved to data/outputs
    As a checkpoint, it also saves the intermediate step from model response to a file in data/outputs
    """
    # print(os.environ)
    # print(os.getenv("OPENAI_API_KEY"))
    os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
    openai_api_key = os.getenv("OPENAI_API_KEY")
    openai.api_key = openai_api_key
    # get_gpt_completion("What is your name?")
    responses_json = {"responses": []}
    new_reviews = []
    count_processed = 0
    for prompt in prompts:
        new_reviews.append(extract_review(prompt))
        response = get_gpt_completion(prompt)
        print(response)
        responses_json["responses"].append(response)
        # Save every 25 because it might break in the middle and we don't want to lose it
        if count_processed % 25 == 0:
            now = datetime.now()
            now = now.strftime("%Y_%m_%d-%H_%M_%S")
            with open(f"data/outputs/interm_gpt_raw_output_{now}.json", "w") as raw_output_file:
                json.dump(responses_json, raw_output_file, indent=4)

    #save raw outputs to a file in data/outputs as a checkpoint
    now = datetime.now()
    now = now.strftime("%Y_%m_%d-%H_%M_%S")
    with open(f"data/outputs/gpt_raw_output_{now}.json", "w") as raw_output_file:
        json.dump(responses_json, raw_output_file, indent=4)

    gpt_save_output_json(new_reviews, responses_json["responses"])


def run_hugg_flan():
    tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-base", token = os.getenv("HUGGING_FACE_KEY"))
    model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-base", token = os.getenv("HUGGING_FACE_KEY")) 
    get_hugg_completion(prompt_2, tokenizer, model)
    get_hugg_completion("can you tell me what sport the following prompt relates too and give me your resoning? prompt: I like to shoot balls into a circle. Answer either: basketball, baseball", tokenizer, model)
    

def run_bard():
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/zackduitz/Downloads/first-website-374821-7893c1f2d758.json'
    palm.configure(api_key = os.getenv("PALM_KEY"))
    response = palm.generate_text(prompt=prompt_2, model ='models/text-bison-001', temperature = 0.0, max_output_tokens = 1024)
    print( "From text-bison: ", response)
    response2 = palm.chat(messages=prompt_2, model ='models/chat-bison-001', temperature = 0.0)
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
    prompts = [prompt_1, prompt_2]
    run_gpt(prompts)
    # run_bard()
    # run_hugg_flan()

    