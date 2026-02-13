# app/video/explainability/calibration.py

from typing import Optional


def calibrate_video_confidence(
    raw_confidence: float,
    frames_analyzed: int,
) -> float:
    """
    Frame-aware confidence calibration.

    Confidence represents probability of AI generation.
    - Short videos are down-weighted
    - Long videos gain confidence gradually
    - Meaning is NEVER inverted
    """

    confidence = max(0.0, min(1.0, float(raw_confidence)))

    if frames_analyzed < 5:
        evidence_factor = 0.40
        hard_cap = 0.45
    elif frames_analyzed < 10:
        evidence_factor = 0.55
        hard_cap = 0.65
    elif frames_analyzed < 20:
        evidence_factor = 0.70
        hard_cap = None
    elif frames_analyzed < 40:
        evidence_factor = 0.85
        hard_cap = None
    else:
        evidence_factor = 1.0
        hard_cap = None

    confidence *= evidence_factor

    if confidence < 0.10:
        confidence *= 0.5
    elif confidence < 0.30:
        confidence *= 0.75
    elif confidence < 0.60:
        confidence *= 0.9

    if hard_cap is not None:
        confidence = min(confidence, hard_cap)

    return confidence


# ============================================================
# 🔒 PHASE 3 — READ-ONLY CONFIDENCE EXPLANATION
# ============================================================

def explain_confidence(confidence: Optional[float]) -> str:
    """
    Human-readable explanation of the final confidence value.

    RULES:
    - READ ONLY
    - NO recalibration
    - NO thresholds
    - NO verdicts
    """

    if confidence is None:
        return (
            "A confidence score could not be computed for this video due to "
            "insufficient or incomplete analysis signals."
        )

    confidence = max(0.0, min(1.0, float(confidence)))

    if confidence < 0.25:
        return (
            "The system observed limited forensic indicators. "
            "The confidence level is low, meaning the analysis did not find "
            "strong or consistent patterns associated with AI generation."
        )

    if confidence < 0.50:
        return (
            "Some forensic irregularities were observed, but they were not "
            "consistently strong across the video. The confidence reflects "
            "moderate uncertainty."
        )

    if confidence < 0.75:
        return (
            "Multiple forensic signals showed noticeable irregularities. "
            "The confidence indicates a meaningful likelihood of synthetic "
            "or manipulated content, though no single signal dominates."
        )

    return (
        "Strong and consistent forensic patterns were observed across "
        "multiple independent signals. The confidence reflects a high "
        "likelihood of AI-generated or manipulated content."
    )
