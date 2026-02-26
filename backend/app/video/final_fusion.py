
# from app.video.explainability.calibration import calibrate_video_confidence
# from app.video.weight_learning import get_weight_registry


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
# # SECTION 7 — CROSS SIGNAL AGREEMENT
# # ============================================================

# def compute_cross_signal_agreement(signal_values):

#     if not signal_values:
#         return 1.0, 0.0

#     import statistics

#     mean_val = statistics.mean(signal_values)
#     variance = statistics.pvariance(signal_values)

#     normalized_variance = min(1.0, variance / 0.25)
#     agreement_score = 1.0 - normalized_variance

#     if agreement_score > 0.75 and mean_val > 0.5:
#         delta = 0.05
#     elif agreement_score < 0.35:
#         delta = -0.06
#     else:
#         delta = 0.0

#     return round(agreement_score, 3), delta


# # ============================================================
# # SECTION 8 — STATISTICAL UNCERTAINTY
# # ============================================================

# def compute_confidence_uncertainty(
#     confidence,
#     agreement_score,
#     signal_values,
#     frames_analyzed,
# ):
#     import statistics

#     base_variance = statistics.pvariance(signal_values) if signal_values else 0.0
#     dispersion = min(1.0, base_variance / 0.25)
#     agreement_uncertainty = 1.0 - agreement_score

#     if frames_analyzed < 10:
#         frame_factor = 0.25
#     elif frames_analyzed < 20:
#         frame_factor = 0.15
#     else:
#         frame_factor = 0.08

#     uncertainty_margin = (
#         0.4 * dispersion +
#         0.4 * agreement_uncertainty +
#         frame_factor
#     )

#     uncertainty_margin = min(0.35, max(0.03, uncertainty_margin))

#     lower = max(0.0, confidence - uncertainty_margin)
#     upper = min(1.0, confidence + uncertainty_margin)

#     if uncertainty_margin < 0.08:
#         category = "high_certainty"
#     elif uncertainty_margin < 0.18:
#         category = "moderate_certainty"
#     else:
#         category = "low_certainty"

#     return {
#         "uncertainty_margin": round(uncertainty_margin, 3),
#         "confidence_interval": [round(lower, 3), round(upper, 3)],
#         "confidence_category": category,
#     }


# # ============================================================
# # SECTION 9 — DEPENDENCY MODELING
# # ============================================================

# def compute_signal_dependency_adjustment(signal_map):

#     delta = 0.0
#     report = {}

#     if signal_map["gan"] > 0.5 and signal_map["motion"] > 0.5:
#         corr_penalty = -0.04
#         delta += corr_penalty
#         report["gan_motion_correlation"] = corr_penalty

#     if signal_map["identity"] > 0.5 and signal_map["geometry"] > 0.5:
#         corr_penalty = -0.03
#         delta += corr_penalty
#         report["identity_geometry_correlation"] = corr_penalty

#     if signal_map["av_sync"] > 0.5 and signal_map["temporal"] > 0.5:
#         corr_penalty = -0.03
#         delta += corr_penalty
#         report["av_temporal_correlation"] = corr_penalty

#     strong_signals = sum(1 for v in signal_map.values() if v > 0.6)
#     if strong_signals >= 3:
#         independence_bonus = 0.04
#         delta += independence_bonus
#         report["cross_domain_independence_bonus"] = independence_bonus

#     return delta, report


# # ============================================================
# # VIDEO FINAL FUSION (DYNAMIC WEIGHTS ENABLED)
# # ============================================================

# def fuse_video_signals(
#     *,
#     avg_fake_probability,
#     frames_analyzed,

#     temporal_signal=None,
#     motion_signal=None,
#     gan_signal=None,
#     video_ml_signal=None,

#     blink_signal=None,
#     gaze_signal=None,
#     adversarial_attack=None,
#     evidence_summary=None,
#     av_sync_signal=None,

