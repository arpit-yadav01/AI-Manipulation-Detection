# app/video/explainability/temporal_explainer.py

from typing import Dict, Any, Optional


def explain_temporal(
    temporal_signal: Optional[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Phase 3 — Temporal Explainability

    PURPOSE:
    - Describe frame-to-frame temporal behavior
    - NO thresholds
    - NO verdicts
    - NO confidence changes
    """

    if not isinstance(temporal_signal, dict):
        return {
            "type": "temporal",
            "available": False,
            "explanation": "Temporal consistency analysis was not available.",
        }

    if temporal_signal.get("available") is False:
        return {
            "type": "temporal",
            "available": False,
            "explanation": temporal_signal.get(
                "reason",
                "Temporal consistency analysis could not be performed."
            ),
        }

    observations = {}

    if "stability_score" in temporal_signal:
        observations["stability_score"] = temporal_signal["stability_score"]

    if "variance" in temporal_signal:
        observations["variance"] = temporal_signal["variance"]

    explanation = (
        "This signal describes how visual patterns evolve across consecutive frames. "
        "Higher variation suggests changing temporal structure, while lower variation "
        "indicates more consistent transitions."
    )

    return {
        "type": "temporal",
        "available": True,
        "observations": observations,
        "explanation": explanation,
    }
