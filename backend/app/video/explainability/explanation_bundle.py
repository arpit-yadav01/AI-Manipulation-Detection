from typing import Dict, Any, List

from app.video.explainability.temporal_explainer import explain_temporal
from app.video.explainability.motion_explainer import explain_motion
from app.video.explainability.identity_explainer import explain_identity
from app.video.explainability.frame_heatmap import explain_frames


def build_video_explanations(
    *,
    temporal_signal: Dict[str, Any] | None,
    motion_signal: Dict[str, Any] | None,
    identity_signal: Dict[str, Any] | None,
    frame_results: List[Dict[str, Any]] | None,
) -> Dict[str, Any]:
    """
    Phase 3 — Video Explainability Bundle

    RULES:
    - Read-only
    - No thresholds
    - No verdicts
    - No confidence modification
    """

    explanations = []

    temporal_exp = explain_temporal(temporal_signal)
    if temporal_exp.get("available"):
        explanations.append(temporal_exp)

    motion_exp = explain_motion(motion_signal)
    if motion_exp.get("available"):
        explanations.append(motion_exp)

    identity_exp = explain_identity(identity_signal)
    if identity_exp.get("available"):
        explanations.append(identity_exp)

    frame_exp = explain_frames(frame_results or [])
    if frame_exp:
        explanations.append({
            "type": "frames",
            "available": True,
            "observations": frame_exp,
            "explanation": (
                "These frames were selected due to higher visual anomaly signals. "
                "They help illustrate where the model detected stronger patterns."
            ),
        })

    return {
        "available": len(explanations) > 0,
        "explanations": explanations,
    }
