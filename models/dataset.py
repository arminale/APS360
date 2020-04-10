import os
import torch
import torch.utils.data as data
from collections import deque
import json
import random
import numpy as np


class ImageSet(data.Dataset):
    def __init__(self, img_folder_path, recipe_folder_path, mappings_path=None, mappings=None):

        if mappings_path is None and mappings is None:
            raise RuntimeError(
                "Exactly one of mapping path and mappings must be specified")
        elif mappings_path is not None and mappings is not None:
            raise RuntimeError(
                "Exactly one of mapping path and mappings must be specified")

        elif mappings_path is not None:
            self.mappings = deque()
            with open(mappings_path, 'r') as jfile:
                temp = json.load(jfile)

                for mapping in temp:
                    for image in mapping["images"]:
                        self.mappings.append(
                            [mapping["id"], "{}.tensor".format(image.split(".")[0])])

            self.mappings = list(self.mappings)
        else:
            self.mappings = mappings

        self.length = len(self.mappings)
        self.recipes = {}
        self.images = {}
        self.recipe_folder_path = recipe_folder_path
        self.img_folder_path = img_folder_path
        self.loaded = False

    def unload(self):
        if not self.loaded:
            print("Data has already been removed from memory")
            return
        print("Removing loaded data from memory")
        del self.recipes
        del self.images
        self.loaded = False

    def split(self):
        if self.loaded:
            raise MemoryError(
                "Data is loaded. Splitting and loading the new datasets might cause memory issues.")

        random.seed(1000)
        random.shuffle(self.mappings)

        train_set = ImageSet(self.img_folder_path, self.recipe_folder_path,
                             mappings=self.mappings[:int(self.length*0.70)])
        valid_set = ImageSet(self.img_folder_path, self.recipe_folder_path,
                             mappings=self.mappings[int(self.length*0.70):int(self.length*0.85)])
        test_set = ImageSet(self.img_folder_path, self.recipe_folder_path,
                            mappings=self.mappings[int(self.length*0.85):])

        return train_set, valid_set, test_set

    def load(self):
        if self.loaded:
            print("Dataset has already been loaded. No need to reload data")
            return

        self.recipes = {}
        print("Loading dataset into memory. This requires >1GB of RAM")
        for start in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, "a", "b", "c", "d", "e", "f"]:
            with open(os.path.join(self.recipe_folder_path, "encoded-{}.json".format(start)), 'r') as jfile:
                temp = json.load(jfile)
                for recipe in temp:
                    self.recipes[recipe["id"]] = torch.FloatTensor(
                        recipe["ingredients"])

        self.images = {}
        for root, dirs, files in os.walk(self.img_folder_path):
            for name in files:
                self.images[name] = torch.load(
                    os.path.join(root, name)).view(-1, 2048).squeeze(0)
        self.loaded = True

    def __getitem__(self, index):
        if not self.loaded:
            raise IndexError("You must load the dataset first. Call .load()")
        recipe_id, image_id = self.mappings[index]
        return self.images[image_id], self.recipes[recipe_id]

    def __len__(self):
        return self.length

    def is_loaded(self):
        return self.loaded

    def get_all_as_numpy(self):
        if not self.loaded:
            self.load()

        print("Transforming data to numpy arrays")
        test_i, test_r = self.__getitem__(0)
        images_np = np.zeros((self.length, test_i.shape[0]))
        recipes_np = np.zeros((self.length, test_r.shape[0]))
        for i, mapping in enumerate(self.mappings):
            recipe_id, image_id = mapping
            images_np[i] = self.images[image_id].numpy()
            recipes_np[i] = self.recipes[recipe_id].numpy()

        print("To avoid memory errors, data loaded into this dataset will be removed")
        self.unload()
        return images_np, recipes_np


if __name__ == "__main__":

    test = ImageSet(os.path.join("..", "data", "cleaned", "images", "test"),
                    os.path.join("..", "data", "cleaned", "recipes"),
                    mappings_path=os.path.join(
        "..", "data", "cleaned", "final_cleaned_mappings.json"))
    test.load()
    # test.load()
    # print(test.__getitem__(0)[0].shape)
    # print(test.__getitem__(0)[1].shape)
    # print(len(test))
    # test.unload()
    X, y = test.get_all_as_numpy()
    print(X.shape)
    print(y.shape)

    from sklearn.ensemble import RandomForestClassifier

    X_train = X[0:int(0.2*X.shape[0]), :]
    y_train = y[0:int(0.2*y.shape[0])]
    X_test = X[int(0.2*X.shape[0]):int(0.2*X.shape[0])+int(0.05*X.shape[0]), :]
    y_test = y[int(0.2*y.shape[0]):int(0.2*X.shape[0])+int(0.05*X.shape[0])]

#X_valid = X[0:]
    print(X.shape, X_train.shape, y_train.shape, X_test.shape, y_test.shape)

    clf = RandomForestClassifier(max_depth=200, verbose=2)
    clf.fit(X_train, y_train)

    correct = 0

    prediction = clf.predict(X_test)
    print(prediction)

    for i in range(len(y_test)):
        if prediction[i] == y_test[i]:
            correct += 1

    print("prediction accuracy: {}".format(correct/len(y_test)))
    # del images
    # del recipes
    # train_set, valid_set, test_set = test.split()
    # print(len(train_set))
    # print(len(valid_set))
    # print(len(test_set))
    # train_set.load()
    # train_loader = data.DataLoader(train_set, batch_size=32, shuffle=True)
    # for sample, label in train_loader:
    #     print(sample.shape)
    #     print(label.shape)
    #     break
