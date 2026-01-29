import torch
import torch.nn as nn
from models.cnn_lstm.encoder import CNNEncoder
from models.cnn_lstm.decoder import AttnLSTMDecoder


class HMERModel(nn.Module):
    def __init__(self, vocab_size, hidden_dim=256):
        super().__init__()
        self.encoder = CNNEncoder()
        self.decoder = AttnLSTMDecoder(vocab_size)


        self.init_h = nn.Linear(512, hidden_dim)
        self.init_c = nn.Linear(512, hidden_dim)

    def forward(self, images, tokens):
        enc_out = self.encoder(images)          # [B, T, 512]
        context = enc_out.mean(dim=1)

        h0 = self.init_h(context).unsqueeze(0)
        c0 = self.init_c(context).unsqueeze(0)

        return self.decoder(enc_out, tokens, (h0, c0))
