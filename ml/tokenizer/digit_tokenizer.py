class DigitCTCTokenizer:
    """
    CTC tokenizer for digit-only pretraining.
    Vocabulary:
        <blank> 0 1 2 3 4 5 6 7 8 9
    """

    def __init__(self):
        self.blank_token = "<blank>"
        self.blank_idx = 0

        self.stoi = {self.blank_token: self.blank_idx}
        self.itos = {self.blank_idx: self.blank_token}

        idx = 1
        for d in range(10):
            self.stoi[str(d)] = idx
            self.itos[idx] = str(d)
            idx += 1

    def encode(self, text):
        return [self.stoi[ch] for ch in text if ch.isdigit()]

    def decode(self, token_ids):
        decoded = []
        prev = None
        for t in token_ids:
            if t != prev and t != self.blank_idx:
                decoded.append(self.itos[t])
            prev = t
        return "".join(decoded)

    def vocab_size(self):
        return len(self.stoi)

if __name__ == "__main__":
    tok = DigitCTCTokenizer()
    print(tok.encode("120"))
    print(tok.decode([1, 2, 3, 0, 3]))
