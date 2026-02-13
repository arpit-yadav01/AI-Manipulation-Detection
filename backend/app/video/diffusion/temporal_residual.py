import cv2
import numpy as np
from typing import List, Dict, Optional
from sklearn.metrics.pairwise import cosine_similarity


# ============================================================
# TEMPORAL NOISE RESIDUAL STABILITY (DIFFUSION-SPECIFIC)
# ============================================================

def _extract_residual(gray: np.ndarray) -> np.ndarray:
    """
    High-frequency residual extraction.
    """
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    residual = gray.astype(np.float32) - blur.astype(np.float32)
    return residual


def _normalize(vec: np.ndarray) -> np.ndarray:
    norm = np.linalg.norm(vec)
    if norm < 1e-6:
        return vec
    return vec / norm


def analyze_temporal_residual_stability(
    frame_paths: List[str]
) -> Optional[Dict]:
    """
    Measures temporal similarity of noise residuals.

    Diffusion models tend to regenerate texture with
    unnaturally stable residual statistics across frames.

    SAFE MODE:
    - No thresholds
    - No verdict
    - No failure escalation
    """

    residual_vectors = []

    for path in frame_paths:
        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            continue

        img = cv2.resize(img, (256, 256))
        residual = _extract_residual(img)

        # Flatten & normalize
        vec = residual.flatten()
        vec = _normalize(vec)

        residual_vectors.append(vec)

    if len(residual_vectors) < 5:
        return {
            "available": False,
            "reason": "not_enough_frames",
        }

    residual_vectors = np.stack(residual_vectors)

    # --------------------------------------------------------
    # Pairwise cosine similarity (temporal texture consistency)
    # --------------------------------------------------------
    similarities = cosine_similarity(residual_vectors)

    # Use upper triangle only (ignore self-similarity)
    triu_indices = np.triu_indices_from(similarities, k=1)
    sim_values = similarities[triu_indices]

    return {
        "available": True,

        # Mean similarity between residuals
        "mean_cosine_similarity": round(
            float(np.mean(sim_values)), 6
        ),

        # Stability variance (lower = suspicious)
        "similarity_variance": round(
            float(np.var(sim_values)), 6
        ),

        # Extreme similarity occurrences
        "high_similarity_ratio": round(
            float(np.mean(sim_values > 0.9)), 6
        ),

        # Research-only stability proxy
        "temporal_stability_score": round(
            float(
                np.mean(sim_values) *
                (1.0 - np.var(sim_values))
            ),
            6
        ),

        "frames_used": int(len(residual_vectors)),
    }
