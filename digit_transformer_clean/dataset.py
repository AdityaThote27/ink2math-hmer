# dataset.py
from torchvision.datasets import MNIST
from torchvision import transforms
from torch.utils.data import DataLoader

def get_loader(batch_size=32):
    transform = transforms.Compose([
        transforms.Resize((64, 64)),
        transforms.ToTensor()
    ])

    dataset = MNIST(
        root="./data",
        train=True,
        download=True,
        transform=transform
    )

    return DataLoader(dataset, batch_size=batch_size, shuffle=True)

import random
import torch

def get_test_sample():
    """
    Returns a single random digit image and its label
    from the test dataset.
    """
    from torchvision import datasets, transforms

    transform = transforms.Compose([
        transforms.Resize((64, 64)),
        transforms.ToTensor()
    ])

    test_dataset = datasets.MNIST(
        root="./data",
        train=False,
        download=True,
        transform=transform
    )

    idx = random.randint(0, len(test_dataset) - 1)
    img, label = test_dataset[idx]

    return img, label
