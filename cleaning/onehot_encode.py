import os
import json
import csv
import copy
import pprint
import sys
from collections import deque

pp = pprint.PrettyPrinter(indent=4)

print("Loading cleaned recipes file")
with open(os.path.join("..", "data", "cleaned", "cleaned_recipes_full.json"), "r") as inf:
    recipes = json.load(inf)

recipes.sort(key=lambda x: int(x["id"], 16))

print("Loading unique list of ingredients")
val_ingredients = deque()
with open(os.path.join("..", "data", "cleaned", "reduced_listing.csv"), "r") as inf:
    for line in inf:
        val_ingredients.append(line.strip("\n").lower().strip())

val_ingredients = list(filter(lambda ing: len(ing) > 0, val_ingredients))
val_ingredients = list(set(val_ingredients))
val_ingredients.sort(key=lambda x: len(x), reverse=True)

map_ingredients = True
ing_dict = {}

if map_ingredients:
    print("Generating ingredient mapping")
    for i, ing in enumerate(val_ingredients):
        ing_dict[ing] = i

    with open(os.path.join("..", "data", "cleaned", "ingredient_to_index.json"), "w") as output:
        json.dump(ing_dict, output, indent=4)

    inv_map = {v: k for k, v in ing_dict.items()}
    with open(os.path.join("..", "data", "cleaned", "index_to_ingredient.json"), "w") as output:
        json.dump(inv_map, output, indent=4)
    print("Ingredients mapped")

else:
    print("Reusing old mapping")
    with open(os.path.join("..", "data", "cleaned", "ingredient_to_index.json"), "r") as inf:
        ing_dict = json.load(inf)
    print("Ingredient mapping loaded")

encoding_dim = len(ing_dict)
print("Encoding Dimension: {}".format(encoding_dim))
print("Starting Recipe Encoding")

last_saved = -1

for start in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f"]:
    print("Targeting recipes that start with {}".format(start))
    letter_end = -1
    for i, recipe in enumerate(recipes):
        if recipe["id"].startswith(start):
            letter_end += 1
        else:
            break
    target_recipes = copy.deepcopy(recipes[:letter_end+1])
    del recipes[:letter_end+1]
    for recipe in target_recipes:
        encoded = [0 for i in range(encoding_dim)]
        for ingredient in recipe["ingredients"]:
            encoded[ing_dict[ingredient]] = 1
        recipe["ingredients"] = copy.deepcopy(encoded)

    print("Encoded recipes that start with {}".format(start))

    with open("encoded-{}.json".format(start), "w") as out:
        json.dump(target_recipes, out)
# for i, recipe in enumerate(recipes):
#     encoded = [0 for i in range(encoding_dim)]
#     for ingredient in recipe["ingredients"]:
#         encoded[ing_dict[ingredient]] = 1
#     recipe["ingredients"] = copy.deepcopy(encoded)
#     if i % 10000 == 0 and i != 0:
#         with open("temp-{}-{}.json".format(i-10000, i), "w") as out:
#             json.dump(recipes[i-10000:i], out)
#             last_saved = i-1

# with open("temp-{}-end.json".format(last_saved), "w") as out:
#     json.dump(recipes[last_saved+1:], out)

# n = len(recipes)
# for i in range(10):
#     with open(os.path.join("..", "data", "cleaned", "onehot_recipes-{}.json".format(i)), "w") as output:
#         recipes = json.dump(recipes[i*n // 10: (i+1) * n // 10], output)
