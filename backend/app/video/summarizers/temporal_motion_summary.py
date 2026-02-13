def summarize_temporal(signal: dict) -> float:
    if not signal:
        return 0.0

    stability = signal.get("stability_score")
    if stability is None:
        return 0.0

    return max(0.0, min(1.0 - float(stability), 1.0))


def summarize_motion(signal: dict) -> float:
    if not signal:
        return 0.0

    variance = signal.get("motion_variance")
    if variance is None:
        return 0.0

    return max(0.0, min(float(variance) / 3.0, 1.0))
