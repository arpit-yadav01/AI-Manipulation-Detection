# app/video/timeline/second_aggregation.py

from typing import List, Dict
from collections import defaultdict


def aggregate_frames_to_seconds(
    frames: List[Dict],
    frames_per_second: int = 3,
) -> List[Dict]:
    """
    Phase 7.2 — Aggregate frame scores into per-second scores

    RULES:
    - Read-only
    - Conservative
    - UI-safe
    """

    buckets = defaultdict(list)

    for f in frames:
        sec = int(f["timestamp"])
        buckets[sec].append(f)

    second_scores = []

    for sec, items in sorted(buckets.items()):
        scores = [f["score"] for f in items]

        avg_score = sum(scores) / len(scores)

        if avg_score >= 0.7:
            label = "manipulated"
        elif avg_score >= 0.4:
            label = "suspicious"
        else:
            label = "real"

        second_scores.append({
            "second": sec,
            "avg_score": round(avg_score, 3),
            "label": label,
            "frames_used": len(items),
        })

    return second_scores
