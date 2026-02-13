import os
from PIL import Image

# Base directory where uploaded files live
UPLOAD_DIR = "datasets/uploads"
THUMBNAIL_DIR = "datasets/uploads/thumbnails"

os.makedirs(THUMBNAIL_DIR, exist_ok=True)


def generate_thumbnail(image_path: str, size=(256, 256)) -> str:
    """
    Generates a thumbnail for the uploaded image.
    Returns relative thumbnail path.
    """
    try:
        img = Image.open(image_path).convert("RGB")
        img.thumbnail(size)

        filename = os.path.basename(image_path)
        thumb_path = os.path.join(THUMBNAIL_DIR, filename)

        img.save(thumb_path, format="JPEG", quality=85)

        return thumb_path
    except Exception as e:
        print("❌ Thumbnail generation failed:", e)
        return None
