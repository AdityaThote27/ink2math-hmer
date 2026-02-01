import random
import torch
from torch.utils.data import Dataset
import torchvision.transforms as T

from ml.dataset.digit_dataset import DigitDataset


class AugmentedDigitDataset(Dataset):
    """
    Augments digit-only samples to artificially increase data size.
    """

    def __init__(self, year="2014", repeat_factor=50):
        self.base = DigitDataset(year=year)
        self.repeat_factor = repeat_factor

        self.transforms = T.Compose([
            T.RandomRotation(degrees=5),
            T.RandomAffine(
                degrees=0,
                translate=(0.02, 0.02),
                scale=(0.95, 1.05),
                shear=2
            ),
        ])

        self.samples = []
        for img, label in self.base:
            for _ in range(self.repeat_factor):
                self.samples.append((img, label))

        print(f"[AugmentedDigitDataset] Total samples: {len(self.samples)}")

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        img, label = self.samples[idx]

        # Apply augmentation
        img = self.transforms(img)

        return img, label

if __name__ == "__main__":
    ds = AugmentedDigitDataset()
    for i in range(5):
        _, label = ds[i]
        print(label)
