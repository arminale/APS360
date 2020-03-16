import os
import torch
import torch.utils.data as data
from collections import deque
import json
import numpy as np


class ImagerLoader(data.Dataset):
    def __init__(self, img_folder_path, recipe_folder_path, mapping_path):
        self.mappings = deque()
        with open(mapping_path, 'r') as jfile:
            temp = json.load(jfile)

            for mapping in temp:
                for image in mapping["images"]:
                    self.mappings.append(
                        [mapping["id"], "{}.tensor".format(image.split(".")[0])])

        self.mappings = list(self.mappings)
        self.length = len(self.mappings)
        self.recipes = {}

        for start in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, "a", "b", "c", "d", "e", "f"]:
            with open(os.path.join(recipe_folder_path, "encoded-{}.json".format(start)), 'r') as jfile:
                temp = json.load(jfile)
                for recipe in temp:
                    self.recipes[recipe["id"]] = torch.FloatTensor(
                        recipe["ingredients"])

        self.images = {}
        for root, dirs, files in os.walk(img_folder_path):
            for name in files:
                self.images[name] = torch.load(
                    os.path.join(root, name)).view(-1, 2048).squeeze(0)

    def __getitem__(self, index):
        recipe_id, image_id = self.mappings[index]
        return self.images[image_id], self.recipes[recipe_id]

    def __len__(self):
        return self.length

    def get_all_as_numpy(self):
        test_i, test_r = self.__getitem__(0)
        images_np = np.zeros((self.length, test_i.shape[0]))
        recipes_np = np.zeros((self.length, test_r.shape[0]))
        for i, mapping in enumerate(self.mappings):
            recipe_id, image_id = mapping
            images_np[i] = self.images[image_id].numpy()
            recipes_np[i] = self.recipes[recipe_id].numpy()
        return images_np, recipes_np


test = ImagerLoader(r"..\data\cleaned\images\test",
                    r"..\data\cleaned", r"..\data\cleaned\final_cleaned_mappings.json")
print(test.__getitem__(0)[0].shape)
print(test.__getitem__(0)[1].shape)
print(len(test))
images, recipes = test.get_all_as_numpy()
del test
print(images.shape)
print(recipes.shape)
