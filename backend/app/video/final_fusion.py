





# from app.video.explainability.calibration import calibrate_video_confidence


# # ============================================================
# # CONFIDENCE GOVERNOR
# # ============================================================

# def apply_confidence_governor(confidence: float, frames_analyzed: int) -> float:
#     """
#     Caps confidence based on number of analyzed frames
#     to avoid overconfidence on short clips.
#     """
#     if frames_analyzed < 5:
#         cap = 0.55
#     elif frames_analyzed < 15:
#         cap = 0.75
#     elif frames_analyzed < 30:
#         cap = 0.90
#     else:
#         return confidence

#     return min(confidence, cap)


# # ============================================================
# # PHASE 2.5 — EVIDENCE SOFT BOOST
# # ============================================================

# def apply_evidence_soft_boost(
#     confidence: float,
#     evidence_summary: dict | None,
# ) -> float:
#     """
#     Soft confidence nudge from accumulated evidence.
#     NEVER decides verdict.
#     """

#     if not isinstance(evidence_summary, dict):
#         return confidence

#     if not evidence_summary.get("available"):
#         return confidence

#     hint = float(evidence_summary.get("confidence_hint", 0.0))
#     consistency = float(evidence_summary.get("consistency_score", 0.0))

#     # Conservative gate
#     if hint <= 0.0 or consistency <= 0.5:
#         return confidence

#     # Hard cap on boost
#     delta = min(0.08, hint * consistency * 0.1)
#     return confidence + delta


# # ============================================================
# # PHASE 2.6 — CONTRADICTION CONTROL
# # ============================================================

# def apply_contradiction_dampening(
#     confidence: float,
#     *,
#     temporal_signal: dict | None,
#     motion_signal: dict | None,
#     blink_signal: dict | None,
#     gaze_signal: dict | None,
#     av_sync_signal: dict | None,
#     evidence_summary: dict | None,
# ) -> float:
#     """
#     Dampens confidence when diffusion/evidence contradicts
#     strong natural signals.

#     Max dampening: -0.12
#     Fail-open design.
#     """

#     if not isinstance(evidence_summary, dict):
#         return confidence

#     if not evidence_summary.get("available"):
#         return confidence

#     natural_votes = 0

#     if temporal_signal and temporal_signal.get("verdict") == "stable":
#         natural_votes += 1

#     if motion_signal and motion_signal.get("verdict") == "natural_motion":
#         natural_votes += 1

#     if blink_signal and blink_signal.get("verdict") == "blink_normal":
#         natural_votes += 1

#     if gaze_signal and gaze_signal.get("verdict") == "gaze_stable":
#         natural_votes += 1

#     if av_sync_signal and av_sync_signal.get("verdict") == "synced":
#         natural_votes += 1

#     # Require multiple strong natural anchors
#     if natural_votes < 2:
#         return confidence

#     dampening = min(0.12, natural_votes * 0.03)
#     return confidence - dampening


# # ============================================================
# # VIDEO FINAL FUSION — V3.3 (PHASE 2.6 ENABLED)
# # ============================================================

# def fuse_video_signals(
#     *,
#     avg_fake_probability: float,
#     frames_analyzed: int,
#     high_risk_frames: int = 0,
#     ela_suspicious_frames: int = 0,

#     temporal_signal: dict | None = None,
#     motion_signal: dict | None = None,
#     gan_signal: dict | None = None,
#     identity_signal: dict | None = None,
#     video_ml_signal: dict | None = None,

#     blink_signal: dict | None = None,
#     gaze_signal: dict | None = None,
#     micro_expression_signal: dict | None = None,

#     adversarial_attack: dict | None = None,

#     # 🔥 Phase 2 brain
#     evidence_summary: dict | None = None,
#     av_sync_signal: dict | None = None,
# ) -> dict:
#     """
#     Final conservative fusion of all video-level forensic signals.
#     """

#     confidence = float(avg_fake_probability)
#     penalties: list[float] = []

#     # --------------------------------------------------------
#     # Frame-based penalties
#     # --------------------------------------------------------
#     if frames_analyzed > 0:
#         confidence += (high_risk_frames / frames_analyzed) * 0.5
#         confidence += (ela_suspicious_frames / frames_analyzed) * 0.3

#     # --------------------------------------------------------
#     # Core forensic signals
#     # --------------------------------------------------------
#     if temporal_signal and temporal_signal.get("verdict") == "unstable":
#         confidence += 0.08
#         penalties.append(0.08)

#     if motion_signal and motion_signal.get("verdict") == "unnatural_motion":
#         confidence += 0.08
#         penalties.append(0.08)

#     if gan_signal and gan_signal.get("verdict") == "gan_artifacts_detected":
#         confidence += 0.04
#         penalties.append(0.04)

#     # --------------------------------------------------------
#     # Video-level ML (soft assist)
#     # --------------------------------------------------------
#     if video_ml_signal and video_ml_signal.get("verdict") in (
#         "AI_GENERATED",
#         "LIKELY_AI",
#     ):
#         delta = min(0.15, float(video_ml_signal.get("confidence", 0.0)) * 0.2)
#         confidence += delta
#         penalties.append(delta)

