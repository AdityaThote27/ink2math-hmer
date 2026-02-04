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
