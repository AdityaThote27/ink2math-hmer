import torch

from ml.models.cnn_transformer.hmer_transformer import HMERTransformer
from ml.models.cnn_transformer.decoding import ctc_greedy_decode
from ml.dataset.crohme_dataset import CROHMEDataset


# --------------------------------------------------
# Device
# --------------------------------------------------
device = "cuda" if torch.cuda.is_available() else "cpu"
print("Using device:", device)


# --------------------------------------------------
# Config (MUST match training)
# --------------------------------------------------
IMG_HEIGHT = 256
IMG_WIDTH = 256
NUM_CLASSES = 75

CHECKPOINT_PATH = "ml/models/cnn_transformer/transformer_ctc.pth"
TOKENIZER_PATH = "ml/models/cnn_transformer/tokenizer_stoi.pth"


# --------------------------------------------------
# Load tokenizer vocab (STRICT)
# --------------------------------------------------
stoi = torch.load(TOKENIZER_PATH)
idx_to_token = {v: k for k, v in stoi.items()}

print("Tokenizer size:", len(stoi))
print("Max token id in tokenizer:", max(stoi.values()))


# --------------------------------------------------
# Load model
# --------------------------------------------------
model = HMERTransformer(
    num_classes=NUM_CLASSES,
    img_height=IMG_HEIGHT,
    img_width=IMG_WIDTH
).to(device)

checkpoint = torch.load(CHECKPOINT_PATH, map_location=device)
model.load_state_dict(checkpoint)

model.eval()
print("✅ Transformer model loaded")


# --------------------------------------------------
# Load dataset (single sample test)
# --------------------------------------------------
dataset = CROHMEDataset(year="2014")

image, gt = dataset[0]
image = image.unsqueeze(0).to(device)

print("GT:", gt)


# --------------------------------------------------
# Inference
# --------------------------------------------------
with torch.no_grad():
    logits, seq_len = model(image, return_log_probs=True)
    decoded = ctc_greedy_decode(logits, idx_to_token)


prediction = decoded[0] if len(decoded) > 0 else ""
print("Prediction:", prediction)
