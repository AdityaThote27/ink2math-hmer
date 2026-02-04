import torch
from torchvision.datasets import MNIST
from torchvision import transforms
from model import DigitTransformer

device = "cuda" if torch.cuda.is_available() else "cpu"

transform = transforms.Compose([
    transforms.Resize((64, 64)),
    transforms.ToTensor()
])

dataset = MNIST(root="./data", train=False, download=True, transform=transform)

model = DigitTransformer().to(device)
model.load_state_dict(torch.load("digit_transformer.pth", map_location=device))
model.eval()

img, label = dataset[0]
with torch.no_grad():
    pred = model(img.unsqueeze(0).to(device)).argmax(dim=1).item()

print("True label:", label)
print("Predicted:", pred)
