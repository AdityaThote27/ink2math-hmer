from torch.utils.data import Dataset
from ml.dataset.crohme_dataset import CROHMEDataset


class DigitDataset(Dataset):
    """
    Dataset containing ONLY digit-based samples.
    Examples:
        '1'
        '2'
        '12'
        '20'
    """

    def __init__(self, year="2014"):
        self.base = CROHMEDataset(year=year)
        self.samples = []

        for img, label in self.base:
            clean = label.replace(" ", "")
            if clean.isdigit():
                self.samples.append((img, clean))

        print(f"[DigitDataset] Total digit samples: {len(self.samples)}")

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        return self.samples[idx]

if __name__ == "__main__":
    ds = DigitDataset()
    for i in range(10):
        _, label = ds[i]
        print(label)
