import numpy as np
import pandas as pd
import torch
from torch.utils.data import Dataset

class training_dataset(Dataset):
    """
    Custom Dataset for CNN training.
    Loads grayscale images (100x100) and
    corresponding bounding box labels.
    """

    def __init__(self):
        # Load training data
        trainX = pd.read_csv('./Dataset/trainingData.csv', header=None).values
        trainY = pd.read_csv('./Dataset/ground-truth.csv', header=None).values

        # Convert to torch tensors
        self.features = torch.tensor(trainX, dtype=torch.float32)
        self.labels = torch.tensor(trainY, dtype=torch.float32)

        self.length = len(self.features)

    def __getitem__(self, index):
        """
        Returns:
        - image tensor (100*100 flattened)
        - bounding box tensor (x, y, w, h)
        """
        return self.features[index], self.labels[index]

    def __len__(self):
        return self.length
