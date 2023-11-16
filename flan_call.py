# This file contains the calls to hugginface models

import os
from transformers import AutoTokenizer, AutoModelForMaskedLM




def get_hugg_completion(prompt, tokenizer, model):
    """
    Given a prompt to pass into the model specified return a response
    """
    # tokenizer = AutoTokenizer.from_pretrained(model, token = os.getenv("HUGGING_FACE_KEY"))
    # model = AutoModelForMaskedLM.from_pretrained(model, token = os.getenv("HUGGING_FACE_KEY"))


    input_text = "translate English to German: How old are you?"
    input_ids = tokenizer(prompt, return_tensors="pt").input_ids

    outputs = model.generate(input_ids, max_length = 1000)
    print(tokenizer.decode(outputs[0]))