#     temporal_anomaly=0.0,
#     motion_anomaly=0.0,
#     identity_anomaly=0.0,
#     geometry_anomaly=0.0,
#     av_sync_anomaly=0.0,

#     temporal_reliability=1.0,
#     motion_reliability=1.0,
#     identity_reliability=1.0,
#     geometry_reliability=1.0,
#     gan_reliability=1.0,
#     av_reliability=1.0,
# ):

#     confidence = float(avg_fake_probability)
#     weights = get_weight_registry()

#     penalties = []
#     signal_breakdown = {}

#     def record(name, anomaly, reliability, weight, delta):
#         signal_breakdown[name] = {
#             "anomaly": round(anomaly, 3),
#             "reliability": round(reliability, 3),
#             "weight": round(weight, 4),
#             "effective_impact": round(delta, 4),
#         }

#     # === Dynamic Weight Signals ===

#     delta = weights["temporal"] * temporal_anomaly * temporal_reliability
#     confidence += delta
#     penalties.append(delta)
#     record("temporal", temporal_anomaly, temporal_reliability, weights["temporal"], delta)

#     delta = weights["motion"] * motion_anomaly * motion_reliability
#     confidence += delta
#     penalties.append(delta)
#     record("motion", motion_anomaly, motion_reliability, weights["motion"], delta)

#     delta = weights["identity"] * identity_anomaly * identity_reliability
#     confidence += delta
#     penalties.append(delta)
#     record("identity", identity_anomaly, identity_reliability, weights["identity"], delta)

#     delta = weights["geometry"] * geometry_anomaly * geometry_reliability
#     confidence += delta
#     penalties.append(delta)
#     record("geometry", geometry_anomaly, geometry_reliability, weights["geometry"], delta)

#     delta = weights["av_sync"] * av_sync_anomaly * av_reliability
#     confidence += delta
#     penalties.append(delta)
#     record("av_sync", av_sync_anomaly, av_reliability, weights["av_sync"], delta)

#     gan_delta = 0.0
#     if gan_signal and gan_signal.get("verdict") == "gan_artifacts_detected":
#         gan_delta = weights["gan"] * gan_reliability
#         confidence += gan_delta
#         penalties.append(gan_delta)

#     record("gan", 1.0 if gan_delta > 0 else 0.0, gan_reliability, weights["gan"], gan_delta)

#     ml_delta = 0.0
#     if video_ml_signal and video_ml_signal.get("verdict") in ("AI_GENERATED", "LIKELY_AI"):
#         ml_delta = min(
#             weights["video_ml"],
#             float(video_ml_signal.get("confidence", 0.0)) * 0.2
#         )
#         confidence += ml_delta
#         penalties.append(ml_delta)

#     record("video_ml", 1.0 if ml_delta > 0 else 0.0, 1.0, weights["video_ml"], ml_delta)

#     # === Agreement ===

#     signal_values = [
#         temporal_anomaly,
#         motion_anomaly,
#         identity_anomaly,
#         geometry_anomaly,
#         av_sync_anomaly,
#         1.0 if gan_delta > 0 else 0.0,
#     ]

#     agreement_score, agreement_delta = compute_cross_signal_agreement(signal_values)
#     confidence += agreement_delta

#     signal_breakdown["cross_signal_agreement"] = {
#         "agreement_score": agreement_score,
#         "confidence_adjustment": agreement_delta,
#     }

#     # === Dependency ===

#     signal_map = {
#         "temporal": temporal_anomaly,
#         "motion": motion_anomaly,
#         "identity": identity_anomaly,
#         "geometry": geometry_anomaly,
#         "av_sync": av_sync_anomaly,
#         "gan": 1.0 if gan_delta > 0 else 0.0,
#     }

#     dependency_delta, dependency_report = compute_signal_dependency_adjustment(signal_map)
#     confidence += dependency_delta

