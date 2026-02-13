import librosa
import numpy as np
from typing import Dict


def extract_audio_energy(
    video_path: str,
    hop_length: int = 512
) -> Dict:
    """
    Extracts normalized audio energy over time.
    Returns structured signal only.
    """

    try:
        # Load audio from video
        audio, sr = librosa.load(video_path, sr=None)

    except Exception:
        return {
            "available": False,
            "reason": "no_audio",
        }

    if audio is None or len(audio) == 0:
        return {
            "available": False,
            "reason": "empty_audio",
        }

    # Root Mean Square Energy
    rms = librosa.feature.rms(y=audio, hop_length=hop_length)[0]

    # Normalize (0–1)
    rms_norm = (rms - rms.min()) / (rms.max() - rms.min() + 1e-6)

    return {
        "available": True,
        "frames": len(rms_norm),
        "mean_energy": round(float(np.mean(rms_norm)), 4),
        "energy_variance": round(float(np.var(rms_norm)), 4),
        "energy_curve": rms_norm.tolist(),  # used later for sync
    }
