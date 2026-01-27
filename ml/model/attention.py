import torch
import torch.nn as nn
import torch.nn.functional as F

class Attention(nn.Module):
    def __init__(self, enc_dim, dec_dim):
        super().__init__()
        self.enc_proj = nn.Linear(enc_dim, dec_dim)
        self.dec_proj = nn.Linear(dec_dim, dec_dim)
        self.score = nn.Linear(dec_dim, 1)

    def forward(self, encoder_out, hidden):
        # encoder_out: [B, T, C]
        # hidden: [B, H]

        enc = self.enc_proj(encoder_out)           # [B, T, H]
        dec = self.dec_proj(hidden).unsqueeze(1)   # [B, 1, H]

        energy = torch.tanh(enc + dec)
        scores = self.score(energy).squeeze(-1)    # [B, T]
        alpha = F.softmax(scores, dim=1)           # attention weights

        context = (encoder_out * alpha.unsqueeze(-1)).sum(dim=1)
        return context
