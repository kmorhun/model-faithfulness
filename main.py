import os
import openai
from flan_call import get_hugg_completion
from gpt_api import test
from transformers import T5Tokenizer, T5ForConditionalGeneration
import google.generativeai as palm
from dotenv import load_dotenv

prompt_1 = """Please classify the sentiment of the following Yelp customer reviews of restaurants with a score from 1 (negative) to 5 (positive). Explain the reasoning for your classification by highlighting the most relevant phrases in the review used in analysis.

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

Please classify this last text. In the same format the assistant has.

"""

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
    get_hugg_completion(prompt_1, tokenizer, model)
    get_hugg_completion("can you tell me what sport the following prompt relates too and give me your resoning? prompt: I like to shoot balls into a circle. Answer either: basketball, baseball", tokenizer, model)
    

def run_bard():
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/zackduitz/Downloads/first-website-374821-7893c1f2d758.json'
    palm.configure(api_key = os.getenv("PALM_KEY"))
    response = palm.generate_text(prompt=prompt_1, model ='models/text-bison-001', temperature = 0.0, max_output_tokens = 1024)
    print(response)
    response2 = palm.chat(messages=prompt_1, model ='models/chat-bison-001', temperature = 0.0)
    print(response2.last)
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

    