import cv2
import numpy as np
import subprocess
from typing import Dict, List
import json


# --------------------------------------------------
# Helper: extract per-second bitrate curve
# --------------------------------------------------

def _extract_bitrate_curve(video_path: str) -> List[float]:
    try:
        cmd = [
            "ffprobe",
            "-select_streams", "v",
            "-show_frames",
            "-show_entries", "frame=pkt_size",
            "-of", "json",
            video_path,
        ]

        result = subprocess.run(
            cmd, capture_output=True, text=True, check=True
        )
        data = json.loads(result.stdout)

        sizes = [
            int(f["pkt_size"])
            for f in data.get("frames", [])
            if "pkt_size" in f
        ]

        if len(sizes) < 30:
            return []

        chunk = 30  # ~30 fps
        return [
            sum(sizes[i:i + chunk])
            for i in range(0, len(sizes), chunk)
        ]

    except Exception:
        return []


# --------------------------------------------------
# Helper: compression entropy estimate
# --------------------------------------------------

def _estimate_block_entropy(frame: np.ndarray) -> float:
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    h, w = gray.shape

    entropies = []

    for y in range(0, h - 8, 8):
        for x in range(0, w - 8, 8):
            block = gray[y:y + 8, x:x + 8]
            hist = np.bincount(block.flatten(), minlength=256)
            prob = hist / (np.sum(hist) + 1e-6)
            prob = prob[prob > 0]
            entropies.append(-np.sum(prob * np.log2(prob)))

    return float(np.mean(entropies)) if entropies else 0.0


# --------------------------------------------------
# MAIN — Phase 4 detector (READ-ONLY)
# --------------------------------------------------

def analyze_reencoding(video_path: str) -> Dict:
    """
    Phase 4 — Re-encoding & Compression Abuse Detector

    RULES:
    - No verdicts
    - No confidence
    - No thresholds implying judgment
    """

    signals = []
    score = 0.0

    # ------------------------------
    # Bitrate stability signal
    # ------------------------------
    bitrate_curve = _extract_bitrate_curve(video_path)

    if len(bitrate_curve) >= 3:
        variance_ratio = np.std(bitrate_curve) / (np.mean(bitrate_curve) + 1e-6)
        score += float(max(0.0, min(0.3, 0.3 - variance_ratio)))
        signals.append("bitrate_uniformity")

    # ------------------------------
    # Compression entropy signal
    # ------------------------------
    cap = cv2.VideoCapture(video_path)
    entropies = []

    for _ in range(12):
        ret, frame = cap.read()
        if not ret:
            break
        entropies.append(_estimate_block_entropy(frame))

    cap.release()

    if entropies:
        entropy_mean = float(np.mean(entropies))
        score += float(max(0.0, min(0.3, (4.8 - entropy_mean) / 4.8)))
        signals.append("low_entropy_blocks")

    return {
        "available": True,
        "score": round(float(min(score, 1.0)), 3),
        "signals": signals,
    }
