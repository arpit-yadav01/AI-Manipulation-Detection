import numpy as np
from typing import List, Dict, Optional


# ============================================================
# HEAD POSE TEMPORAL DRIFT
# ============================================================

def compute_head_pose_drift(
    head_poses: List[Optional[Dict]]
) -> Dict:
    """
    Computes temporal drift of head pose (yaw, pitch, roll).

    Input:
        [
          {"yaw": 2.1, "pitch": -1.3, "roll": 0.5},
          {"yaw": 2.3, "pitch": -1.2, "roll": 0.6},
          None,
          ...
        ]

    Output:
        Structured statistics ONLY (no verdict).
    """

    # Filter valid poses
    valid = [p for p in head_poses if p is not None]

    if len(valid) < 3:
        return {
            "available": False,
            "reason": "not_enough_faces",
        }

    # Extract sequences
    yaw = np.array([p["yaw"] for p in valid])
    pitch = np.array([p["pitch"] for p in valid])
    roll = np.array([p["roll"] for p in valid])

    # Frame-to-frame deltas
    yaw_delta = np.diff(yaw)
    pitch_delta = np.diff(pitch)
    roll_delta = np.diff(roll)

    return {
        "available": True,

        # Raw variance (how spread values are)
        "variance": {
            "yaw": round(float(np.var(yaw)), 4),
            "pitch": round(float(np.var(pitch)), 4),
            "roll": round(float(np.var(roll)), 4),
        },

        # Jitter (frame-to-frame instability)
        "delta_variance": {
            "yaw": round(float(np.var(yaw_delta)), 4),
            "pitch": round(float(np.var(pitch_delta)), 4),
            "roll": round(float(np.var(roll_delta)), 4),
        },

        # Max jump (important forensic clue)
        "max_jump": {
            "yaw": round(float(np.max(np.abs(yaw_delta))), 2),
            "pitch": round(float(np.max(np.abs(pitch_delta))), 2),
            "roll": round(float(np.max(np.abs(roll_delta))), 2),
        },

        "frames_used": len(valid),
    }


# ============================================================
# LIGHTING TEMPORAL DRIFT
# ============================================================

def compute_lighting_drift(
    lightings: List[Optional[Dict]]
) -> Dict:
    """
    Computes temporal drift of lighting asymmetry.

    We track brightness difference between left & right
    over time and measure instability.
    """

    valid = [l for l in lightings if l is not None]

    if len(valid) < 3:
        return {
            "available": False,
            "reason": "not_enough_frames",
        }

    # Brightness difference over time
    diff = np.array([l["difference"] for l in valid])

    diff_delta = np.diff(diff)

    return {
        "available": True,

        # Overall fluctuation
        "variance": round(float(np.var(diff)), 4),

        # Frame-to-frame flicker
        "delta_variance": round(float(np.var(diff_delta)), 4),

        # Maximum lighting jump
        "max_jump": round(float(np.max(np.abs(diff_delta))), 2),

        # Direction instability
        "direction_changes": int(
            sum(
                1 for i in range(1, len(valid))
                if valid[i]["direction"] != valid[i - 1]["direction"]
            )
        ),

        "frames_used": len(valid),
    }
