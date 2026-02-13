from typing import Dict, Any, List


# ============================================================
# EVIDENCE ACCUMULATOR — PHASE 2.3
# ============================================================
# ❌ No verdicts
# ❌ No thresholds
# ❌ No hard decisions
# ✅ Soft probabilistic accumulation
# ============================================================


def _normalize(value: float, max_cap: float = 1.0) -> float:
    """
    Soft normalization into [0, 1]
    """
    try:
        value = float(value)
    except Exception:
        return 0.0

    if value <= 0:
        return 0.0

    return min(value / max_cap, 1.0)


def accumulate_evidence(
    *,
    diffusion_evidence: Dict[str, Any] | None,
    temporal_signal: Dict[str, Any] | None,
    motion_signal: Dict[str, Any] | None,
    gan_signal: Dict[str, Any] | None,
    av_sync_signal: Dict[str, Any] | None,
) -> Dict[str, Any]:
    """
    Combine heterogeneous forensic evidence into a single
    soft evidence representation.

    SAFE GUARANTEES:
    - Fail open
    - Missing signals reduce confidence, never crash
    - No verdicts
    """

    evidence_items: List[Dict[str, Any]] = []
    cumulative_score = 0.0
    weight_sum = 0.0

    # --------------------------------------------------------
    # 1️⃣ Diffusion evidence (HIGH VALUE, LOW CONFIDENCE)
    # --------------------------------------------------------
    if diffusion_evidence and diffusion_evidence.get("available"):
        score = diffusion_evidence.get("confidence_hint", 0.0)
        weight = 0.35  # strong but still soft

        evidence_items.append({
            "source": "diffusion",
            "score": round(score, 4),
            "weight": weight,
            "details": diffusion_evidence,
        })

        cumulative_score += score * weight
        weight_sum += weight

    # --------------------------------------------------------
    # 2️⃣ Temporal instability
    # --------------------------------------------------------
    if temporal_signal:
        score = 1.0 if temporal_signal.get("verdict") == "unstable" else 0.0
        weight = 0.20

        evidence_items.append({
            "source": "temporal",
            "score": score,
            "weight": weight,
            "details": temporal_signal,
        })

        cumulative_score += score * weight
        weight_sum += weight

    # --------------------------------------------------------
    # 3️⃣ Motion inconsistency
    # --------------------------------------------------------
    if motion_signal:
        score = 1.0 if motion_signal.get("verdict") == "unnatural_motion" else 0.0
        weight = 0.15

        evidence_items.append({
            "source": "motion",
            "score": score,
            "weight": weight,
            "details": motion_signal,
        })

        cumulative_score += score * weight
        weight_sum += weight

    # --------------------------------------------------------
    # 4️⃣ GAN artifacts
    # --------------------------------------------------------
    if gan_signal:
        score = 1.0 if gan_signal.get("verdict") == "gan_artifacts_detected" else 0.0
        weight = 0.15

        evidence_items.append({
            "source": "gan",
            "score": score,
            "weight": weight,
            "details": gan_signal,
        })

        cumulative_score += score * weight
        weight_sum += weight

    # --------------------------------------------------------
    # 5️⃣ Audio–visual sync
    # --------------------------------------------------------
    if av_sync_signal:
        score = 1.0 if av_sync_signal.get("verdict") == "desynced" else 0.0
        weight = 0.15

        evidence_items.append({
            "source": "av_sync",
            "score": score,
            "weight": weight,
            "details": av_sync_signal,
        })

        cumulative_score += score * weight
        weight_sum += weight

    # --------------------------------------------------------
    # Final normalization
    # --------------------------------------------------------
    if weight_sum > 0:
        final_score = cumulative_score / weight_sum
    else:
        final_score = 0.0

    return {
        "available": bool(evidence_items),
        "evidence_score": round(final_score, 4),
        "confidence_stability": round(weight_sum, 3),
        "signals_used": len(evidence_items),
        "evidence_breakdown": evidence_items,
        "phase": "2.3",
    }
