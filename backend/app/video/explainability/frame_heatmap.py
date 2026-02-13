from typing import List, Dict, Any


def explain_frames(
    frame_results: List[Dict[str, Any]],
    top_k: int = 3,
) -> Dict[str, Any]:
    """
    Phase 3 — Frame-Level Explainability (SAFE)

    PURPOSE:
    - Highlight frames with stronger forensic signals
    - Describe relative signal intensity
    - NO verdicts
    - NO thresholds
    - NO classification language
    """

    if not isinstance(frame_results, list) or not frame_results:
        return {
            "type": "frame_heatmap",
            "available": False,
            "explanation": "No frame-level analysis was available.",
            "frames": [],
        }

    # Sort frames by signal strength (pure ordering, no interpretation)
    sorted_frames = sorted(
        frame_results,
        key=lambda x: float(x.get("ml_fake_probability", 0.0)),
        reverse=True,
    )[:top_k]

    frames = []

    for idx, frame in enumerate(sorted_frames):
        prob = float(frame.get("ml_fake_probability", 0.0))

        frames.append({
            "frame_index": frame.get("frame_index", idx),
            "timestamp": frame.get("timestamp"),
            "signal_strength": round(prob, 4),
            "description": (
                "This frame exhibits comparatively stronger model response "
                "relative to other analyzed frames."
                if prob > 0.0
                else "This frame shows low model response relative to others."
            ),
        })

    return {
        "type": "frame_heatmap",
        "available": True,
        "frames": frames,
        "explanation": (
            "This view highlights frames that elicited stronger responses "
            "from frame-level analysis models. Signal strength values "
            "are shown for comparison only and do not represent a verdict."
        ),
    }
