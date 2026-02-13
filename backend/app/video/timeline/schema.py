# app/video/timeline/schema.py

from typing import List, Dict, Any


def build_video_timeline_schema(
    *,
    frames: List[Dict[str, Any]],
    seconds: List[Dict[str, Any]],
    segments: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """
    Phase 7.4 — Timeline Schema (UI-safe)

    RULES:
    - No raw model outputs
    - No embeddings
    - No thresholds
    """

    return {
        "available": True,
        "frame_level": [
            {
                "timestamp": f["timestamp"],
                "score": f["score"],
                "label": f["label"],
            }
            for f in frames
        ],
        "second_level": [
            {
                "second": s["second"],
                "score": s["avg_score"],
                "label": s["label"],
            }
            for s in seconds
        ],
        "segments": segments,
    }
