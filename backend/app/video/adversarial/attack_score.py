"""
Phase 4 — Adversarial Robustness Aggregation (LOCKED)

PURPOSE:
- Softly aggregate adversarial / evasion indicators
- Detect attempts to suppress or hide forensic evidence

STRICT RULES:
- NO fake/real verdicts
- NO hard decisions
- NO confidence semantics from Phase 5
- OUTPUT CONTRACT IS FINAL
"""

from typing import Dict, List


# ---------------------------------------------------------
# Helper: safe score extraction
# ---------------------------------------------------------

def _get_score(signal: Dict) -> float:
    """
    Extracts a numeric score safely from a Phase-4 signal.
    """
    try:
        return float(signal.get("score", 0.0))
    except Exception:
        return 0.0


# ---------------------------------------------------------
# Phase 4 — Aggregator
# ---------------------------------------------------------

def compute_adversarial_attack_score(
    *,
    reencoding_signal: Dict | None = None,
    bitrate_signal: Dict | None = None,
    codec_signal: Dict | None = None,

    frame_duplication_signal: Dict | None = None,
    temporal_jitter_signal: Dict | None = None,
    smoothing_signal: Dict | None = None,

    noise_floor_signal: Dict | None = None,
    residual_flattening_signal: Dict | None = None,
) -> Dict:
    """
    Aggregates Phase-4 adversarial signals into a SOFT awareness score.

    OUTPUT CONTRACT (LOCKED):
    {
        "available": true,
        "level": "LOW | MEDIUM | HIGH",
        "confidence": 0.0
    }
    """

    signals = [
        reencoding_signal,
        bitrate_signal,
        codec_signal,
        frame_duplication_signal,
        temporal_jitter_signal,
        smoothing_signal,
        noise_floor_signal,
        residual_flattening_signal,
    ]

    scores: List[float] = []

    for signal in signals:
        if not isinstance(signal, dict):
            continue

        if signal.get("available") is False:
            continue

        score = _get_score(signal)
        if score > 0:
            scores.append(score)

    if not scores:
        return {
            "available": False,
            "level": "NONE",
            "confidence": 0.0,
        }

    # -------------------------------------------------
    # Conservative aggregation (soft awareness)
    # -------------------------------------------------

    avg_score = sum(scores) / len(scores)
    peak_score = max(scores)

    combined = (0.65 * peak_score) + (0.35 * avg_score)

    # -------------------------------------------------
    # Awareness levels (NOT verdicts)
    # -------------------------------------------------

    if combined >= 0.55:
        level = "HIGH"
    elif combined >= 0.30:
        level = "MEDIUM"
    else:
        level = "LOW"

    return {
        "available": True,
        "level": level,
        "confidence": round(float(combined), 3),
    }
