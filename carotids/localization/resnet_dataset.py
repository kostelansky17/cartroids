import os

import torch
from torch.utils.data.dataset import Dataset

from carotids.preprocessing import load_img, load_position
from carotids.utils import recompute_labels


class ResnetCarotidDataset(Dataset):
    def __init__(self, imgs_path, labels_path, transformations):
        self.data_path = imgs_path
        self.labels_path = labels_path

        self.data_files = sorted(os.listdir(imgs_path))
        self.labels_files = sorted(os.listdir(labels_path))

        self.transformations = transformations

    def __getitem__(self, index):
        img = load_img(self.data_path, self.data_files[index])
        x0, y0, x1, y1 = load_position(self.labels_path, self.labels_files[index])
        label_tensor = recompute_labels(img, x0, y0, x1, y1)

        return self.transformations(img).double(), label_tensor.double()

    def __len__(self):
        return len(self.data_files)
