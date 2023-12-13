from datasets import load_dataset
import xlrd
import csv
import json
    

def remove_labels(example):
    del example['label']
    return example

def is_short_text(example):
    # Split the text into words and check if the length is 15-25 or 35-80
    return 35 <= len(example['text'].split()) <= 80

def convert_json(data):
    dic = {}
    count = 0
    for review in data:
        keyname = 'Example_' + str(count)

        



if __name__ == '__main__':

    # dataset = load_dataset("yelp_review_full")
    # dataset = dataset['train']
    # #print(dataset['train'][:100])
    # #dataset = dataset.map(remove_labels)
    # short_texts_dataset = dataset.filter(is_short_text)
    # short_texts_dataset.to_csv('train_sentences2.csv', index=False)

    # print((short_texts_dataset)[0])
    dic = {}
    with open("/Users/bennettstankovits/Downloads/reviews - movie.csv", mode='r') as file:
        movie = {}
        reader = csv.reader(file)
        count = 1
        for row in reader:
            examplename = "Example_" + str(count)
            text = row[0]
            label = int(row[1])
            v = {"text": text, "label": label}
            movie[examplename] = v
            count += 1
        dic["movieshort"] = movie

    with open("/Users/bennettstankovits/Downloads/reviews - restaurant.csv", mode='r') as file:
        restaurant = {}
        reader = csv.reader(file)
        count = 1
        for row in reader:
            examplename = "Example_" + str(count)
            text = row[0]
            label = int(row[1])

            v = {"text": text, "label": label+1}
            restaurant[examplename] = v
            count += 1
        dic["yelpshort"] = restaurant
        
    with open("/Users/bennettstankovits/Downloads/reviews - movielong.csv", mode='r') as file:
        movie = {}
        reader = csv.reader(file)
        count = 1
        for row in reader:
            examplename = "Example_" + str(count)
            text = row[0]
            label = int(row[1])
            v = {"text": text, "label": label}
            movie[examplename] = v
            count += 1
        dic["movielong"] = movie

    with open("/Users/bennettstankovits/Downloads/reviews - yelplong.csv", mode='r') as file:
        restaurant = {}
        reader = csv.reader(file)
        count = 1
        for row in reader:
            examplename = "Example_" + str(count)
            text = row[1]
            label = int(row[0])

            v = {"text": text, "label": label+1}
            restaurant[examplename] = v
            count += 1
        dic["yelplong"] = restaurant


    with open("/Users/bennettstankovits/reviews.json", 'w') as json_file:
        json.dump(dic, json_file)



