import numpy as np
import cv2
from typing import List


# --------------------------------------------------
# CONFIG (SOFT, NON-DECISIONAL)
# --------------------------------------------------
MIN_FRAMES = 8
STABILITY_SENSITIVITY = 0.4


def _estimate_noise_level(image_path: str) -> float | None:
    """
    Estimate image noise using high-frequency residuals.
    """
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        return None

    img = img.astype(np.float32)
    lap = cv2.Laplacian(img, cv2.CV_32F)

    return float(np.std(lap))


def analyze_noise_floor_shift(frame_paths: List[str]) -> dict:
    """
    Phase 4 — Noise Floor Stability Analysis (READ-ONLY)

    PURPOSE:
    - Detect unnaturally stable noise floors caused by denoising or generative pipelines
    - Soft adversarial awareness only
    """

    noise_levels = []

    for path in frame_paths:
        n = _estimate_noise_level(path)
        if n is not None:
            noise_levels.append(n)

    if len(noise_levels) < MIN_FRAMES:
        return {
            "available": False,
            "score": 0.0,
            "signals": [],
        }

    noise_levels = np.array(noise_levels, dtype=np.float32)

    mean_noise = float(np.mean(noise_levels))
    std_noise = float(np.std(noise_levels))

    if mean_noise <= 0:
        return {
            "available": True,
            "score": 0.25,
            "signals": ["invalid_noise_measurement"],
        }

    variation_ratio = std_noise / (mean_noise + 1e-6)

    score = min(0.35, (1.0 - variation_ratio) * STABILITY_SENSITIVITY)
    signals = []

    if variation_ratio < 0.12:
        signals.append("unnaturally_stable_noise_floor")

    return {
        "available": True,
        "score": round(max(score, 0.0), 3),
        "signals": signals,
    }
