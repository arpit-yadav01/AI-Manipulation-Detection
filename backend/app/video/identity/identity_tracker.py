import numpy as np
from sklearn.metrics.pairwise import cosine_distances

def analyze_identity_consistency(face_embeddings):
    """
    VIDEO_V2.IDENTITY
    Measures identity drift across frames.
    """

    embeddings = [e for e in face_embeddings if e is not None]

    if len(embeddings) < 10:
        return {
            "verdict": "insufficient_data",
            "avg_drift": None,
            "confidence": 0.0
        }

    window = 5
    drifts = []

    for i in range(0, len(embeddings) - window, window):
        w1 = embeddings[i:i+window]
        w2 = embeddings[i+window:i+2*window]

        if len(w2) < window:
            break

        mean1 = np.mean(w1, axis=0).reshape(1, -1)
        mean2 = np.mean(w2, axis=0).reshape(1, -1)

        drift = cosine_distances(mean1, mean2)[0][0]
        drifts.append(drift)

    if not drifts:
        return {
            "verdict": "no_drift_detected",
            "avg_drift": 0.0,
            "confidence": 0.0
        }

    avg_drift = float(np.mean(drifts))

    if avg_drift > 0.15:
        verdict = "identity_unstable"
        confidence = 0.15
    elif avg_drift > 0.08:
        verdict = "mild_identity_drift"
        confidence = 0.08
    else:
        verdict = "identity_stable"
        confidence = 0.0

    return {
        "verdict": verdict,
        "avg_drift": round(avg_drift, 3),
        "confidence": confidence
    }
