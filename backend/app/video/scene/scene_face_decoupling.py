import numpy as np
from typing import List, Dict
from scipy.stats import pearsonr


def _safe_norm_diff(a: np.ndarray, b: np.ndarray) -> float:
    """
    Normalized L2 difference (robust).
    """
    return float(np.linalg.norm(a - b))


def analyze_scene_face_decoupling(
    face_embeddings: List[np.ndarray],
    scene_embeddings: List[np.ndarray],
    min_pairs: int = 6,
) -> Dict:
    """
    STEP 3.2.2 — Scene ↔ Face Decoupling

    Measures whether face changes are physically correlated
    with scene changes over time.
    """

    # --------------------------------------------------
    # Clean inputs
    # --------------------------------------------------
    faces = [f for f in face_embeddings if f is not None]
    scenes = [s for s in scene_embeddings if s is not None]

    n = min(len(faces), len(scenes))

    if n < min_pairs:
        return {
            "available": False,
            "reason": "insufficient_pairs",
        }

    faces = faces[:n]
    scenes = scenes[:n]

    # --------------------------------------------------
    # Compute temporal deltas
    # --------------------------------------------------
    face_deltas = []
    scene_deltas = []

    for i in range(1, n):
        face_deltas.append(
            _safe_norm_diff(faces[i - 1], faces[i])
        )
        scene_deltas.append(
            _safe_norm_diff(scenes[i - 1], scenes[i])
        )

    face_deltas = np.array(face_deltas)
    scene_deltas = np.array(scene_deltas)

    # --------------------------------------------------
    # Correlation analysis
    # --------------------------------------------------
    if np.std(face_deltas) == 0 or np.std(scene_deltas) == 0:
        corr = 0.0
    else:
        corr, _ = pearsonr(face_deltas, scene_deltas)

    corr = float(corr)

    # --------------------------------------------------
    # Verdict (conservative)
    # --------------------------------------------------
    if corr < 0.20:
        verdict = "decoupled"
    elif corr < 0.40:
        verdict = "weakly_coupled"
    else:
        verdict = "coupled"

    return {
        "available": True,
        "correlation": round(corr, 3),
        "frames_used": n,
        "verdict": verdict,
    }
