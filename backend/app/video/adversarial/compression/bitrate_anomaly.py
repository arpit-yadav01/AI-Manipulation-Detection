import subprocess
import json


def _probe_bitrate(video_path: str):
    """
    Uses ffprobe to extract average stream bitrate (kbps).
    """
    try:
        cmd = [
            "ffprobe",
            "-v", "error",
            "-select_streams", "v:0",
            "-show_entries", "stream=bit_rate",
            "-of", "json",
            video_path,
        ]

        out = subprocess.check_output(cmd, stderr=subprocess.DEVNULL)
        data = json.loads(out)

        bit_rate = data["streams"][0].get("bit_rate")
        if bit_rate is None:
            return None

        return int(bit_rate) / 1000.0  # kbps

    except Exception:
        return None


def analyze_bitrate_anomaly(video_path: str) -> dict:
    """
    Phase 4 — Bitrate Anomaly Detector (READ-ONLY)

    RULES:
    - No verdicts
    - No confidence
    - No hard decisions
    """

    bitrate = _probe_bitrate(video_path)

    if bitrate is None:
        return {
            "available": False,
            "score": 0.0,
            "signals": [],
        }

    signals = []
    score = 0.0

    # Soft suspicion mapping (no thresholds implying judgment)
    if bitrate < 1000:
        score += min(0.3, (1000 - bitrate) / 1000)
        signals.append("low_average_bitrate")

    if bitrate < 500:
        score += 0.2
        signals.append("extremely_low_bitrate")

    return {
        "available": True,
        "score": round(min(score, 1.0), 3),
        "signals": signals,
    }
