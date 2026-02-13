# app/video/timeline/frame_scoring.py

from typing import Dict, Any


# ---------------------------------------
# Weights (VISUALIZATION ONLY)
# ---------------------------------------
ML_WEIGHT = 0.55
ELA_WEIGHT = 0.25
BAND_WEIGHT = 0.1
LIPSYNC_WEIGHT = 0.1  # 🔥 NEW

ELA_NORMALIZER = 30.0


def score_frame(
    frame: Dict[str, Any],
    *,
    lipsync_dominance: Dict | None = None,
) -> Dict[str, Any]:
    """
    Phase 7.1 — Frame-level manipulation scoring (UPDATED)

    NEW:
    - Lip-sync dominance can boost score
    - Face realism can be overridden visually

    STILL:
    - No verdicts
    - UI-only
    """

    ml_prob = float(frame.get("ml_fake_probability", 0.0))
    ela_score = float(frame.get("ela_score", 0.0))
    band = frame.get("confidence_band", "UNCERTAIN")

    # ---------------------------------------
    # Normalize signals
    # ---------------------------------------
    ml_component = ml_prob
    ela_component = min(ela_score / ELA_NORMALIZER, 1.0)

    if band == "STRONG_FAKE":
        band_component = 1.0
    elif band == "LIKELY_FAKE":
        band_component = 0.7
    elif band == "UNCERTAIN":
        band_component = 0.4
    else:
        band_component = 0.1

    # ---------------------------------------
    # Base score
    # ---------------------------------------
    score = (
        ML_WEIGHT * ml_component +
        ELA_WEIGHT * ela_component +
        BAND_WEIGHT * band_component
    )

    # ---------------------------------------
    # 🔥 Lip-sync dominance boost
    # ---------------------------------------
    if lipsync_dominance and lipsync_dominance.get("dominant"):
        boost = lipsync_dominance.get("severity_boost", 0.0)
        score += boost

    score = round(min(max(score, 0.0), 1.0), 3)

    # ---------------------------------------
    # Human-friendly label (UI ONLY)
    # ---------------------------------------
    if score >= 0.7:
        label = "manipulated"
    elif score >= 0.4:
        label = "suspicious"
    else:
        label = "real"

    return {
        "score": score,
        "label": label,
    }
