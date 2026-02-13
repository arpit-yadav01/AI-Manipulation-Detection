# app/video/timeline/segment_detection.py

from typing import List, Dict


def detect_manipulated_segments(
    second_scores: List[Dict],
    min_length: int = 2,
) -> List[Dict]:
    """
    Phase 7.3 — Detect continuous manipulated segments

    RULES:
    - Read-only
    - No verdict override
    - Conservative merging

    Input:
    [
        {
            "second": int,
            "avg_score": float,
            "label": "real | suspicious | manipulated"
        }
    ]

    Output:
    [
        {
            "start": int,
            "end": int,
            "duration": int,
            "severity": "suspicious | manipulated"
        }
    ]
    """

    segments = []
    current = None

    for item in second_scores:
        label = item.get("label")
        sec = item.get("second")

        if label in ("manipulated", "suspicious"):
            if current is None:
                current = {
                    "start": sec,
                    "end": sec,
                    "severity": label,
                }
            else:
                current["end"] = sec
                if label == "manipulated":
                    current["severity"] = "manipulated"
        else:
            if current:
                duration = current["end"] - current["start"] + 1
                if duration >= min_length:
                    segments.append({
                        "start": current["start"],
                        "end": current["end"],
                        "duration": duration,
                        "severity": current["severity"],
                    })
                current = None

    # Flush last segment
    if current:
        duration = current["end"] - current["start"] + 1
        if duration >= min_length:
            segments.append({
                "start": current["start"],
                "end": current["end"],
                "duration": duration,
                "severity": current["severity"],
            })

    return segments
