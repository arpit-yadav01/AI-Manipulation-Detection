def compute_av_sync(audio_energy, lip_motion_curve):
    """
    SAFE audio–visual sync.
    Returns INSUFFICIENT_DATA instead of crashing.
    """

    if audio_energy is None or lip_motion_curve is None:
        return {
            "verdict": "insufficient_data",
            "correlation": None,
            "confidence": 0.0,
        }

    energy_curve = audio_energy.get("energy_curve")
    if not energy_curve or len(energy_curve) < 5:
        return {
            "verdict": "insufficient_data",
            "correlation": None,
            "confidence": 0.0,
        }

    if len(lip_motion_curve) < 5:
        return {
            "verdict": "insufficient_data",
            "correlation": None,
            "confidence": 0.0,
        }

    # --- actual correlation ---
    import numpy as np

    min_len = min(len(energy_curve), len(lip_motion_curve))
    a = np.array(energy_curve[:min_len])
    b = np.array(lip_motion_curve[:min_len])

    corr = float(np.corrcoef(a, b)[0, 1])

    if corr < 0.35:
        verdict = "desynced"
        confidence = 0.15
    else:
        verdict = "synced"
        confidence = 0.0

    return {
        "verdict": verdict,
        "correlation": round(corr, 3),
        "confidence": confidence,
    }
