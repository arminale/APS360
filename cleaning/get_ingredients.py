import os
import json
import csv
import pprint
from collections import deque
pp = pprint.PrettyPrinter(indent=4)

print("Loading pruned recipes file")
with open(os.path.join("..", "data", "cleaned", "pruned.json"), "r") as inf:
    recipes = json.load(inf)

print("Loading unique list of ingredients")
with open(os.path.join("..", "data", "cleaned", "ingredients.csv"), newline='') as inf:
    reader = csv.reader(inf)
    ingredients = list(reader)
    ingredients = [x[0] for x in ingredients]

pp.pprint(recipes[0])
print(ingredients)

for i, recipe in enumerate(recipes):
    valid_ing_list = deque()
    for raw_ing in recipe["ingredients"]:
        for valid_ing in ingredients:
            if valid_ing in raw_ing["text"]:
                valid_ing_list.append(valid_ing)
    recipe["ingredients"] = list(valid_ing_list)
    if i+1 % 10000 == 0:
        print(i)

with open(os.path.join("..", "data", "cleaned", "cleaned_recipes.json"), "w") as inf:
    recipes = json.dump(recipes, inf)
