import os
import json
import csv
import pprint
from collections import deque
pp = pprint.PrettyPrinter(indent=4)

print("Loading cleaned recipes file")
with open(os.path.join("..", "data", "cleaned", "cleaned_recipes.json"), "r") as inf:
    recipes = json.load(inf)

print("Loading unique list of ingredients")
with open(os.path.join("..", "data", "cleaned", "ingredients.csv"), newline='') as inf:
    reader = csv.reader(inf)
    val_ingredients = list(reader)
    val_ingredients = [x[0] for x in val_ingredients]

map_ingredients = True
ing_dict = {}

if map_ingredients:
    print("Generating ingredient mapping")
    for i, ing in enumerate(val_ingredients):
        ing_dict[ing] = i

    with open(os.path.join("..", "data", "cleaned", "ingredient_mapping.json"), "w") as output:
        json.dump(ing_dict, output)
    print("Ingredients mapped")

else:
    print("Reusing old mapping")
    with open(os.path.join("..", "data", "cleaned", "ingredient_mapping.json"), "r") as inf:
        ing_dict = json.load(inf)
    print("Ingredient mapping loaded")

encoding_dim = len(ing_dict)
print("Encoding Dimension: {}".format(encoding_dim))
print("Starting Recipe Encoding")
for i, recipe in enumerate(recipes):
    encoded = [0 for i in range(encoding_dim)]
    for ingredient in recipe["ingredients"]:
        encoded[ing_dict[ingredient]] = 1
    recipe["ingredients"] = encoded

with open(os.path.join("..", "data", "cleaned", "onehot_recipes.json"), "w") as output:
    recipes = json.dump(recipes, output)
