import json 

def preprocess(json_filepath, add_one=True):
    json_content = {}
    with open(json_filepath, "r", encoding="UTF-8") as json_file:
        json_content = json.load(json_file)
        for category, reviews in json_content.items():
            category_content = {}
            for review_name, review in reviews.items():
                if (add_one):
                    new_sentiment = int(review["label"])+1
                else:
                    new_sentiment = int(review["label"])
                category_content[review_name] = {"review": review["text"], "sentiment": new_sentiment}

            with open(f"data/inputs/{category}_dataset.json", "w", encoding="UTF-8") as category_file:
                json.dump(category_content, category_file, indent=4) #repopulate, but pretty~
if __name__ == "__main__":
    preprocess("data/inputs/raw/dataset_reviews.json")


