from collections import Counter

PAD = "<PAD>"
SOS = "<SOS>"
EOS = "<EOS>"

class Tokenizer:
    def __init__(self):
        self.stoi = {PAD: 0, SOS: 1, EOS: 2}
        self.itos = {0: PAD, 1: SOS, 2: EOS}

    def build_vocab(self, labels, min_freq=1):
        counter = Counter()
        for l in labels:
            counter.update(l.split())

        for token, freq in counter.items():
            if freq >= min_freq and token not in self.stoi:
                idx = len(self.stoi)
                self.stoi[token] = idx
                self.itos[idx] = token

    def encode(self, text):
        tokens = text.split()
        ids = [self.stoi[SOS]] + [self.stoi[t] for t in tokens] + [self.stoi[EOS]]
        return ids

    def vocab_size(self):
        return len(self.stoi)
