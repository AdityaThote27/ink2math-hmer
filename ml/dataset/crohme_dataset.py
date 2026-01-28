import os
import cv2
import torch
from torch.utils.data import Dataset


class CROHMEDataset(Dataset):
    def __init__(self, year="2014", root=None):
        # --------------------------------------------------
        # Resolve dataset root robustly
        # --------------------------------------------------
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))

        if root is None:
            # ml/dataset/ -> ml/data/
            root = os.path.join(BASE_DIR, "..", "data")

        self.img_dir = os.path.join(root, "images", year)
        self.label_file = os.path.join(root, "labels", year, "caption.txt")

        self.samples = []

        total = 0
        missing = 0

        # --------------------------------------------------
        # Load labels
        # --------------------------------------------------
        with open(self.label_file, "r", encoding="utf-8") as f:
            for line in f:
                total += 1
                parts = line.strip().split()

                img_name = parts[0] + ".bmp"
                label = " ".join(parts[1:])

                img_path = os.path.join(self.img_dir, img_name)
                if not os.path.exists(img_path):
                    missing += 1
                    continue  # skip invalid entry

                self.samples.append((img_name, label))

        print(
            f"[CROHME-{year}] Total labels: {total} | "
            f"Valid samples: {len(self.samples)} | "
            f"Missing images: {missing}"
        )

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        img_name, label = self.samples[idx]
        img_path = os.path.join(self.img_dir, img_name)

        image = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        image = cv2.resize(image, (256, 256))
        image = image.astype("float32") / 255.0
        image = torch.from_numpy(image).unsqueeze(0)

        return image, label
