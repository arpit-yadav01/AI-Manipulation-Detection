import cv2
import numpy as np
from typing import List, Dict, Optional


# ============================================================
# DIFFUSION NOISE RESIDUAL ANALYSIS (RESEARCH-ONLY)
# ============================================================

def _high_pass_residual(gray: np.ndarray) -> np.ndarray:
    """
    Extract high-frequency residual using Gaussian blur subtraction.
    """
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    residual = gray.astype(np.float32) - blur.astype(np.float32)
    return residual


def _fft_energy_ratio(residual: np.ndarray) -> float:
    """
    Compute ratio of high-frequency FFT energy to total energy.
    """
    fft = np.fft.fft2(residual)
    fft_shift = np.fft.fftshift(fft)
    magnitude = np.abs(fft_shift)

    h, w = magnitude.shape
    center_h, center_w = h // 2, w // 2

    low_freq_radius = min(h, w) // 8
    y, x = np.ogrid[:h, :w]
    mask = (y - center_h) ** 2 + (x - center_w) ** 2 > low_freq_radius ** 2

    high_energy = np.sum(magnitude[mask])
    total_energy = np.sum(magnitude) + 1e-6

    return float(high_energy / total_energy)


def analyze_diffusion_noise(
    frame_paths: List[str]
) -> Optional[Dict]:
    """
    Research-grade diffusion noise residual analysis.

    SAFE GUARANTEES:
    - No verdict
    - No thresholds
    - No classification
    - Fail-open

    Returns structured statistics only.
    """

    residual_energies = []
    fft_ratios = []

    for path in frame_paths:
        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            continue

        img = cv2.resize(img, (256, 256))
        residual = _high_pass_residual(img)

        residual_energy = float(np.var(residual))
        fft_ratio = _fft_energy_ratio(residual)

        residual_energies.append(residual_energy)
        fft_ratios.append(fft_ratio)

    if len(residual_energies) < 5:
        return {
            "available": False,
            "reason": "not_enough_frames",
        }

    residual_energies = np.array(residual_energies)
    fft_ratios = np.array(fft_ratios)

    return {
        "available": True,

        # Texture smoothness / over-regularization
        "residual_energy": round(float(np.mean(residual_energies)), 6),

        # Frequency-domain fingerprint
        "fft_high_freq_ratio": round(float(np.mean(fft_ratios)), 6),

        # Temporal stability (diffusion re-generation hint)
        "temporal_consistency": round(
            float(np.var(residual_energies)), 6
        ),

        # Research-only combined anomaly proxy
        "anomaly_score": round(
            float(
                0.5 * np.mean(fft_ratios) +
                0.5 * np.var(residual_energies)
            ),
            6
        ),

        "frames_used": int(len(residual_energies)),
    }
