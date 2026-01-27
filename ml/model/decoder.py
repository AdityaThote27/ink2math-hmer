import torch
import torch.nn as nn
from ml.model.attention import Attention

class AttnLSTMDecoder(nn.Module):
    def __init__(self, vocab_size, enc_dim=512, hidden_dim=256):
        super().__init__()
        self.hidden_dim = hidden_dim

        self.embedding = nn.Embedding(vocab_size, hidden_dim)
        self.attention = Attention(enc_dim, hidden_dim)

        self.lstm = nn.LSTM(hidden_dim + enc_dim, hidden_dim, batch_first=True)
        self.fc = nn.Linear(hidden_dim, vocab_size)

    def forward(self, encoder_out, tokens, hidden):
        batch_size, seq_len = tokens.size()
        outputs = []

        h, c = hidden

        for t in range(seq_len):
            emb = self.embedding(tokens[:, t])      # [B, H]
            context = self.attention(encoder_out, h[-1])  # [B, C]

            lstm_input = torch.cat([emb, context], dim=1).unsqueeze(1)
            out, (h, c) = self.lstm(lstm_input, (h, c))

            logits = self.fc(out.squeeze(1))
            outputs.append(logits)

        return torch.stack(outputs, dim=1)


