# app/video/evidence/diffusion_pipeline.py

from typing import Dict, List, Optional

# ------------------------------------------------------------
# Diffusion signal imports (YOUR EXISTING FILES)
# ------------------------------------------------------------
from app.video.diffusion.noise_residual import analyze_diffusion_noise
from app.video.diffusion.temporal_residual import (
    analyze_temporal_residual_stability
)


# ============================================================
# DIFFUSION EVIDENCE PIPELINE (PHASE 2.1)
# ============================================================

def run_diffusion_evidence(
    frame_paths: List[str]
) -> Dict:
    """
    Executes diffusion-specific forensic analysis.

    IMPORTANT GUARANTEES:
    - No verdicts
    - No thresholds
    - No hard decisions
    - Fail-open (never raises)

    Output:
    Single normalized diffusion evidence object.
    """

    evidence: Dict[str, Optional[Dict]] = {
        "available": False,
        "noise_residual": None,
        "temporal_residual": None,
        "confidence_hint": 0.0,   # soft-only (0–1)
        "reason": None,
    }

    # --------------------------------------------------------
    # Safety guard
    # --------------------------------------------------------
    if not frame_paths or len(frame_paths) < 5:
        evidence["reason"] = "not_enough_frames"
        return evidence

    try:
        # ----------------------------------------------------
        # 1️⃣ Diffusion noise residual (spatial + frequency)
        # ----------------------------------------------------
        noise_signal = analyze_diffusion_noise(frame_paths)

        if noise_signal and noise_signal.get("available"):
            evidence["noise_residual"] = noise_signal

        # ----------------------------------------------------
        # 2️⃣ Temporal residual stability
        # ----------------------------------------------------
        temporal_signal = analyze_temporal_residual_stability(frame_paths)

        if temporal_signal and temporal_signal.get("available"):
            evidence["temporal_residual"] = temporal_signal

        # ----------------------------------------------------
        # 3️⃣ Availability check
        # ----------------------------------------------------
        if evidence["noise_residual"] or evidence["temporal_residual"]:
            evidence["available"] = True

        # ----------------------------------------------------
        # 4️⃣ VERY SOFT confidence hint (NO THRESHOLDS)
        # ----------------------------------------------------
        confidence = 0.0

        if evidence["noise_residual"]:
            confidence += float(
                evidence["noise_residual"].get("anomaly_score", 0.0)
            )

        if evidence["temporal_residual"]:
            confidence += float(
                evidence["temporal_residual"].get(
                    "temporal_stability_score", 0.0
                )
            )

        # Clamp gently (never dominate system)
        evidence["confidence_hint"] = round(
            min(confidence, 0.25), 4
        )

    except Exception as e:
        # FAIL OPEN — never break pipeline
        evidence["available"] = False
        evidence["reason"] = f"diffusion_error: {str(e)}"

    return evidence
