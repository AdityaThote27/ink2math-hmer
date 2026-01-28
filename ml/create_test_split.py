import random
from dataset.crohme_dataset import CROHMEDataset

random.seed(42)

dataset = CROHMEDataset(year="2014")
samples = dataset.samples  # (image_path, label)

total = len(samples)
test_size = int(0.2 * total)

random.shuffle(samples)

test_samples = samples[:test_size]
train_samples = samples[test_size:]

print(f"Total samples: {total}")
print(f"Train samples: {len(train_samples)}")
print(f"Test samples: {len(test_samples)}")

# Save test set
with open("test_samples.txt", "w", encoding="utf-8") as f:
    for img, label in test_samples:
        f.write(f"{img}\t{label}\n")

print("✅ Test split saved to test_samples.txt")
