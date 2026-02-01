class CTCTokenizer:
    def __init__(self):
        """
        CTC tokenizer with explicit blank token at index 0
        """
        self.blank_token = "<blank>"
        self.blank_idx = 0

        self.stoi = {self.blank_token: self.blank_idx}
        self.itos = {self.blank_idx: self.blank_token}

    # --------------------------------------------------
    # Vocabulary building
    # --------------------------------------------------
    def build_vocab(self, labels):
        """
        Build character-level vocabulary from labels
        """
        idx = 1  # start after blank

        for label in labels:
            for ch in label:
                if ch == " ":
                    continue
                if ch not in self.stoi:
                    self.stoi[ch] = idx
                    self.itos[idx] = ch
                    idx += 1

    # --------------------------------------------------
    # Encoding
    # --------------------------------------------------
    def encode(self, text):
        """
        Convert string to list of token IDs
        Unknown characters are safely ignored.
        """
        encoded = []
        for ch in text:
            if ch == " ":
                continue
            if ch in self.stoi:
                encoded.append(self.stoi[ch])
            # else: silently skip unknown token
        return encoded

    # --------------------------------------------------
    # Decoding (baseline greedy CTC only)
    # --------------------------------------------------
    def decode(self, token_ids):
        """
        Greedy CTC decoding:
        - collapse repeats
        - remove blanks

        NOTE:
        This is for baseline / debugging only.
        Beam search decoding is handled separately.
        """
        decoded = []
        prev = None

        for t in token_ids:
            if t != prev and t != self.blank_idx:
                if t in self.itos:
                    decoded.append(self.itos[t])
            prev = t

        return "".join(decoded)

    # --------------------------------------------------
    # Helpers
    # --------------------------------------------------
    def vocab_size(self):
        return len(self.stoi)

    def is_digit_token(self, idx):
        """
        Utility for digit-aware decoding or analysis
        """
        return idx in self.itos and self.itos[idx].isdigit()
