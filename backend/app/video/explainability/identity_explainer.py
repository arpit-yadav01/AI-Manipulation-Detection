# app/video/explainability/identity_explainer.py

from typing import Dict, Any, Optional


def explain_identity(
    identity_signal: Optional[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Phase 3 — Identity Explainability

    PURPOSE:
    - Describe how facial identity similarity evolves across frames
    - NO verdicts
    - NO thresholds
    - NO classification language
    """

    if not isinstance(identity_signal, dict):
        return {
            "type": "identity",
            "available": False,
            "explanation": "Identity analysis was not available.",
        }

    if identity_signal.get("available") is False:
        return {
            "type": "identity",
            "available": False,
            "explanation": identity_signal.get(
                "reason",
                "Identity analysis could not be performed."
            ),
        }

    observations = {}

    if "mean_similarity" in identity_signal:
        observations["mean_similarity"] = identity_signal["mean_similarity"]

    if "variance" in identity_signal:
        observations["variance"] = identity_signal["variance"]

    if "max_distance" in identity_signal:
        observations["max_distance"] = identity_signal["max_distance"]

    explanation = (
        "This signal summarizes how facial identity embeddings compare across frames. "
        "It reflects the consistency of detected facial features over time. "
        "Variations can arise from pose changes, lighting differences, occlusion, "
        "or frame quality, and should be interpreted alongside other forensic signals."
    )

    return {
        "type": "identity",
        "available": True,
        "observations": observations,
        "explanation": explanation,
    }
