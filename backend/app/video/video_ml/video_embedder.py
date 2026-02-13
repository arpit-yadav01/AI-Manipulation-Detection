import numpy as np
from typing import List, Dict, Any


def _normalize(vec: np.ndarray) -> np.ndarray:
    """
    L2 normalize vector (safe).
    """
    norm = np.linalg.norm(vec)
    if norm == 0:
        return vec
    return vec / norm


def aggregate_face_embeddings(frames: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Phase 3 · Step 2
    Aggregate face embeddings across frames into
    a single video-level embedding + drift signal.
    """

    embeddings = []

    for frame in frames:
        emb = frame.get("face_embedding")
        if emb is None:
            continue

        # Convert safely to numpy
        vec = np.array(emb, dtype=np.float32)

        if vec.ndim != 1:
            continue

        embeddings.append(_normalize(vec))

    if len(embeddings) < 3:
        return {
            "frames_used": len(embeddings),
            "embedding": None,
            "identity_drift": None,
        }

    E = np.stack(embeddings)  # (N, D)

    # -----------------------------
    # Video-level embedding
    # -----------------------------
    mean_embedding = _normalize(np.mean(E, axis=0))

    # -----------------------------
    # Identity drift (temporal)
    # -----------------------------
    # cosine distance between consecutive frames
    drifts = []

    for i in range(1, len(E)):
        sim = float(np.dot(E[i - 1], E[i]))
        drift = 1.0 - sim
        drifts.append(drift)

    drift_mean = float(np.mean(drifts))
    drift_std = float(np.std(drifts))

    return {
        "frames_used": len(embeddings),

        # ⚠️ NOT for MongoDB storage
        "embedding": mean_embedding.tolist(),

        # forensic identity instability
        "identity_drift": {
            "mean": drift_mean,
            "std": drift_std,
            "max": float(np.max(drifts)),
        },
    }
