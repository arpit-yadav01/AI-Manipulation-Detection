import os
from PIL import Image

DATASET_DIR = "datasets/image_ml"

bad_files = []

for cls in ["real", "fake"]:
    cls_dir = os.path.join(DATASET_DIR, cls)

    for root, _, files in os.walk(cls_dir):
        for file in files:
            path = os.path.join(root, file)
            try:
                with Image.open(path) as img:
                    img.verify()   # check integrity
            except Exception:
                bad_files.append(path)

print(f"❌ Found {len(bad_files)} corrupted images")

for f in bad_files:
    print("Deleting:", f)
    os.remove(f)

print("✅ Cleanup complete")


