import cv2
import numpy as np


def analyze_motion_consistency(frame_paths):
    flows = []

    for i in range(len(frame_paths) - 1):
        f1 = cv2.imread(frame_paths[i], cv2.IMREAD_GRAYSCALE)
        f2 = cv2.imread(frame_paths[i + 1], cv2.IMREAD_GRAYSCALE)

        if f1 is None or f2 is None:
            continue

        flow = cv2.calcOpticalFlowFarneback(
            f1, f2, None,
            0.5, 3, 15, 3, 5, 1.2, 0
        )

        mag, _ = cv2.cartToPolar(flow[..., 0], flow[..., 1])
        flows.append(np.mean(mag))

    if not flows:
        return {
            "motion_variance": None,
            "verdict": "insufficient_data"
        }

    variance = np.var(flows)

    verdict = (
        "unnatural_motion"
        if variance > 1.5
        else "natural_motion"
    )

    return {
        "motion_variance": round(float(variance), 3),
        "verdict": verdict
    }
