class CTCTokenizer:
    def __init__(self):
        # CTC blank token MUST be 0
        self.blank_token = "<blank>"
        self.stoi = {self.blank_token: 0}
        self.itos = {0: self.blank_token}

    def build_vocab(self, labels):
        idx = 1  # start after blank

        for label in labels:
            for ch in label:
                if ch == " ":
                    continue
                if ch not in self.stoi:
                    self.stoi[ch] = idx
                    self.itos[idx] = ch
                    idx += 1

    def encode(self, text):
        """
        Convert string to list of token IDs
        """
        return [self.stoi[ch] for ch in text if ch != " "]

    def decode(self, token_ids):
        """
        Greedy CTC decoding:
        - remove repeats
        - remove blanks
        """
        decoded = []
        prev = None

        for t in token_ids:
            if t != prev and t != 0:
                decoded.append(self.itos[t])
            prev = t

        return "".join(decoded)

    def vocab_size(self):
        return len(self.stoi)
