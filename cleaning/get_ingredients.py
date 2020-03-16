import os
import json
import csv
import pprint
import sys
from collections import deque
pp = pprint.PrettyPrinter(indent=4)

print("Loading pruned recipes file")
with open(os.path.join("..", "data", "cleaned", "pruned_recipes.json"), "r") as inf:
    recipes = json.load(inf)

print("Loading unique list of ingredients")
with open(os.path.join("..", "data", "cleaned", "reduced_listing.csv"), "r") as inf:
    ingredients = deque()
    for line in inf:
        ingredients.append(line.strip("\n").lower().strip())

ingredients = list(filter(lambda ing: len(ing) > 0, ingredients))
ingredients = list(set(ingredients))
print(len(ingredients))

ingredients.sort(key=lambda x: len(x), reverse=True)
last_saved = -1
for i, recipe in enumerate(recipes):
    valid_ing_list = []
    for raw_ing in recipe["ingredients"]:
        for j, valid_ing in enumerate(ingredients):
            if valid_ing in raw_ing["text"].lower().replace("-", " "):
                valid_ing_list.append(valid_ing)
                break
    recipe["ingredients"] = list(set(valid_ing_list))
    if i % 10000 == 0 and i != 0:
        with open("temp-{}-{}.json".format(i-10000, i), "w") as out:
            json.dump(recipes[i-10000:i], out, indent=4)
            last_saved = i-1


with open("temp-{}-end.json".format(last_saved), "w") as out:
    json.dump(recipes[last_saved+1:], out, indent=4)

del recipes

with open(os.path.join("..", "data", "cleaned", "cleaned_recipes_full.json"), "w") as big_file:
    temp = []
    for f in os.listdir("."):
        if f.startswith("temp-"):
            print(f)
            with open(os.path.join(".", f)) as temp_file:
                temp.extend(json.load(temp_file))
    json.dump(temp, big_file, indent=4)