#     # ========================================================
#     # PHASE 2.5 — Evidence soft boost
#     # ========================================================
#     confidence = apply_evidence_soft_boost(
#         confidence,
#         evidence_summary,
#     )

#     # ========================================================
#     # PHASE 2.6 — Contradiction control
#     # ========================================================
#     confidence = apply_contradiction_dampening(
#         confidence,
#         temporal_signal=temporal_signal,
#         motion_signal=motion_signal,
#         blink_signal=blink_signal,
#         gaze_signal=gaze_signal,
#         av_sync_signal=av_sync_signal,
#         evidence_summary=evidence_summary,
#     )

#     # ========================================================
#     # PHASE 4 — Adversarial evasion (SOFT ONLY)
#     # ========================================================
#     if adversarial_attack and adversarial_attack.get("available", False):
#         level = adversarial_attack.get("level", "NONE")

#         if level == "LOW":
#             confidence -= 0.03
#         elif level == "MEDIUM":
#             confidence -= 0.07
#         elif level == "HIGH":
#             confidence -= 0.12

#     # --------------------------------------------------------
#     # Calibration + governor
#     # --------------------------------------------------------
#     confidence = calibrate_video_confidence(confidence, frames_analyzed)
#     confidence = apply_confidence_governor(confidence, frames_analyzed)
#     confidence = max(0.0, min(1.0, confidence))

#     # --------------------------------------------------------
#     # Final verdict
#     # --------------------------------------------------------
#     if confidence >= 0.70:
#         verdict = "AI_GENERATED"
#     elif confidence >= 0.40:
#         verdict = "INCONCLUSIVE"
#     else:
#         verdict = "LIKELY_REAL"

#     return {
#         "verdict": verdict,
#         "confidence": round(confidence, 2),
#         "raw_confidence": round(confidence, 3),
#         "frames_analyzed": frames_analyzed,
#         "penalties_applied": round(sum(penalties), 3),
#     }




from app.video.explainability.calibration import calibrate_video_confidence


# ============================================================
# CONFIDENCE GOVERNOR
# ============================================================

def apply_confidence_governor(confidence: float, frames_analyzed: int) -> float:
    if frames_analyzed < 5:
        cap = 0.55
    elif frames_analyzed < 15:
        cap = 0.75
    elif frames_analyzed < 30:
        cap = 0.90
    else:
        return confidence

    return min(confidence, cap)


# ============================================================
# PHASE 2.5 — EVIDENCE SOFT BOOST
# ============================================================

def apply_evidence_soft_boost(
    confidence: float,
    evidence_summary: dict | None,
) -> float:

    if not isinstance(evidence_summary, dict):
        return confidence

    if not evidence_summary.get("available"):
        return confidence

    hint = float(evidence_summary.get("confidence_hint", 0.0))
    consistency = float(evidence_summary.get("consistency_score", 0.0))

    if hint <= 0.0 or consistency <= 0.5:
        return confidence

    delta = min(0.08, hint * consistency * 0.1)
    return confidence + delta


# ============================================================
# PHASE 2.6 — CONTRADICTION CONTROL
# ============================================================

def apply_contradiction_dampening(
    confidence: float,
    *,
    temporal_signal: dict | None,
    motion_signal: dict | None,
    blink_signal: dict | None,
    gaze_signal: dict | None,
    av_sync_signal: dict | None,
    evidence_summary: dict | None,
) -> float:

    if not isinstance(evidence_summary, dict):
        return confidence

    if not evidence_summary.get("available"):
        return confidence

    natural_votes = 0

    if temporal_signal and temporal_signal.get("verdict") == "stable":
        natural_votes += 1

    if motion_signal and motion_signal.get("verdict") == "natural_motion":
        natural_votes += 1

    if blink_signal and blink_signal.get("verdict") == "blink_normal":
        natural_votes += 1

    if gaze_signal and gaze_signal.get("verdict") == "gaze_stable":
        natural_votes += 1

    if av_sync_signal and av_sync_signal.get("verdict") == "synced":
        natural_votes += 1

    if natural_votes < 2:
        return confidence

    dampening = min(0.12, natural_votes * 0.03)
    return confidence - dampening


# ============================================================
# VIDEO FINAL FUSION — V7 (Reliability + All Safeguards)
# ============================================================

