import os
import json
import csv
import copy
import pprint
import sys
from gensim.models import Word2Vec
import numpy as np
from collections import deque

pp = pprint.PrettyPrinter(indent=4)

print("Loading cleaned recipes file")
with open(os.path.join("..", "data", "cleaned", "cleaned_recipes_full.json"), "r") as inf:
    recipes = json.load(inf)

recipes.sort(key=lambda x: int(x["id"], 16))


recipes = list(filter(lambda recipe: recipe["partition"] == "test", recipes))
print("Test recipes: {}".format(len(recipes)))

encoder = Word2Vec.load("W2Vmod")
print("Starting Recipe Encoding")

last_saved = -1
missed = 0

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
        encoded = np.zeros(300)
        for ingredient in recipe["ingredients"]:
            for temp in ingredient.split(" "):
                try:
                    encoded += np.asarray(encoder[temp])
                except KeyError:
                    missed += 1
        recipe["ingredients"] = list(encoded)
    print("Encoded recipes that start with {}".format(start))

    with open("encoded-w2v-{}.json".format(start), "w") as out:
        json.dump(target_recipes, out)
print(missed)
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
