import cv2
import numpy as np


def estimate_lighting(image_path: str):
    """
    Rough lighting asymmetry estimator.
    Returns brightness + direction or None.
    """

    image = cv2.imread(image_path)
    if image is None:
        return None

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    h, w = gray.shape

    left = gray[:, :w // 2]
    right = gray[:, w // 2:]

    left_mean = np.mean(left)
    right_mean = np.mean(right)

    diff = left_mean - right_mean

    direction = (
        "LEFT" if diff > 15 else
        "RIGHT" if diff < -15 else
        "CENTER"
    )

    return {
        "left_brightness": round(float(left_mean), 2),
        "right_brightness": round(float(right_mean), 2),
        "difference": round(float(diff), 2),
        "direction": direction,
    }
