from ml.dataset.crohme_dataset import CROHMEDataset

ds = CROHMEDataset(year="2014")

print("Class:", type(ds))
print("Samples:", len(ds))

img, label = ds[0]
print("Image shape:", img.shape)
print("Label:", label)