def fuse_video_signals(
    *,
    avg_fake_probability: float,
    frames_analyzed: int,
    high_risk_frames: int = 0,
    ela_suspicious_frames: int = 0,

    # Raw signals
    temporal_signal: dict | None = None,
    motion_signal: dict | None = None,
    gan_signal: dict | None = None,
    identity_signal: dict | None = None,
    video_ml_signal: dict | None = None,

    blink_signal: dict | None = None,
    gaze_signal: dict | None = None,
    micro_expression_signal: dict | None = None,

    adversarial_attack: dict | None = None,

    evidence_summary: dict | None = None,
    av_sync_signal: dict | None = None,

    # Normalized anomaly scores (0–1)
    temporal_anomaly: float = 0.0,
    motion_anomaly: float = 0.0,
    identity_anomaly: float = 0.0,
    geometry_anomaly: float = 0.0,
    av_sync_anomaly: float = 0.0,

    # 🔵 RELIABILITY MULTIPLIERS (0–1)
    temporal_reliability: float = 1.0,
    motion_reliability: float = 1.0,
    identity_reliability: float = 1.0,
    geometry_reliability: float = 1.0,
    gan_reliability: float = 1.0,
    av_reliability: float = 1.0,
) -> dict:

    confidence = float(avg_fake_probability)
    penalties: list[float] = []

    # --------------------------------------------------------
    # Frame-based penalties
    # --------------------------------------------------------
    if frames_analyzed > 0:
        confidence += (high_risk_frames / frames_analyzed) * 0.5
        confidence += (ela_suspicious_frames / frames_analyzed) * 0.3

    # --------------------------------------------------------
    # TEMPORAL
    # --------------------------------------------------------
    if temporal_anomaly > 0:
        delta = 0.10 * temporal_anomaly * temporal_reliability
        confidence += delta
        penalties.append(delta)
    elif temporal_signal and temporal_signal.get("verdict") == "unstable":
        delta = 0.08 * temporal_reliability
        confidence += delta
        penalties.append(delta)

    # --------------------------------------------------------
    # MOTION
    # --------------------------------------------------------
    if motion_anomaly > 0:
        delta = 0.08 * motion_anomaly * motion_reliability
        confidence += delta
        penalties.append(delta)
    elif motion_signal and motion_signal.get("verdict") == "unnatural_motion":
        delta = 0.08 * motion_reliability
        confidence += delta
        penalties.append(delta)

    # --------------------------------------------------------
    # IDENTITY
    # --------------------------------------------------------
    if identity_anomaly > 0:
        delta = 0.09 * identity_anomaly * identity_reliability
        confidence += delta
        penalties.append(delta)

    # --------------------------------------------------------
    # GEOMETRY
    # --------------------------------------------------------
    if geometry_anomaly > 0:
        delta = 0.07 * geometry_anomaly * geometry_reliability
        confidence += delta
        penalties.append(delta)

    # --------------------------------------------------------
    # AV SYNC
    # --------------------------------------------------------
    if av_sync_anomaly > 0:
        delta = 0.08 * av_sync_anomaly * av_reliability
        confidence += delta
        penalties.append(delta)

    # --------------------------------------------------------
    # GAN ARTIFACTS
    # --------------------------------------------------------
    if gan_signal and gan_signal.get("verdict") == "gan_artifacts_detected":
        delta = 0.04 * gan_reliability
        confidence += delta
        penalties.append(delta)

    # --------------------------------------------------------
    # VIDEO-LEVEL ML
    # --------------------------------------------------------
    if video_ml_signal and video_ml_signal.get("verdict") in (
        "AI_GENERATED",
        "LIKELY_AI",
    ):
        delta = min(0.15, float(video_ml_signal.get("confidence", 0.0)) * 0.2)
        confidence += delta
        penalties.append(delta)

    # --------------------------------------------------------
    # Evidence Soft Boost
    # --------------------------------------------------------
    confidence = apply_evidence_soft_boost(
        confidence,
        evidence_summary,
    )

    # --------------------------------------------------------
    # Contradiction Control
    # --------------------------------------------------------
    confidence = apply_contradiction_dampening(
        confidence,
        temporal_signal=temporal_signal,
        motion_signal=motion_signal,
        blink_signal=blink_signal,
        gaze_signal=gaze_signal,
        av_sync_signal=av_sync_signal,
        evidence_summary=evidence_summary,
    )

    # --------------------------------------------------------
    # Adversarial Soft Handling
    # --------------------------------------------------------
    if adversarial_attack and adversarial_attack.get("available", False):
        level = adversarial_attack.get("level", "NONE")

        if level == "LOW":
            confidence -= 0.03
        elif level == "MEDIUM":
            confidence -= 0.07
        elif level == "HIGH":
            confidence -= 0.12

    # --------------------------------------------------------
    # Calibration + Governor
    # --------------------------------------------------------
    confidence = calibrate_video_confidence(confidence, frames_analyzed)
    confidence = apply_confidence_governor(confidence, frames_analyzed)
    confidence = max(0.0, min(1.0, confidence))

    # --------------------------------------------------------
    # Final Verdict
    # --------------------------------------------------------
    if confidence >= 0.70:
        verdict = "AI_GENERATED"
    elif confidence >= 0.40:
        verdict = "INCONCLUSIVE"
    else:
        verdict = "LIKELY_REAL"

    return {
        "verdict": verdict,
        "confidence": round(confidence, 2),
        "raw_confidence": round(confidence, 3),
        "frames_analyzed": frames_analyzed,
        "penalties_applied": round(sum(penalties), 3),
    }
