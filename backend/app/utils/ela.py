from PIL import Image, ImageChops, ImageEnhance
import numpy as np
import os
import tempfile


def compute_ela_score(image_path: str, quality: int = 90) -> float:
    """
    Compute Error Level Analysis (ELA) score for an image.

    Returns:
        float: mean pixel intensity difference
    """

    original = Image.open(image_path).convert("RGB")

    # Save recompressed copy
    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
        temp_path = tmp.name

    original.save(temp_path, "JPEG", quality=quality)

    recompressed = Image.open(temp_path)

    # Compute difference
    diff = ImageChops.difference(original, recompressed)

    # Enhance differences
    enhancer = ImageEnhance.Brightness(diff)
    diff = enhancer.enhance(10)

    # Convert to numpy
    diff_np = np.asarray(diff, dtype=np.float32)

    # Cleanup
    os.remove(temp_path)

    # Mean difference = ELA score
    return float(diff_np.mean())
