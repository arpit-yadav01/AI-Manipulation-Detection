# app/video/lipsync/speech_presence.py

from typing import Dict


def detect_speech_presence(audio_energy: Dict) -> Dict:
    """
    Phase 8.1 — Speech / Singing Presence Detector

    PURPOSE:
    - Decide whether lip-sync analysis should dominate
    - Based purely on audio energy patterns

    RULES:
    - Read-only
    - No verdicts
    - Conservative
    """

    if not isinstance(audio_energy, dict):
        return {
            "available": False,
            "speech_present": False,
            "confidence": 0.0,
        }

    if not audio_energy.get("available"):
        return {
            "available": False,
            "speech_present": False,
            "confidence": 0.0,
        }

    mean_energy = audio_energy.get("mean_energy", 0.0)
    variance = audio_energy.get("energy_variance", 0.0)

    # Conservative speech detection
    if mean_energy > 0.12 and variance > 0.01:
        return {
            "available": True,
            "speech_present": True,
            "confidence": round(min(1.0, mean_energy + variance), 3),
        }

    return {
        "available": True,
        "speech_present": False,
        "confidence": round(mean_energy, 3),
    }
