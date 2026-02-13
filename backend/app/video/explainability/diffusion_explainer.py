# app/video/explainability/diffusion_explainer.py

from typing import Dict, Any, List, Optional


def explain_diffusion(
    diffusion_evidence: Optional[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Phase 3 — Diffusion Explainability (READ-ONLY)

    PURPOSE:
    - Translate diffusion-related forensic signals into human-readable form
    - Describe observed residual patterns without interpretation or judgment

    RULES:
    - NO verdicts
    - NO thresholds
    - NO confidence manipulation
    - NO classification language
    """

    # --------------------------------------------------
    # Availability guard
    # --------------------------------------------------
    if not isinstance(diffusion_evidence, dict):
        return {
            "type": "diffusion",
            "available": False,
            "explanation": "Diffusion-based analysis was not available for this video.",
        }

    if diffusion_evidence.get("available") is False:
        return {
            "type": "diffusion",
            "available": False,
            "explanation": "Diffusion-related signals could not be reliably extracted.",
        }

    components = diffusion_evidence.get("components", {})
    observations: List[str] = []

    # --------------------------------------------------
    # Noise residual observations
    # --------------------------------------------------
    noise_residuals = components.get("noise_residuals")
    if isinstance(noise_residuals, dict) and noise_residuals.get("available"):
        observations.append(
            "Residual noise patterns were measured across frames, capturing fine-grained artifacts left after visual reconstruction."
        )

    # --------------------------------------------------
    # Temporal residual observations
    # --------------------------------------------------
    temporal_residuals = components.get("temporal_residuals")
    if isinstance(temporal_residuals, dict) and temporal_residuals.get("available"):
        observations.append(
            "Temporal residual analysis examined how noise characteristics evolve between consecutive frames."
        )

    # --------------------------------------------------
    # Fallback explanation if no components are readable
    # --------------------------------------------------
    if not observations:
        return {
            "type": "diffusion",
            "available": False,
            "explanation": (
                "Diffusion evidence was present but did not yield interpretable residual observations."
            ),
        }

    # --------------------------------------------------
    # Final explanation (neutral, auditor-safe)
    # --------------------------------------------------
    explanation = (
        "This section summarizes diffusion-related forensic signals. "
        "Diffusion models generate content through iterative noise refinement, "
        "which can leave subtle residual patterns in both spatial noise and temporal consistency. "
        "These observations describe how such residual characteristics appear in this video, "
        "and should be interpreted alongside other independent forensic signals."
    )

    return {
        "type": "diffusion",
        "available": True,
        "observations": observations,
        "explanation": explanation,
    }
