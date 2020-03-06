import json
import pprint
import sys
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
print("Data pruned")
pp.pprint(recipes[0])
with open(os.path.join("..", "data", "raw", "pruned.json"), "w") as output:
    json.dump(recipes, output)
