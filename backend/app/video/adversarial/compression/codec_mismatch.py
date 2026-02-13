import subprocess
import json


def _probe_codec(video_path: str):
    try:
        cmd = [
            "ffprobe",
            "-v", "error",
            "-show_entries", "format=format_name",
            "-show_entries", "stream=codec_name,profile",
            "-of", "json",
            video_path,
        ]

        out = subprocess.check_output(cmd, stderr=subprocess.DEVNULL)
        return json.loads(out)

    except Exception:
        return None


def analyze_codec_mismatch(video_path: str) -> dict:
    """
    Phase 4 — Codec / Container Consistency Check (READ-ONLY)

    PURPOSE:
    - Detect unusual codec/container combinations often caused by re-encoding
    - Soft adversarial awareness only
    """

    meta = _probe_codec(video_path)

    if not meta:
        return {
            "available": False,
            "score": 0.0,
            "signals": [],
        }

    container = meta.get("format", {}).get("format_name", "")
    streams = meta.get("streams", [])

    if not streams:
        return {
            "available": False,
            "score": 0.0,
            "signals": [],
        }

    stream = streams[0]
    codec = stream.get("codec_name", "")
    profile = (stream.get("profile") or "").lower()

    score = 0.0
    signals = []

    # Soft inconsistencies (NO judgement)
    if "mp4" in container and codec not in ("h264", "hevc"):
        score += 0.25
        signals.append("unusual_codec_for_container")

    if codec == "h264" and profile and "baseline" not in profile:
        score += 0.15
        signals.append("non_baseline_h264_profile")

    return {
        "available": True,
        "score": round(min(score, 1.0), 3),
        "signals": signals,
    }
