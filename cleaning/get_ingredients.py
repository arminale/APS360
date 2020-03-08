import os
import json
import csv
import pprint
import sys
from collections import deque
pp = pprint.PrettyPrinter(indent=4)

print("Loading pruned recipes file")
with open(os.path.join("..", "data", "cleaned", "test.json"), "r") as inf:
    recipes = json.load(inf)

print("Loading unique list of ingredients")
with open(os.path.join("..", "data", "cleaned", "reduced_listing.csv"), "r") as inf:
    ingredients = deque()
    for line in inf:
        ingredients.append(line.strip("\n").lower().strip())

ingredients = list(filter(lambda ing: len(ing) > 0, ingredients))
ingredients = list(set(ingredients))
print(len(ingredients))

print("baking powder" in ingredients)
ingredients.sort(key=lambda x: len(x), reverse=True)
print(ingredients.index("baking powder"))
print(ingredients.index("powder"))

for i, recipe in enumerate(recipes):
    valid_ing_list = []
    for raw_ing in recipe["ingredients"]:
        for j, valid_ing in enumerate(ingredients):
            if valid_ing in raw_ing["text"].lower().replace("-", " "):
                valid_ing_list.append(valid_ing)
                break
    recipe["ingredients"] = list(set(valid_ing_list))
    if i+1 % 10000 == 0:
        print(i)

with open(os.path.join("..", "data", "cleaned", "cleaned_recipes.json"), "w") as inf:
    recipes = json.dump(recipes, inf)