#     signal_breakdown["signal_dependency"] = {
#         "dependency_adjustment": round(dependency_delta, 3),
#         "details": dependency_report,
#     }

#     # === Post Processing ===

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

#     # === Uncertainty ===

#     uncertainty_data = compute_confidence_uncertainty(
#         confidence,
#         agreement_score,
#         signal_values,
#         frames_analyzed,
#     )

#     # === Verdict ===

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
#         **uncertainty_data,
#     }



from app.video.explainability.calibration import calibrate_video_confidence
from app.video.weight_learning import get_weight_registry
import math


# ============================================================
# SECTION 11 — BAYESIAN CONFIG
# ============================================================

BASE_PRIOR = 0.35
LR_SCALE = 2.2
MAX_LR = 6.0  # overflow safety


# ============================================================
# CONFIDENCE GOVERNOR (Retained)
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
# SECTION 11 — LIKELIHOOD RATIO CORE
# ============================================================

def compute_likelihood_ratio(weight, anomaly, reliability, frames_analyzed):

    # Section 12 — adaptive scaling
    frame_factor = min(1.2, max(0.7, frames_analyzed / 30))

    strength = weight * anomaly * reliability
    lr = 1.0 + (strength * LR_SCALE * frame_factor)

    return min(lr, MAX_LR)


def compute_bayesian_posterior(likelihood_ratios, prior):

    # log-domain multiplication (Section 12 stability)
    log_sum = 0.0
    for lr in likelihood_ratios:
        log_sum += math.log(max(lr, 1e-6))

    combined_lr = math.exp(log_sum)

    numerator = prior * combined_lr
    denominator = numerator + (1 - prior)

    if denominator == 0:
        return 0.0

    return numerator / denominator


# ============================================================
# SECTION 9 — DEPENDENCY MODELING (Retained)
# ============================================================

def compute_signal_dependency_adjustment(signal_map):

    delta_prior = 0.0
    report = {}

    if signal_map["gan"] > 0.5 and signal_map["motion"] > 0.5:
        delta_prior -= 0.05
        report["gan_motion_overlap"] = -0.05

    if signal_map["identity"] > 0.5 and signal_map["geometry"] > 0.5:
        delta_prior -= 0.04
        report["identity_geometry_overlap"] = -0.04

    if signal_map["av_sync"] > 0.5 and signal_map["temporal"] > 0.5:
        delta_prior -= 0.04
        report["av_temporal_overlap"] = -0.04

    strong = sum(1 for v in signal_map.values() if v > 0.6)
    if strong >= 3:
        delta_prior += 0.05
        report["cross_domain_independence_bonus"] = 0.05

    return delta_prior, report


# ============================================================
# SECTION 8 — UNCERTAINTY (Retained)
# ============================================================

def compute_confidence_uncertainty(
    confidence,
    agreement_score,
    signal_values,
    frames_analyzed,
):
    import statistics

    base_variance = statistics.pvariance(signal_values) if signal_values else 0.0
    dispersion = min(1.0, base_variance / 0.25)
    agreement_uncertainty = 1.0 - agreement_score

    if frames_analyzed < 10:
        frame_factor = 0.25
    elif frames_analyzed < 20:
        frame_factor = 0.15
    else:
        frame_factor = 0.08

    uncertainty_margin = (
        0.4 * dispersion +
        0.4 * agreement_uncertainty +
        frame_factor
    )

    uncertainty_margin = min(0.35, max(0.03, uncertainty_margin))

    lower = max(0.0, confidence - uncertainty_margin)
    upper = min(1.0, confidence + uncertainty_margin)

    if uncertainty_margin < 0.08:
        category = "high_certainty"
    elif uncertainty_margin < 0.18:
        category = "moderate_certainty"
    else:
        category = "low_certainty"

    return {
        "uncertainty_margin": round(uncertainty_margin, 3),
        "confidence_interval": [round(lower, 3), round(upper, 3)],
        "confidence_category": category,
    }


