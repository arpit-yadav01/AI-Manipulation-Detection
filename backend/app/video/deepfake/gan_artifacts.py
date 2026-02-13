import cv2
import numpy as np


def detect_gan_artifacts(frame_paths):
    scores = []

    for path in frame_paths:
        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            continue

        lap = cv2.Laplacian(img, cv2.CV_64F)
        score = lap.var()
        scores.append(score)

    if not scores:
        return {
            "artifact_score": None,
            "verdict": "insufficient_data"
        }

    mean_score = np.mean(scores)

    verdict = (
        "gan_artifacts_detected"
        if mean_score > 150
        else "no_gan_artifacts"
    )

    return {
        "artifact_score": round(float(mean_score), 2),
        "verdict": verdict
    }
