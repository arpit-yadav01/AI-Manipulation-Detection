import cv2
import numpy as np


def compute_prnu_score(image_path: str) -> float:
    """
    Simple industry-grade PRNU strength estimator.
    NOT camera identification.
    """

    try:
        # 1️⃣ Load image in grayscale
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            return 0.0

        img = img.astype(np.float32)

        # 2️⃣ Remove image content using Gaussian blur
        denoised = cv2.GaussianBlur(img, (5, 5), 0)

        # 3️⃣ Extract noise residual
        noise = img - denoised

        # 4️⃣ Normalize noise
        noise_std = np.std(noise)

        # 5️⃣ Convert to readable score
        prnu_score = float(noise_std * 10)

        return round(prnu_score, 3)

    except Exception:
        return 0.0
