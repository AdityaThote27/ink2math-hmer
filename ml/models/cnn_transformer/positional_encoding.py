import torch
import torch.nn as nn


class PositionalEncoding2D(nn.Module):
    """
    2D Positional Encoding for CNN feature maps converted to tokens.

    Adds spatial information (row + column) so the Transformer
    understands layout: fractions, superscripts, roots, etc.
    """

    def __init__(self, embed_dim, height, width):
        """
        Args:
            embed_dim (int): embedding dimension (must be even)
            height (int): feature map height (H')
            width (int): feature map width (W')
        """
        super().__init__()

        assert embed_dim % 2 == 0, "embed_dim must be even for 2D positional encoding"

        self.embed_dim = embed_dim
        self.height = height
        self.width = width

        # Half for rows, half for columns
        self.row_embed = nn.Embedding(height, embed_dim // 2)
        self.col_embed = nn.Embedding(width, embed_dim // 2)

        self.reset_parameters()

    def reset_parameters(self):
        nn.init.uniform_(self.row_embed.weight)
        nn.init.uniform_(self.col_embed.weight)

    def forward(self, x):
        """
        Args:
            x: Tensor of shape (batch, seq_len, embed_dim)
               where seq_len = height * width
        Returns:
            x with positional encodings added
        """

        device = x.device
        B, T, E = x.shape
        assert T == self.height * self.width, "Sequence length mismatch"

        # Create row and column indices
        rows = torch.arange(self.height, device=device)
        cols = torch.arange(self.width, device=device)

        # Get embeddings
        row_emb = self.row_embed(rows)    # (H', E/2)
        col_emb = self.col_embed(cols)    # (W', E/2)

        # Combine row + column embeddings
        pos = torch.cat(
            [
                row_emb.unsqueeze(1).repeat(1, self.width, 1),
                col_emb.unsqueeze(0).repeat(self.height, 1, 1)
            ],
            dim=-1
        )  # (H', W', E)

        pos = pos.view(1, T, E)  # (1, seq_len, embed_dim)

        return x + pos

