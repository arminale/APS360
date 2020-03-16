import json
import pprint
import sys
from collections import deque
import os
pp = pprint.PrettyPrinter(indent=4)

print("Opening raw data file")
with open(os.path.join("..", "data", "raw", "layer1.json"), 'r') as jfile:
    recipes = json.load(jfile)

print("File loaded")

for i, recipe in enumerate(recipes):
    recipe.pop("instructions")
    recipe.pop("url")
    keys = list(recipe.keys())
    for attribute in ["id", "ingredients", "partition", "title"]:
        if attribute not in keys:
            print(i, keys)
            sys.exit()

    if i+1 % 10000 == 0:
        print(i)
print("Recipes pruned")
pp.pprint(recipes[0])

print("Opening mapping file")
with open(os.path.join("..", "data", "raw", "layer2.json"), 'r') as jfile:
    mappings = json.load(jfile)

pp.pprint(mappings[0])

print("Pruning mappings")
valid_recipe_ids = deque()
for mapping in mappings:
    valid_recipe_ids.append(mapping["id"])
    mapping["images"] = [image["id"] for image in mapping["images"]]

valid_recipe_ids = list(valid_recipe_ids)
pp.pprint(mappings[0])
print("Removing recipes without images")
temp_dict = {}
for recipe in recipes:
    temp_dict[recipe["id"]] = recipe

valid_recipes = deque()
for iD in valid_recipe_ids:
    valid_recipes.append(temp_dict[iD])
valid_recipes = list(valid_recipes)
del recipes
del temp_dict
print(len(valid_recipes))
pp.pprint(valid_recipes[0])
with open(os.path.join("..", "data", "cleaned", "pruned_recipes.json"), "w") as output:
    json.dump(valid_recipes, output)

with open(os.path.join("..", "data", "cleaned", "pruned_mappings.json"), "w") as output:
    json.dump(mappings, output)
