import os
import random
import shutil

# --------------------------------------------------
# Resolve project root safely
# models_training/image_classifier/split_dataset.py
# -> go up 2 levels (repo root)
# --------------------------------------------------
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(
    os.path.join(CURRENT_DIR, "..", "..")
)

SRC_DIR = os.path.join(PROJECT_ROOT, "datasets", "image_ml")
DST_DIR = os.path.join(PROJECT_ROOT, "datasets", "image_ml_split")

SPLITS = {
    "train": 0.8,
    "val": 0.1,
    "test": 0.1
}


CLASSES = ["real", "fake"]


def ensure_dirs():
    for split in SPLITS:
        for cls in CLASSES:
            os.makedirs(os.path.join(DST_DIR, split, cls), exist_ok=True)


def split_class(cls):
    src_cls_dir = os.path.join(SRC_DIR, cls)

    if not os.path.exists(src_cls_dir):
        raise RuntimeError(f"❌ Source folder missing: {src_cls_dir}")

    files = [
        f for f in os.listdir(src_cls_dir)
        if os.path.isfile(os.path.join(src_cls_dir, f))
    ]

    random.shuffle(files)

    n = len(files)
    train_end = int(n * SPLITS["train"])
    val_end = train_end + int(n * SPLITS["val"])

    splits = {
        "train": files[:train_end],
        "val": files[train_end:val_end],
        "test": files[val_end:]
    }

    for split, split_files in splits.items():
        for f in split_files:
            src = os.path.join(src_cls_dir, f)
            dst = os.path.join(DST_DIR, split, cls, f)
            shutil.copy2(src, dst)

    print(f"✅ {cls}: {n} images split")


if __name__ == "__main__":
    print("📁 Source:", SRC_DIR)
    print("📁 Destination:", DST_DIR)

    ensure_dirs()

    for cls in CLASSES:
        split_class(cls)

    print("🎯 Dataset split complete")
