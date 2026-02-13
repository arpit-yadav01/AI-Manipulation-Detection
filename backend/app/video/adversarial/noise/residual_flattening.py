import numpy as np
import cv2
from typing import List


# --------------------------------------------------
# CONFIG (SOFT HEURISTICS ONLY)
# --------------------------------------------------
MIN_FRAMES = 8
FLATTENING_SENSITIVITY = 0.45


def _compute_residual_energy(image_path: str) -> float | None:
    """
    Computes high-frequency residual energy of an image.
    """
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        return None

    img = img.astype(np.float32)

    blurred = cv2.GaussianBlur(img, (5, 5), 0)
    residual = img - blurred

    return float(np.mean(np.abs(residual)))


def analyze_residual_flattening(frame_paths: List[str]) -> dict:
    """
    Phase 4 — Residual Flattening Analysis (READ-ONLY)

    PURPOSE:
    - Detect unnaturally suppressed high-frequency residuals
    - Indicates aggressive denoising or diffusion-based smoothing
    """

    energies = []

    for path in frame_paths:
        e = _compute_residual_energy(path)
        if e is not None:
            energies.append(e)

    if len(energies) < MIN_FRAMES:
        return {
            "available": False,
            "score": 0.0,
            "signals": [],
        }

    energies = np.array(energies, dtype=np.float32)

    mean_energy = float(np.mean(energies))
    std_energy = float(np.std(energies))

    if mean_energy <= 0:
        return {
            "available": True,
            "score": 0.25,
            "signals": ["invalid_residual_measurement"],
        }

    variation_ratio = std_energy / (mean_energy + 1e-6)

    score = min(0.35, (1.0 - variation_ratio) * FLATTENING_SENSITIVITY)
    signals = []

    if variation_ratio < 0.2:
        signals.append("suppressed_high_frequency_residuals")

    return {
        "available": True,
        "score": round(max(score, 0.0), 3),
        "signals": signals,
    }
