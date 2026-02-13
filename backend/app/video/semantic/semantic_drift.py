import numpy as np


def bbox_area(b):
    x1, y1, x2, y2 = b
    return max(1, (x2 - x1) * (y2 - y1))


def compute_semantic_drift(tracks):
    """
    Measures how much object geometry changes over time.
    """

    if len(tracks) < 3:
        return {
            "verdict": "insufficient_data",
            "confidence": 0.0,
        }

    areas = [bbox_area(t["bbox"]) for t in tracks]

    variance = float(np.var(areas))
    mean_area = float(np.mean(areas))

    normalized_drift = variance / max(mean_area, 1.0)

    if normalized_drift > 0.35:
        verdict = "semantic_drift_detected"
        confidence = min(0.15, normalized_drift)
    elif normalized_drift > 0.2:
        verdict = "mild_semantic_drift"
        confidence = min(0.08, normalized_drift)
    else:
        verdict = "stable"
        confidence = 0.0

    return {
        "verdict": verdict,
        "confidence": round(confidence, 3),
        "drift_score": round(normalized_drift, 3),
    }
