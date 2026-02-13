from typing import Dict, Any


def classify_video(
    *,
    frame_stats: Dict[str, Any],
    identity_stats: Dict[str, Any],
    geometry_stats: Dict[str, Any] | None,
    audio_sync_stats: Dict[str, Any] | None,
) -> Dict[str, Any]:
    """
    Phase 3 · Step 3
    Video-level forensic classifier (SAFE MODE)

    Returns verdict + confidence + explainable reasons.
    """

    confidence = 0.0
    reasons = []

    # ----------------------------------
    # 1️⃣ Frame ML consistency
    # ----------------------------------
    avg_fake = frame_stats.get("avg_ml_fake_prob", 0.0)
    std_fake = frame_stats.get("std_ml_fake_prob", 0.0)

    if avg_fake > 0.75:
        confidence += 0.40
        reasons.append("High average frame-level fake probability")

    if std_fake < 0.05 and avg_fake > 0.55:
        confidence += 0.15
        reasons.append("Consistent fake signal across frames")

    # ----------------------------------
    # 2️⃣ Identity drift (CRITICAL)
    # ----------------------------------
    identity_drift = identity_stats.get("identity_drift")

    if identity_drift:
        drift_mean = identity_drift.get("mean", 0.0)
        drift_max = identity_drift.get("max", 0.0)

        if drift_mean > 0.08:
            confidence += 0.25
            reasons.append("High temporal identity drift")

        if drift_max > 0.15:
            confidence += 0.10
            reasons.append("Sudden identity jumps detected")

    # ----------------------------------
    # 3️⃣ Geometry & lighting drift
    # ----------------------------------
    if geometry_stats:
        if geometry_stats.get("verdict") == "unstable":
            confidence += 0.10
            reasons.append("Unstable head pose / lighting physics")

    # ----------------------------------
    # 4️⃣ Audio–Visual sync
    # ----------------------------------
    if audio_sync_stats:
        if audio_sync_stats.get("verdict") == "desynced":
            confidence += 0.15
            reasons.append("Lip motion and audio energy mismatch")

    # ----------------------------------
    # 5️⃣ Clamp + verdict
    # ----------------------------------
    confidence = min(confidence, 1.0)

    if confidence >= 0.75:
        verdict = "AI_GENERATED"
    elif confidence >= 0.45:
        verdict = "LIKELY_AI"
    else:
        verdict = "LIKELY_REAL"

    return {
        "verdict": verdict,
        "confidence": round(confidence, 3),
        "reasons": reasons,
        "classifier_version": "phase3_rule_v1",
    }
