import torch

from ml.models.cnn_transformer.hmer_transformer import HMERTransformer


# --------------------------------------------------
# Paths
# --------------------------------------------------
DIGIT_CKPT = "ml/models/cnn_transformer/transformer_digit_pretrained.pth"
FULL_CKPT_OUT = "ml/models/cnn_transformer/transformer_with_digit_init.pth"


# --------------------------------------------------
# Load digit-pretrained model (11 classes)
# --------------------------------------------------
digit_model = HMERTransformer(
    num_classes=11,
    img_height=256,
    img_width=256
)

digit_state = torch.load(DIGIT_CKPT, map_location="cpu")
digit_model.load_state_dict(digit_state)

print("✅ Loaded digit-pretrained weights")


# --------------------------------------------------
# Create full model (75 classes)
# --------------------------------------------------
full_model = HMERTransformer(
    num_classes=75,
    img_height=256,
    img_width=256
)

full_state = full_model.state_dict()

# --------------------------------------------------
# Transfer all weights EXCEPT classifier
# --------------------------------------------------
for name, param in digit_model.state_dict().items():
    if not name.startswith("classifier"):
        full_state[name] = param

full_model.load_state_dict(full_state)

# --------------------------------------------------
# Save new initialized model
# --------------------------------------------------
torch.save(full_model.state_dict(), FULL_CKPT_OUT)
print(f"✅ Full model initialized with digit knowledge saved to: {FULL_CKPT_OUT}")
