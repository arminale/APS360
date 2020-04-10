import os
import json

with open(os.path.join("..", "data", "cleaned", "index_to_ingredient.json")) as f:
    mapping_dict = json.load(f)

mapping = [0]*1625

for key, val in mapping_dict.items():
    mapping[int(key)] = val

print(mapping)
