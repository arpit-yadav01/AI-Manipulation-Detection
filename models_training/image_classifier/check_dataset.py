import os
from PIL import Image

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)

DATASET_DIR = os.path.join(BASE_DIR, "datasets", "image_ml_split")

splits = ["train", "val", "test"]
classes = ["real", "fake"]

print("📁 Dataset root:", DATASET_DIR)
print("=" * 50)

for split in splits:
    print(f"\n🔍 Split: {split}")
    for cls in classes:
        path = os.path.join(DATASET_DIR, split, cls)
        count = 0

        if not os.path.exists(path):
            print(f"  ❌ Missing folder: {path}")
            continue

        for f in os.listdir(path):
            try:
                Image.open(os.path.join(path, f)).verify()
                count += 1
            except:
                print(f"  ⚠️ Corrupt image: {split}/{cls}/{f}")

        print(f"  ✅ {cls}: {count} images")
