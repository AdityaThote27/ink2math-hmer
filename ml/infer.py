import torch
import cv2
from ml.model.hmer_model import HMERModel
from ml.tokenizer import Tokenizer
from ml.dataset.crohme_dataset import CROHMEDataset

device = "cuda" if torch.cuda.is_available() else "cpu"

# Load checkpoint
ckpt = torch.load("ml/checkpoints/hmer_attn_2014.pt", map_location=device)

# Rebuild tokenizer
tokenizer = Tokenizer()
tokenizer.stoi = ckpt["vocab"]
tokenizer.itos = {i:s for s,i in tokenizer.stoi.items()}

# Load model
model = HMERModel(vocab_size=len(tokenizer.stoi)).to(device)
model.load_state_dict(ckpt["model_state"])
model.eval()

# Load one sample image
dataset = CROHMEDataset(year="2014")
image, gt = dataset[0]
image = image.unsqueeze(0).to(device)

# Greedy decoding (simple)
tokens = torch.tensor([[tokenizer.stoi["<SOS>"]]]).to(device)

with torch.no_grad():
    for _ in range(30):
        out = model(image, tokens)
        next_token = out[:, -1].argmax(-1).unsqueeze(1)
        tokens = torch.cat([tokens, next_token], dim=1)
        if next_token.item() == tokenizer.stoi["<EOS>"]:
            break

pred = [tokenizer.itos[t.item()] for t in tokens[0][1:]]

print("🖊 Ground Truth:", gt)
print("🤖 Prediction:", " ".join(pred))
