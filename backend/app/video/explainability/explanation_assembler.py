# app/video/explainability/explanation_assembler.py

from typing import Dict, Any, List, Optional

from app.video.explainability.temporal_explainer import explain_temporal
from app.video.explainability.motion_explainer import explain_motion
from app.video.explainability.identity_explainer import explain_identity
from app.video.explainability.diffusion_explainer import explain_diffusion
from app.video.explainability.frame_heatmap import explain_frames
from app.video.explainability.calibration import explain_confidence


def build_video_explanations(
    *,
    temporal_signal: Optional[Dict[str, Any]],
    motion_signal: Optional[Dict[str, Any]],
    identity_signal: Optional[Dict[str, Any]],
    diffusion_evidence: Optional[Dict[str, Any]],
    frame_results: Optional[List[Dict[str, Any]]],
    final_confidence: Optional[float],
) -> Dict[str, Any]:
    """
    Phase 3 — Explanation Assembler (READ-ONLY)

    RULES:
    - NO verdict logic
    - NO confidence modification
    - NO thresholds
    - NO inference
    """

    key_findings: List[str] = []
    evidence_explanations: Dict[str, Any] = {}
    frame_highlights: List[Dict[str, Any]] = []

    # -----------------------------
    # Temporal
    # -----------------------------
    temporal_exp = explain_temporal(temporal_signal)
    if temporal_exp.get("available"):
        key_findings.append(
            "Temporal consistency patterns were observed across frames."
        )
        evidence_explanations["temporal"] = temporal_exp

    # -----------------------------
    # Motion
    # -----------------------------
    motion_exp = explain_motion(motion_signal)
    if motion_exp.get("available"):
        key_findings.append(
            "Motion behavior exhibited measurable variation over time."
        )
        evidence_explanations["motion"] = motion_exp

    # -----------------------------
    # Identity
    # -----------------------------
    identity_exp = explain_identity(identity_signal)
    if identity_exp.get("available"):
        key_findings.append(
            "Identity-related facial features showed variability across frames."
        )
        evidence_explanations["identity"] = identity_exp

    # -----------------------------
    # Diffusion
    # -----------------------------
    diffusion_exp = explain_diffusion(diffusion_evidence)
    if diffusion_exp.get("available"):
        key_findings.append(
            "Diffusion-related residual patterns were observed."
        )
        evidence_explanations["diffusion"] = diffusion_exp

    # -----------------------------
    # Frame highlights
    # -----------------------------
    frames_exp = explain_frames(frame_results or [])
    if frames_exp:
        frame_highlights = frames_exp

    # -----------------------------
    # Confidence explanation (READ-ONLY)
    # -----------------------------
    confidence_explanation = explain_confidence(final_confidence)

    # -----------------------------
    # Neutral summary
    # -----------------------------
    summary = (
        "This explanation summarizes observable forensic patterns detected in the video. "
        "Each section describes independent signals related to temporal behavior, motion "
        "characteristics, identity consistency, and diffusion-based residuals. "
        "No single observation should be interpreted in isolation."
    )

    return {
        "summary": summary,
        "key_findings": key_findings,
        "frame_highlights": frame_highlights,
        "evidence_explanations": evidence_explanations,
        "confidence_explanation": confidence_explanation,
    }
