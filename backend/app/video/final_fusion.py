

# from app.video.explainability.calibration import calibrate_video_confidence


# # ============================================================
# # CONFIDENCE GOVERNOR
# # ============================================================

# def apply_confidence_governor(confidence: float, frames_analyzed: int) -> float:
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
# # EVIDENCE BOOST
# # ============================================================

# def apply_evidence_soft_boost(confidence: float, evidence_summary: dict | None) -> float:
#     if not isinstance(evidence_summary, dict):
#         return confidence
#     if not evidence_summary.get("available"):
#         return confidence

#     hint = float(evidence_summary.get("confidence_hint", 0.0))
#     consistency = float(evidence_summary.get("consistency_score", 0.0))

#     if hint <= 0.0 or consistency <= 0.5:
#         return confidence

#     delta = min(0.08, hint * consistency * 0.1)
#     return confidence + delta


# # ============================================================
# # CONTRADICTION CONTROL
# # ============================================================

# def apply_contradiction_dampening(
#     confidence: float,
#     *,
#     temporal_signal=None,
#     motion_signal=None,
#     blink_signal=None,
#     gaze_signal=None,
#     av_sync_signal=None,
#     evidence_summary=None,
# ) -> float:

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

#     if natural_votes < 2:
#         return confidence

#     dampening = min(0.12, natural_votes * 0.03)
#     return confidence - dampening


# # ============================================================
# # VIDEO FINAL FUSION — V8 (Signal Reporting Enabled)
# # ============================================================

# def fuse_video_signals(
#     *,
#     avg_fake_probability: float,
#     frames_analyzed: int,

#     temporal_signal=None,
#     motion_signal=None,
#     gan_signal=None,
#     video_ml_signal=None,

#     blink_signal=None,
#     gaze_signal=None,
#     adversarial_attack=None,
#     evidence_summary=None,
#     av_sync_signal=None,

#     # anomalies
#     temporal_anomaly: float = 0.0,
#     motion_anomaly: float = 0.0,
#     identity_anomaly: float = 0.0,
#     geometry_anomaly: float = 0.0,
#     av_sync_anomaly: float = 0.0,

#     # reliability
#     temporal_reliability: float = 1.0,
#     motion_reliability: float = 1.0,
#     identity_reliability: float = 1.0,
#     geometry_reliability: float = 1.0,
#     gan_reliability: float = 1.0,
#     av_reliability: float = 1.0,
# ) -> dict:

#     confidence = float(avg_fake_probability)
#     penalties = []
#     signal_breakdown = {}

#     def record(name, anomaly, reliability, weight, delta):
#         signal_breakdown[name] = {
#             "anomaly": round(anomaly, 3),
#             "reliability": round(reliability, 3),
#             "weight": weight,
#             "effective_impact": round(delta, 4),
#         }

#     # Temporal
#     delta = 0.10 * temporal_anomaly * temporal_reliability
#     confidence += delta
#     penalties.append(delta)
#     record("temporal", temporal_anomaly, temporal_reliability, 0.10, delta)

#     # Motion
#     delta = 0.08 * motion_anomaly * motion_reliability
#     confidence += delta
#     penalties.append(delta)
#     record("motion", motion_anomaly, motion_reliability, 0.08, delta)

#     # Identity
#     delta = 0.09 * identity_anomaly * identity_reliability
#     confidence += delta
#     penalties.append(delta)
#     record("identity", identity_anomaly, identity_reliability, 0.09, delta)

#     # Geometry
#     delta = 0.07 * geometry_anomaly * geometry_reliability
#     confidence += delta
#     penalties.append(delta)
#     record("geometry", geometry_anomaly, geometry_reliability, 0.07, delta)

#     # AV Sync
#     delta = 0.08 * av_sync_anomaly * av_reliability
#     confidence += delta
#     penalties.append(delta)
#     record("av_sync", av_sync_anomaly, av_reliability, 0.08, delta)

#     # GAN
#     gan_delta = 0.0
#     if gan_signal and gan_signal.get("verdict") == "gan_artifacts_detected":
#         gan_delta = 0.04 * gan_reliability
#         confidence += gan_delta
#         penalties.append(gan_delta)
#     record("gan", 1.0 if gan_delta > 0 else 0.0, gan_reliability, 0.04, gan_delta)

#     # Video ML
#     ml_delta = 0.0
#     if video_ml_signal and video_ml_signal.get("verdict") in ("AI_GENERATED", "LIKELY_AI"):
#         ml_delta = min(0.15, float(video_ml_signal.get("confidence", 0.0)) * 0.2)
#         confidence += ml_delta
#         penalties.append(ml_delta)
#     record("video_ml", 1.0 if ml_delta > 0 else 0.0, 1.0, 0.15, ml_delta)

#     confidence = apply_evidence_soft_boost(confidence, evidence_summary)

#     confidence = apply_contradiction_dampening(
#         confidence,
#         temporal_signal=temporal_signal,
#         motion_signal=motion_signal,
#         blink_signal=blink_signal,
#         gaze_signal=gaze_signal,
#         av_sync_signal=av_sync_signal,
#         evidence_summary=evidence_summary,
#     )

#     if adversarial_attack and adversarial_attack.get("available", False):
#         level = adversarial_attack.get("level", "NONE")
#         if level == "LOW":
#             confidence -= 0.03
#         elif level == "MEDIUM":
#             confidence -= 0.07
#         elif level == "HIGH":
#             confidence -= 0.12

