# app/video/lipsync/lipsync_dominance.py

from typing import Dict


def compute_lipsync_dominance(
    *,
    speech_signal: Dict,
    av_sync_signal: Dict,
) -> Dict:
    """
    Phase 8.1 — Lip-Sync Dominance Controller

    PURPOSE:
    - Decide whether mouth/audio mismatch should dominate interpretation

    RULES:
    - No verdict override
    - No hard classification
    - Read-only influence
    """

    if not speech_signal.get("available"):
        return {
            "available": False,
            "dominant": False,
            "severity_boost": 0.0,
            "reason": "no_audio_signal",
        }

    if not speech_signal.get("speech_present"):
        return {
            "available": True,
            "dominant": False,
            "severity_boost": 0.0,
            "reason": "no_speech_detected",
        }

    # Speech exists → mouth matters
    av_conf = av_sync_signal.get("confidence", 0.0)
    verdict = av_sync_signal.get("verdict", "unknown")

    if verdict in ("desynced", "mismatch", "insufficient_data"):
        return {
            "available": True,
            "dominant": True,
            "severity_boost": 0.12,

            "reason": "speech_present_but_lips_desynced",
        }

    if av_conf < 0.4:
        return {
            "available": True,
            "dominant": True,
            "severity_boost": 0.07,

            "reason": "weak_lip_sync",
        }

    return {
        "available": True,
        "dominant": False,
        "severity_boost": 0.0,
        "reason": "lip_sync_consistent",
    }