# ============================================================
# SECTION 7 — AGREEMENT (Retained for uncertainty only)
# ============================================================

def compute_cross_signal_agreement(signal_values):

    if not signal_values:
        return 1.0, 0.0

    import statistics

    mean_val = statistics.mean(signal_values)
    variance = statistics.pvariance(signal_values)

    normalized_variance = min(1.0, variance / 0.25)
    agreement_score = 1.0 - normalized_variance

    return round(agreement_score, 3), 0.0


# ============================================================
# FINAL FUSION — V14 (Bayesian + Performance)
# ============================================================

def fuse_video_signals(
    *,
    avg_fake_probability,
    frames_analyzed,

    temporal_signal=None,
    motion_signal=None,
    gan_signal=None,
    video_ml_signal=None,

    blink_signal=None,
    gaze_signal=None,
    adversarial_attack=None,
    evidence_summary=None,
    av_sync_signal=None,

    temporal_anomaly=0.0,
    motion_anomaly=0.0,
    identity_anomaly=0.0,
    geometry_anomaly=0.0,
    av_sync_anomaly=0.0,

    temporal_reliability=1.0,
    motion_reliability=1.0,
    identity_reliability=1.0,
    geometry_reliability=1.0,
    gan_reliability=1.0,
    av_reliability=1.0,
):

    weights = get_weight_registry()

    signal_map = {
        "temporal": temporal_anomaly,
        "motion": motion_anomaly,
        "identity": identity_anomaly,
        "geometry": geometry_anomaly,
        "av_sync": av_sync_anomaly,
        "gan": 1.0 if gan_signal and gan_signal.get("verdict") == "gan_artifacts_detected" else 0.0,
    }

    likelihoods = []
    signal_breakdown = {}

    def process_signal(name, anomaly, reliability):

        weight = weights.get(name, 0.05)

        lr = compute_likelihood_ratio(
            weight,
            anomaly,
            reliability,
            frames_analyzed,
        )

        likelihoods.append(lr)

        signal_breakdown[name] = {
            "anomaly": round(anomaly, 3),
            "reliability": round(reliability, 3),
            "weight": round(weight, 4),
            "likelihood_ratio": round(lr, 3),
        }

    process_signal("temporal", temporal_anomaly, temporal_reliability)
    process_signal("motion", motion_anomaly, motion_reliability)
    process_signal("identity", identity_anomaly, identity_reliability)
    process_signal("geometry", geometry_anomaly, geometry_reliability)
    process_signal("av_sync", av_sync_anomaly, av_reliability)
    process_signal("gan", signal_map["gan"], gan_reliability)

    # Dependency modifies prior
    prior = BASE_PRIOR
    prior_delta, dependency_report = compute_signal_dependency_adjustment(signal_map)
    prior = max(0.05, min(0.95, prior + prior_delta))

    signal_breakdown["signal_dependency"] = dependency_report

    posterior = compute_bayesian_posterior(likelihoods, prior)

    posterior = calibrate_video_confidence(posterior, frames_analyzed)
    posterior = apply_confidence_governor(posterior, frames_analyzed)
    posterior = max(0.0, min(1.0, posterior))

    agreement_score, _ = compute_cross_signal_agreement(
        list(signal_map.values())
    )

    uncertainty_data = compute_confidence_uncertainty(
        posterior,
        agreement_score,
        list(signal_map.values()),
        frames_analyzed,
    )

    if posterior >= 0.75:
        verdict = "AI_GENERATED"
    elif posterior >= 0.40:
        verdict = "INCONCLUSIVE"
    else:
        verdict = "LIKELY_REAL"

    return {
        "verdict": verdict,
        "confidence": round(posterior, 2),
        "raw_confidence": round(posterior, 3),
        "frames_analyzed": frames_analyzed,
        "signal_breakdown": signal_breakdown,
        **uncertainty_data,
    }