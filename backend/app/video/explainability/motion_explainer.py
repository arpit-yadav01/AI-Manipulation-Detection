# app/video/explainability/motion_explainer.py

from typing import Dict, Any, Optional


def explain_motion(
    motion_signal: Optional[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Phase 3 — Motion Explainability

    PURPOSE:
    - Describe motion dynamics across frames
    - NO verdicts
    - NO thresholds
    - NO confidence changes
    """

    if not isinstance(motion_signal, dict):
        return {
            "type": "motion",
            "available": False,
            "explanation": "Motion analysis was not available.",
        }

    if motion_signal.get("available") is False:
        return {
            "type": "motion",
            "available": False,
            "explanation": motion_signal.get(
                "reason",
                "Motion analysis could not be performed."
            ),
        }

    observations = {}

    if "motion_variance" in motion_signal:
        observations["motion_variance"] = motion_signal["motion_variance"]

    if "trajectory_smoothness" in motion_signal:
        observations["trajectory_smoothness"] = motion_signal["trajectory_smoothness"]

    explanation = (
        "This signal summarizes how visual elements move across consecutive frames. "
        "It reflects changes in motion magnitude and smoothness over time, "
        "which can vary depending on scene dynamics, camera movement, and subject behavior."
    )

    return {
        "type": "motion",
        "available": True,
        "observations": observations,
        "explanation": explanation,
    }