#     confidence = calibrate_video_confidence(confidence, frames_analyzed)
#     confidence = apply_confidence_governor(confidence, frames_analyzed)
#     confidence = max(0.0, min(1.0, confidence))

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
#         "signal_breakdown": signal_breakdown,
#     }


import math
import statistics
from app.video.explainability.calibration import calibrate_video_confidence


# ============================================================
# VIDEO FINAL FUSION — V9 (Section 6 Enabled)
# ============================================================

def fuse_video_signals(
    *,
    avg_fake_probability: float,
    frames_analyzed: int,
    std_ml_fake_prob: float = 0.0,  # 🔵 NEW

    temporal_signal=None,
    motion_signal=None,
    gan_signal=None,
    video_ml_signal=None,

    blink_signal=None,
    gaze_signal=None,
    adversarial_attack=None,
    evidence_summary=None,
    av_sync_signal=None,

    # anomalies
    temporal_anomaly: float = 0.0,
    motion_anomaly: float = 0.0,
    identity_anomaly: float = 0.0,
    geometry_anomaly: float = 0.0,
    av_sync_anomaly: float = 0.0,

    # reliability
    temporal_reliability: float = 1.0,
    motion_reliability: float = 1.0,
    identity_reliability: float = 1.0,
    geometry_reliability: float = 1.0,
    gan_reliability: float = 1.0,
    av_reliability: float = 1.0,
) -> dict:

    confidence = float(avg_fake_probability)
    penalties = []
    signal_breakdown = {}

    def record(name, anomaly, reliability, weight, delta):
        signal_breakdown[name] = {
            "anomaly": round(anomaly, 3),
            "reliability": round(reliability, 3),
            "weight": weight,
            "effective_impact": round(delta, 4),
        }

    # --------------------------------------------------------
    # SIGNAL CONTRIBUTIONS
    # --------------------------------------------------------

    delta = 0.10 * temporal_anomaly * temporal_reliability
    confidence += delta
    penalties.append(delta)
    record("temporal", temporal_anomaly, temporal_reliability, 0.10, delta)

    delta = 0.08 * motion_anomaly * motion_reliability
    confidence += delta
    penalties.append(delta)
    record("motion", motion_anomaly, motion_reliability, 0.08, delta)

    delta = 0.09 * identity_anomaly * identity_reliability
    confidence += delta
    penalties.append(delta)
    record("identity", identity_anomaly, identity_reliability, 0.09, delta)

    delta = 0.07 * geometry_anomaly * geometry_reliability
    confidence += delta
    penalties.append(delta)
    record("geometry", geometry_anomaly, geometry_reliability, 0.07, delta)

    delta = 0.08 * av_sync_anomaly * av_reliability
    confidence += delta
    penalties.append(delta)
    record("av_sync", av_sync_anomaly, av_reliability, 0.08, delta)

    gan_delta = 0.0
    if gan_signal and gan_signal.get("verdict") == "gan_artifacts_detected":
        gan_delta = 0.04 * gan_reliability
        confidence += gan_delta
        penalties.append(gan_delta)

    record("gan", 1.0 if gan_delta > 0 else 0.0, gan_reliability, 0.04, gan_delta)

    ml_delta = 0.0
    if video_ml_signal and video_ml_signal.get("verdict") in ("AI_GENERATED", "LIKELY_AI"):
        ml_delta = min(0.15, float(video_ml_signal.get("confidence", 0.0)) * 0.2)
        confidence += ml_delta
        penalties.append(ml_delta)

    record("video_ml", 1.0 if ml_delta > 0 else 0.0, 1.0, 0.15, ml_delta)

    # --------------------------------------------------------
    # Evidence + Contradiction
    # --------------------------------------------------------

    confidence = calibrate_video_confidence(confidence, frames_analyzed)
    confidence = max(0.0, min(1.0, confidence))

    # =========================================================
    # 🔵 SECTION 6 — STATISTICAL CONFIDENCE MODELING
    # =========================================================

    if frames_analyzed > 1 and std_ml_fake_prob > 0:
        standard_error = std_ml_fake_prob / math.sqrt(frames_analyzed)
        ci_margin = 1.96 * standard_error
    else:
        ci_margin = 0.15  # fallback conservative margin

    lower_bound = max(0.0, confidence - ci_margin)
    upper_bound = min(1.0, confidence + ci_margin)

    anomaly_values = [
        temporal_anomaly,
        motion_anomaly,
        identity_anomaly,
        geometry_anomaly,
        av_sync_anomaly,
    ]

    try:
        volatility = statistics.pstdev(anomaly_values)
    except Exception:
        volatility = 0.0

    stability_index = max(0.0, min(1.0, 1 - volatility))

    if ci_margin < 0.05 and stability_index > 0.75:
        uncertainty_level = "LOW"
    elif ci_margin < 0.10:
        uncertainty_level = "MEDIUM"
    else:
        uncertainty_level = "HIGH"

    # --------------------------------------------------------
    # Verdict
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
        "confidence_interval": {
            "lower": round(lower_bound, 3),
            "upper": round(upper_bound, 3),
            "margin": round(ci_margin, 3),
        },
        "stability_index": round(stability_index, 3),
        "uncertainty_level": uncertainty_level,
        "frames_analyzed": frames_analyzed,
        "penalties_applied": round(sum(penalties), 3),
        "signal_breakdown": signal_breakdown,
    }
