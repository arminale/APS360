import os
import json
from collections import deque

with open(os.path.join("..", "data", "cleaned", "pruned_mappings.json"), 'r') as jfile:
    mappings = json.load(jfile)

print(len(mappings))

temp_dict = {}
for mapping in mappings:
    temp_dict[mapping["id"]] = mapping

print("Loading cleaned recipes file")
with open(os.path.join("..", "data", "cleaned", "cleaned_recipes_full.json"), "r") as inf:
    recipes = json.load(inf)

recipes = list(filter(lambda recipe: recipe["partition"] == "test", recipes))

temp = deque()
for recipe in recipes:
    temp.append(temp_dict[recipe["id"]])

mapping = list(temp)
print(len(mapping))
with open(os.path.join("..", "data", "cleaned", "final_cleaned_mappings.json"), 'w') as jfile:
    mappings = json.dump(mapping, jfile)
