import cv2
import numpy as np

# ---------------------------------
# Extract noise (high-pass filter)
# ---------------------------------
def extract_noise(img_gray):
    blur = cv2.GaussianBlur(img_gray, (5, 5), 0)
    noise = img_gray.astype(np.float32) - blur.astype(np.float32)
    return noise


# ---------------------------------
# Block-wise PRNU Analyzer
# ---------------------------------
def analyze_prnu(image_path: str, block_size: int = 128):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    if img is None:
        return {
            "prnu_strength": 0.0,
            "prnu_consistency": 0.0,
            "prnu_verdict": "UNKNOWN"
        }

    noise = extract_noise(img)

    h, w = noise.shape
    strengths = []

    for y in range(0, h - block_size, block_size):
        for x in range(0, w - block_size, block_size):
            block = noise[y:y + block_size, x:x + block_size]
            strength = np.std(block)
            strengths.append(strength)

    if not strengths:
        return {
            "prnu_strength": 0.0,
            "prnu_consistency": 0.0,
            "prnu_verdict": "UNKNOWN"
        }

    mean_strength = float(np.mean(strengths))
    std_strength = float(np.std(strengths))
    consistency = float(1.0 - (std_strength / (mean_strength + 1e-6)))

    if mean_strength > 60 and consistency > 0.7:
        verdict = "CAMERA_LIKELY"
    elif mean_strength < 35:
        verdict = "WEAK_OR_NONE"
    else:
        verdict = "INCONSISTENT"

    return {
        "prnu_strength": round(mean_strength, 3),
        "prnu_consistency": round(consistency, 3),
        "prnu_verdict": verdict
    }
